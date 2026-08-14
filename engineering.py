"""
Fluid Flow & Heat Transfer Engineering Suite - Engineering Engine
===================================================================
Module D: Core Object-Oriented Engineering Calculations

This module provides physical and numerical models for:
1. Fluid properties representation (Density, Viscosity, Kinematic Viscosity)
2. Pipe hydraulics & Flow analysis (Reynolds number, Haaland & Colebrook friction factor, pressure drop)
3. Steady-state Fourier Conduction & Newton's Law of Cooling transient calculations

Authors: Engineering Application Specialists
"""

import math
from typing import Dict, Tuple, Optional, List
import numpy as np
import pandas as pd


class Fluid:
    """
    Represents a fluid medium with essential thermo-physical properties.

    Attributes:
        name (str): Name or description of the fluid.
        density (float): Fluid density in kg/m^3.
        dynamic_viscosity (float): Dynamic viscosity in Pa.s (N.s/m^2 or kg/(m.s)).
    """

    PRESETS: Dict[str, Dict[str, float]] = {
        "Water": {"density": 998.2, "viscosity": 0.001002},
        "Air": {"density": 1.204, "viscosity": 1.825e-5},
        "Crude Oil": {"density": 860.0, "viscosity": 0.025000},
        "Custom": {"density": 1000.0, "viscosity": 0.001000},
    }

    def __init__(self, name: str, density: float, dynamic_viscosity: float):
        """
        Initialize a Fluid object with density and dynamic viscosity.

        Args:
            name (str): Identifier name for the fluid.
            density (float): Density in kg/m^3 (must be > 0).
            dynamic_viscosity (float): Dynamic viscosity in Pa.s (must be > 0).

        Raises:
            ValueError: If density or dynamic_viscosity is non-positive.
        """
        if density <= 0:
            raise ValueError(f"Fluid density must be positive (> 0), got {density} kg/m^3.")
        if dynamic_viscosity <= 0:
            raise ValueError(f"Fluid dynamic viscosity must be positive (> 0), got {dynamic_viscosity} Pa.s.")

        self.name = str(name).strip() or "Unnamed Fluid"
        self.density = float(density)
        self.dynamic_viscosity = float(dynamic_viscosity)

    @classmethod
    def from_preset(cls, preset_name: str, custom_density: Optional[float] = None, custom_viscosity: Optional[float] = None) -> "Fluid":
        """
        Create a Fluid instance from standard presets or fallback to custom values.

        Args:
            preset_name (str): Preset name ('Water', 'Air', 'Crude Oil', or 'Custom').
            custom_density (float, optional): Custom density override if preset is 'Custom'.
            custom_viscosity (float, optional): Custom viscosity override if preset is 'Custom'.

        Returns:
            Fluid: Instantiated Fluid object.
        """
        if preset_name in cls.PRESETS and preset_name != "Custom":
            data = cls.PRESETS[preset_name]
            return cls(preset_name, data["density"], data["viscosity"])
        
        rho = custom_density if custom_density is not None else cls.PRESETS["Custom"]["density"]
        mu = custom_viscosity if custom_viscosity is not None else cls.PRESETS["Custom"]["viscosity"]
        return cls("Custom Fluid", rho, mu)

    @property
    def kinematic_viscosity(self) -> float:
        """
        Calculates kinematic viscosity nu = mu / rho in m^2/s.

        Returns:
            float: Kinematic viscosity in m^2/s.
        """
        return self.dynamic_viscosity / self.density

    def __repr__(self) -> str:
        return f"Fluid(name='{self.name}', density={self.density:.2f} kg/m³, viscosity={self.dynamic_viscosity:.4e} Pa·s)"


class Pipe:
    """
    Represents a circular cross-section conduit for fluid flow modeling.

    Attributes:
        diameter (float): Internal pipe diameter in meters (m).
        length (float): Pipe length in meters (m).
        roughness (float): Absolute pipe wall roughness epsilon in meters (m).
    """

    def __init__(self, diameter: float, length: float, roughness: float = 0.000045):
        """
        Initialize a Pipe object.

        Args:
            diameter (float): Inner diameter of the pipe in meters (m). Must be > 0.
            length (float): Total length of the pipe in meters (m). Must be > 0.
            roughness (float): Absolute pipe roughness in meters (m). Must be >= 0. Default is 0.045 mm (commercial steel).

        Raises:
            ValueError: If diameter or length is <= 0 or roughness is < 0.
        """
        if diameter <= 0:
            raise ValueError(f"Pipe diameter must be greater than zero, got {diameter} m.")
        if length <= 0:
            raise ValueError(f"Pipe length must be greater than zero, got {length} m.")
        if roughness < 0:
            raise ValueError(f"Pipe roughness cannot be negative, got {roughness} m.")

        self.diameter = float(diameter)
        self.length = float(length)
        self.roughness = float(roughness)

    @property
    def cross_sectional_area(self) -> float:
        """
        Calculates internal cross-sectional area: A = (pi * D^2) / 4 in m^2.

        Returns:
            float: Area in square meters (m^2).
        """
        return (math.pi * (self.diameter ** 2)) / 4.0

    @property
    def relative_roughness(self) -> float:
        """
        Calculates relative roughness: epsilon / D (dimensionless).

        Returns:
            float: Relative roughness.
        """
        return self.roughness / self.diameter

    def calculate_velocity(self, volumetric_flow_rate: float) -> float:
        """
        Calculates bulk mean flow velocity: v = Q / A in m/s.

        Args:
            volumetric_flow_rate (float): Volumetric flow rate Q in m^3/s. Must be >= 0.

        Returns:
            float: Mean flow velocity in m/s.

        Raises:
            ValueError: If volumetric_flow_rate is negative.
        """
        if volumetric_flow_rate < 0:
            raise ValueError(f"Flow rate cannot be negative, received {volumetric_flow_rate} m³/s.")
        return volumetric_flow_rate / self.cross_sectional_area

    def calculate_reynolds_number(self, volumetric_flow_rate: float, fluid: Fluid) -> float:
        """
        Calculates dimensionless Reynolds Number: Re = (rho * v * D) / mu.

        Args:
            volumetric_flow_rate (float): Volumetric flow rate Q in m^3/s.
            fluid (Fluid): Fluid object containing density and dynamic viscosity.

        Returns:
            float: Reynolds number (dimensionless).
        """
        velocity = self.calculate_velocity(volumetric_flow_rate)
        if velocity == 0:
            return 0.0
        re = (fluid.density * velocity * self.diameter) / fluid.dynamic_viscosity
        return re

    @staticmethod
    def flow_regime(reynolds_number: float) -> str:
        """
        Classifies the flow regime based on the Reynolds number.

        Args:
            reynolds_number (float): Reynolds number.

        Returns:
            str: 'Laminar' (Re < 2300), 'Transitional' (2300 <= Re <= 4000), or 'Turbulent' (Re > 4000).
        """
        if reynolds_number <= 0:
            return "Static (No Flow)"
        elif reynolds_number < 2300:
            return "Laminar"
        elif 2300 <= reynolds_number <= 4000:
            return "Transitional"
        else:
            return "Turbulent"

    def calculate_friction_factor(self, reynolds_number: float) -> float:
        """
        Calculates the Darcy-Weisbach friction factor (f).
        - For Laminar flow (Re < 2300): Hagen-Poiseuille formula: f = 64 / Re.
        - For Turbulent flow (Re >= 2300): Explicit Haaland Equation:
          1 / sqrt(f) = -1.8 * log10( ((epsilon/D)/3.7)^1.11 + 6.9/Re )

        Args:
            reynolds_number (float): Reynolds number.

        Returns:
            float: Darcy-Weisbach friction factor f (dimensionless).
        """
        if reynolds_number <= 0:
            return 0.0

        if reynolds_number < 2300:
            # Laminar flow
            return 64.0 / reynolds_number

        # Turbulent flow (Haaland explicit equation approximation of Colebrook-White)
        rel_roughness = self.relative_roughness
        term1 = (rel_roughness / 3.7) ** 1.11
        term2 = 6.9 / reynolds_number
        inv_sqrt_f = -1.8 * math.log10(term1 + term2)

        if inv_sqrt_f <= 0:
            return 0.008  # Lower physical boundary safeguard

        f = 1.0 / (inv_sqrt_f ** 2)
        return f

    def calculate_pressure_drop(self, volumetric_flow_rate: float, fluid: Fluid) -> Tuple[float, float, float, float]:
        """
        Calculates hydraulic metrics: Velocity, Reynolds Number, Friction factor, and Pressure Drop (Delta P).
        Uses the Darcy-Weisbach equation:
        Delta P = f * (L / D) * (rho * v^2 / 2)

        Args:
            volumetric_flow_rate (float): Volumetric flow rate Q in m^3/s.
            fluid (Fluid): Fluid instance.

        Returns:
            Tuple[float, float, float, float]: (velocity [m/s], reynolds_number, friction_factor, delta_p [Pa])
        """
        velocity = self.calculate_velocity(volumetric_flow_rate)
        reynolds = self.calculate_reynolds_number(volumetric_flow_rate, fluid)
        friction_factor = self.calculate_friction_factor(reynolds)

        if velocity == 0:
            return 0.0, 0.0, 0.0, 0.0

        # Darcy-Weisbach equation for pressure drop in Pascals (Pa)
        delta_p = friction_factor * (self.length / self.diameter) * (0.5 * fluid.density * (velocity ** 2))
        return velocity, reynolds, friction_factor, delta_p

    def generate_flow_curve(self, fluid: Fluid, q_min: float, q_max: float, num_points: int = 50) -> pd.DataFrame:
        """
        Generates a tabular dataset of flow rates and corresponding pressure drops.

        Args:
            fluid (Fluid): Fluid instance.
            q_min (float): Minimum volumetric flow rate in m^3/s.
            q_max (float): Maximum volumetric flow rate in m^3/s.
            num_points (int): Number of evaluation points.

        Returns:
            pd.DataFrame: DataFrame containing Q (m^3/s, L/min, m^3/h), Velocity, Re, f, and Delta P (Pa and kPa, bar).
        """
        if q_min < 0 or q_max <= q_min:
            raise ValueError("q_min must be >= 0 and q_max must be strictly greater than q_min.")
        if num_points < 2:
            num_points = 2

        q_vals = np.linspace(q_min, q_max, num_points)
        records = []

        for q in q_vals:
            v, re, f, dp = self.calculate_pressure_drop(float(q), fluid)
            records.append({
                "Flow Rate (m³/s)": q,
                "Flow Rate (L/min)": q * 60000.0,
                "Flow Rate (m³/h)": q * 3600.0,
                "Velocity (m/s)": v,
                "Reynolds Number": re,
                "Regime": self.flow_regime(re),
                "Friction Factor (f)": f,
                "Pressure Drop (Pa)": dp,
                "Pressure Drop (kPa)": dp / 1000.0,
                "Pressure Drop (bar)": dp / 100000.0,
            })

        return pd.DataFrame(records)

    def __repr__(self) -> str:
        return f"Pipe(diameter={self.diameter*1000:.1f} mm, length={self.length:.2f} m, roughness={self.roughness*1e6:.1f} µm)"


class HeatTransfer:
    """
    Provides engineering models for steady-state conduction and transient convective cooling.
    """

    @staticmethod
    def fourier_conduction(thermal_conductivity: float, area: float, t_hot: float, t_cold: float, thickness: float) -> Dict[str, float]:
        """
        Computes 1D steady-state thermal conduction through a planar wall using Fourier's Law:
        Q_dot = k * A * (T_hot - T_cold) / L

        Args:
            thermal_conductivity (float): Thermal conductivity k in W/(m.K). Must be > 0.
            area (float): Heat transfer surface area A in m^2. Must be > 0.
            t_hot (float): Higher surface temperature T1 in °C or K.
            t_cold (float): Lower surface temperature T2 in °C or K.
            thickness (float): Wall thickness L in meters (m). Must be > 0.

        Returns:
            Dict[str, float]: Dictionary containing:
                - 'heat_rate_watts' (W)
                - 'heat_rate_kw' (kW)
                - 'heat_flux' (W/m^2)
                - 'thermal_resistance' (K/W)
                - 'delta_t' (K or °C)

        Raises:
            ValueError: If k, area, or thickness are non-positive.
        """
        if thermal_conductivity <= 0:
            raise ValueError(f"Thermal conductivity must be positive, got {thermal_conductivity} W/(m·K).")
        if area <= 0:
            raise ValueError(f"Surface area must be positive, got {area} m².")
        if thickness <= 0:
            raise ValueError(f"Wall thickness must be positive, got {thickness} m.")

        delta_t = abs(t_hot - t_cold)
        thermal_resistance = thickness / (thermal_conductivity * area)
        heat_rate = (thermal_conductivity * area * delta_t) / thickness
        heat_flux = heat_rate / area

        return {
            "heat_rate_watts": heat_rate,
            "heat_rate_kw": heat_rate / 1000.0,
            "heat_flux": heat_flux,
            "thermal_resistance": thermal_resistance,
            "delta_t": delta_t
        }

    @staticmethod
    def newtons_cooling_time(
        t_initial: float,
        t_target: float,
        t_ambient: float,
        cooling_constant: float
    ) -> float:
        """
        Calculates time required to reach a target temperature under Newton's Law of Cooling:
        T(t) = T_ambient + (T_initial - T_ambient) * exp(-k * t)
        => t = - (1 / k) * ln((T_target - T_ambient) / (T_initial - T_ambient))

        Args:
            t_initial (float): Initial object temperature (°C).
            t_target (float): Target object temperature (°C).
            t_ambient (float): Ambient surrounding temperature (°C).
            cooling_constant (float): Lumped cooling rate coefficient k in 1/s (or 1/min). Must be > 0.

        Returns:
            float: Time in seconds required to reach target temperature.

        Raises:
            ValueError: If parameters violate thermodynamic physical bounds.
        """
        if cooling_constant <= 0:
            raise ValueError("Cooling rate constant k must be strictly positive (> 0).")

        # Check for cooling scenario (T_initial > T_ambient)
        if t_initial > t_ambient:
            if t_target <= t_ambient:
                raise ValueError(f"Target temperature ({t_target}°C) cannot cool below or reach ambient ({t_ambient}°C) in finite time.")
            if t_target >= t_initial:
                raise ValueError(f"Target temperature ({t_target}°C) must be lower than initial temperature ({t_initial}°C) for cooling.")
        
        # Check for heating scenario (T_initial < t_ambient)
        elif t_initial < t_ambient:
            if t_target >= t_ambient:
                raise ValueError(f"Target temperature ({t_target}°C) cannot warm above or reach ambient ({t_ambient}°C) in finite time.")
            if t_target <= t_initial:
                raise ValueError(f"Target temperature ({t_target}°C) must be higher than initial temperature ({t_initial}°C) for warming.")
        
        else:
            # Already at equilibrium
            return 0.0

        ratio = (t_target - t_ambient) / (t_initial - t_ambient)
        if ratio <= 0:
            raise ValueError("Invalid temperature ratio; target temperature cannot cross asymptotic ambient temperature.")

        time_val = - (1.0 / cooling_constant) * math.log(ratio)
        return max(0.0, time_val)

    @staticmethod
    def generate_cooling_curve(
        t_initial: float,
        t_ambient: float,
        cooling_constant: float,
        total_time: float,
        num_points: int = 100
    ) -> pd.DataFrame:
        """
        Generates dynamic cooling curve data over time.

        Args:
            t_initial (float): Initial temperature (°C).
            t_ambient (float): Ambient temperature (°C).
            cooling_constant (float): Cooling coefficient k (1/s).
            total_time (float): Total observation duration (s). Must be > 0.
            num_points (int): Number of sampling points.

        Returns:
            pd.DataFrame: DataFrame with columns 'Time (s)', 'Time (min)', 'Temperature (°C)', and 'Delta T (°C)'.
        """
        if total_time <= 0:
            total_time = 100.0
        if num_points < 10:
            num_points = 10

        time_array = np.linspace(0, total_time, num_points)
        temp_array = t_ambient + (t_initial - t_ambient) * np.exp(-cooling_constant * time_array)
        delta_t_array = np.abs(temp_array - t_ambient)

        return pd.DataFrame({
            "Time (s)": time_array,
            "Time (min)": time_array / 60.0,
            "Temperature (°C)": temp_array,
            "Temperature Difference (°C)": delta_t_array
        })
