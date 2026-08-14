"""
Fluid Flow & Heat Transfer Engineering Suite - Streamlit Frontend
==================================================================
Sophisticated Dark Theme Edition

A multi-module engineering application for fluid mechanics, thermal calculations,
and rock & fluid petrophysical data analysis.

Modules:
- Module A: Pipe Flow Analyser
- Module B: Heat Transfer Calculator
- Module C: Rock & Fluid Data Dashboard
"""

import io
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from engineering import Fluid, Pipe, HeatTransfer

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Fluid Flow & Heat Transfer Suite | Engineering Edition",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# SOPHISTICATED DARK THEME STYLING
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global App Background and Text */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Top Header & Titles */
    .app-brand {
        font-family: 'Cinzel', serif;
        color: #d4af37;
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.2rem;
    }
    .app-tagline {
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        color: #8b949e;
        margin-bottom: 1.2rem;
    }

    .main-title {
        font-family: 'Cinzel', serif;
        font-size: 1.85rem;
        font-weight: 700;
        color: #f0f6fc;
        letter-spacing: -0.01em;
        margin-bottom: 0.25rem;
    }
    .sub-title {
        font-size: 0.88rem;
        color: #8b949e;
        margin-bottom: 1.5rem;
        letter-spacing: 0.02em;
    }
    .module-badge {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: #d4af37;
        background: rgba(212, 175, 55, 0.1);
        border: 1px solid rgba(212, 175, 55, 0.3);
        padding: 3px 10px;
        border-radius: 4px;
        margin-bottom: 0.6rem;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #010409 !important;
        border-right: 1px solid #30363d !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #f0f6fc;
        font-family: 'Cinzel', serif;
    }

    /* Cards & Containers */
    .dark-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .card-title {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: #8b949e;
        margin-bottom: 8px;
    }
    .gold-accent {
        color: #d4af37;
    }

    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 14px 18px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="stMetric"]:hover {
        border-color: rgba(212, 175, 55, 0.5);
        transition: border-color 0.2s ease;
    }
    div[data-testid="stMetricLabel"] p {
        font-size: 0.68rem !important;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: #8b949e !important;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Cinzel', serif !important;
        color: #f0f6fc !important;
        font-size: 1.6rem !important;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 0.75rem !important;
        font-weight: 500;
    }

    /* Form Controls & Inputs */
    .stSelectbox label, .stNumberInput label, .stSlider label, .stTextInput label, .stRadio label {
        font-size: 0.78rem !important;
        color: #8b949e !important;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton > button, div[data-testid="stDownloadButton"] > button {
        background-color: transparent !important;
        color: #d4af37 !important;
        border: 1px solid #d4af37 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 0.78rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        padding: 8px 18px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover, div[data-testid="stDownloadButton"] > button:hover {
        background-color: #d4af37 !important;
        color: #0d1117 !important;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.35) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #010409;
        padding: 6px;
        border-radius: 8px;
        border: 1px solid #30363d;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 18px;
        color: #8b949e;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 500;
        letter-spacing: 0.04em;
    }
    .stTabs [aria-selected="true"] {
        background-color: #161b22 !important;
        color: #d4af37 !important;
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        font-weight: 600;
    }

    /* Dataframe & Tables */
    div[data-testid="stDataFrame"] {
        border: 1px solid #30363d;
        border-radius: 8px;
        overflow: hidden;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
        color: #f0f6fc !important;
        font-size: 0.85rem !important;
    }
    div[data-testid="stExpander"] {
        border: none !important;
        margin-top: 10px;
    }
    
    /* Dividers */
    hr {
        border-color: #30363d !important;
    }
</style>
""", unsafe_allow_html=True)

# Plotly Sophisticated Dark Theme Template
PLOTLY_DARK_LAYOUT = dict(
    paper_bgcolor="#161b22",
    plot_bgcolor="#0d1117",
    font=dict(color="#8b949e", family="Inter, sans-serif", size=12),
    title=dict(font=dict(color="#f0f6fc", family="Cinzel, serif", size=15)),
    xaxis=dict(
        gridcolor="#21262d",
        zerolinecolor="#30363d",
        tickfont=dict(color="#8b949e", size=11),
        title_font=dict(color="#c9d1d9", size=12)
    ),
    yaxis=dict(
        gridcolor="#21262d",
        zerolinecolor="#30363d",
        tickfont=dict(color="#8b949e", size=11),
        title_font=dict(color="#c9d1d9", size=12)
    ),
    legend=dict(
        bgcolor="rgba(22, 27, 34, 0.8)",
        bordercolor="#30363d",
        borderwidth=1,
        font=dict(color="#e6edf3", size=11)
    )
)


# ==============================================================================
# HELPER FUNCTIONS & SYNTHETIC DATA GENERATOR
# ==============================================================================
@st.cache_data
def get_sample_petrophysics_data() -> pd.DataFrame:
    """Generates a realistic petrophysics and core sample dataset for Module C."""
    np.random.seed(42)
    n_samples = 120
    sample_ids = [f"CORE-{1000 + i}" for i in range(n_samples)]
    depths = np.round(np.linspace(2100.0, 2450.0, n_samples) + np.random.normal(0, 1.5, n_samples), 2)
    
    porosity = np.clip(np.random.normal(18.5, 4.8, n_samples), 4.0, 32.0)
    log_k = 0.18 * porosity + np.random.normal(0.2, 0.45, n_samples) - 1.2
    permeability = np.round(np.clip(10 ** log_k, 0.01, 2500.0), 3)
    grain_density = np.round(np.random.normal(2.65, 0.03, n_samples), 3)
    water_sat = np.round(np.clip(85.0 / (porosity ** 0.6) + np.random.normal(0, 5, n_samples), 10.0, 95.0), 1)
    lithology = np.where(grain_density > 2.68, "Carbonate", np.where(porosity > 20, "Clean Sandstone", "Shaly Sandstone"))

    return pd.DataFrame({
        "Sample_ID": sample_ids,
        "Depth_m": depths,
        "Porosity_pct": np.round(porosity, 2),
        "Permeability_mD": permeability,
        "Grain_Density_gcc": grain_density,
        "Water_Saturation_pct": water_sat,
        "Lithology": lithology
    })


# ==============================================================================
# SIDEBAR NAVIGATION
# ==============================================================================
with st.sidebar:
    st.markdown('<div class="app-brand">Fluid Flow Suite</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-tagline">Engineering Edition v4.2</div>', unsafe_allow_html=True)
    st.divider()
    
    selected_module = st.radio(
        "Navigation",
        (
            "Module A: Pipe Flow Analyser",
            "Module B: Heat Transfer Calculator",
            "Module C: Rock & Fluid Data Dashboard"
        ),
        index=0
    )
    
    st.divider()
    
    # System Status / Telemetry widget
    st.markdown("""
    <div style="background-color: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 15px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 0.65rem; color: #8b949e; text-transform: uppercase; letter-spacing: 0.15em;">Calculation Engine</span>
            <span style="font-size: 0.65rem; color: #3fb950; font-weight: 600;">ACTIVE</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <span style="font-size: 0.65rem; color: #8b949e; text-transform: uppercase; letter-spacing: 0.1em;">Precision</span>
            <span style="font-size: 0.65rem; color: #d4af37; font-family: 'JetBrains Mono', monospace;">IEEE 754 DP</span>
        </div>
        <div style="width: 100%; background-color: #30363d; height: 3px; border-radius: 2px; margin-top: 8px;">
            <div style="background-color: #d4af37; height: 3px; width: 100%; border-radius: 2px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("• SI Metric Standards (m, kg, s, Pa, W, °C)")
    st.caption("• Darcy-Weisbach & Haaland Eq.")
    st.caption("• 1D Fourier & Newton's Cooling")


# ==============================================================================
# MODULE A: PIPE FLOW ANALYSER
# ==============================================================================
if selected_module == "Module A: Pipe Flow Analyser":
    st.markdown('<div class="module-badge">Module A / Hydraulic Engineering</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Pipe Flow & Hydraulic Analyser</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Hydraulic pressure drop, Reynolds flow regime, and Darcy friction factor analysis across conduits.</div>', unsafe_allow_html=True)

    col_config, col_results = st.columns([1, 2], gap="large")

    with col_config:
        st.markdown('<div class="card-title">1. Fluid Thermo-Physical Properties</div>', unsafe_allow_html=True)
        fluid_option = st.selectbox(
            "Fluid Selection Preset:",
            ["Water", "Air", "Crude Oil", "Custom"],
            help="Select a standard fluid or choose 'Custom' to define density and viscosity."
        )

        preset_data = Fluid.PRESETS.get(fluid_option, Fluid.PRESETS["Custom"])

        if fluid_option == "Custom":
            density_val = st.number_input(
                "Fluid Density ρ (kg/m³):",
                min_value=0.1,
                max_value=25000.0,
                value=float(preset_data["density"]),
                step=10.0,
                format="%.2f"
            )
            viscosity_val = st.number_input(
                "Dynamic Viscosity μ (Pa·s):",
                min_value=1e-7,
                max_value=100.0,
                value=float(preset_data["viscosity"]),
                step=1e-5,
                format="%.6f"
            )
        else:
            density_val = float(preset_data["density"])
            viscosity_val = float(preset_data["viscosity"])
            st.markdown(f"""
            <div style="background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 10px; margin-bottom: 12px; font-size: 0.78rem;">
                <span style="color: #8b949e;">Preset Density:</span> <strong style="color: #f0f6fc;">{density_val} kg/m³</strong><br>
                <span style="color: #8b949e;">Preset Viscosity:</span> <strong style="color: #f0f6fc;">{viscosity_val:.3e} Pa·s</strong>
            </div>
            """, unsafe_allow_html=True)

        try:
            current_fluid = Fluid(fluid_option, density_val, viscosity_val)
        except Exception as e:
            st.error(f"Fluid Configuration Error: {e}")
            st.stop()

        st.markdown('<div class="card-title" style="margin-top: 18px;">2. Pipe Geometry & Roughness</div>', unsafe_allow_html=True)
        diameter_mm = st.number_input(
            "Internal Pipe Diameter (mm):",
            min_value=1.0,
            max_value=5000.0,
            value=50.0,
            step=5.0,
            help="Internal diameter D in millimeters."
        )
        diameter_m = diameter_mm / 1000.0

        length_m = st.number_input(
            "Pipe Length L (m):",
            min_value=0.1,
            max_value=100000.0,
            value=100.0,
            step=10.0,
            help="Total conduit length in meters."
        )

        roughness_material = st.selectbox(
            "Pipe Material / Absolute Roughness ε:",
            [
                "Commercial Steel (0.045 mm)",
                "Drawn Tubing / Copper / Plastic (0.0015 mm)",
                "Cast Iron (0.26 mm)",
                "Galvanized Iron (0.15 mm)",
                "Smooth Glass / PVC (0.000 mm)",
                "Custom Value"
            ]
        )

        roughness_presets = {
            "Commercial Steel (0.045 mm)": 0.000045,
            "Drawn Tubing / Copper / Plastic (0.0015 mm)": 0.0000015,
            "Cast Iron (0.26 mm)": 0.00026,
            "Galvanized Iron (0.15 mm)": 0.00015,
            "Smooth Glass / PVC (0.000 mm)": 0.0000001,
        }

        if roughness_material == "Custom Value":
            roughness_mm = st.number_input(
                "Absolute Roughness ε (mm):",
                min_value=0.0,
                max_value=20.0,
                value=0.045,
                step=0.005,
                format="%.5f"
            )
            roughness_m = roughness_mm / 1000.0
        else:
            roughness_m = roughness_presets[roughness_material]

        try:
            current_pipe = Pipe(diameter=diameter_m, length=length_m, roughness=roughness_m)
        except Exception as e:
            st.error(f"Pipe Configuration Error: {e}")
            st.stop()

        st.markdown('<div class="card-title" style="margin-top: 18px;">3. Operating Flow Rate</div>', unsafe_allow_html=True)
        flow_unit = st.selectbox("Flow Rate Unit:", ["Liters / minute (L/min)", "m³ / hour (m³/h)", "m³ / second (m³/s)"])
        
        if flow_unit == "Liters / minute (L/min)":
            q_input = st.number_input("Volumetric Flow Rate (L/min):", min_value=0.01, max_value=500000.0, value=300.0, step=25.0)
            q_m3s = q_input / 60000.0
        elif flow_unit == "m³ / hour (m³/h)":
            q_input = st.number_input("Volumetric Flow Rate (m³/h):", min_value=0.001, max_value=50000.0, value=18.0, step=1.0)
            q_m3s = q_input / 3600.0
        else:
            q_input = st.number_input("Volumetric Flow Rate (m³/s):", min_value=0.00001, max_value=100.0, value=0.005, step=0.001, format="%.5f")
            q_m3s = q_input

    with col_results:
        try:
            vel, re, f, dp_pa = current_pipe.calculate_pressure_drop(q_m3s, current_fluid)
            flow_regime = current_pipe.flow_regime(re)
            head_loss_m = dp_pa / (current_fluid.density * 9.80665)
        except Exception as err:
            st.error(f"Calculation Error: {err}")
            st.stop()

        st.markdown('<div class="card-title">Key Hydraulic Performance Indicators</div>', unsafe_allow_html=True)
        
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.metric("Velocity (v)", f"{vel:.2f} m/s", help="Mean cross-sectional velocity v = Q / A")
        with m_col2:
            regime_badge = "🟢" if flow_regime == "Laminar" else ("🟡" if flow_regime == "Transitional" else "🔵")
            st.metric("Reynolds No. (Re)", f"{re:,.0f}", delta=f"{regime_badge} {flow_regime}")
        with m_col3:
            st.metric("Friction Factor (f)", f"{f:.4f}", help="Darcy friction factor via Hagen-Poiseuille or Haaland equation")
        with m_col4:
            st.metric("Pressure Drop (ΔP)", f"{dp_pa/1000.0:.2f} kPa", delta=f"{dp_pa/100000.0:.3f} bar")

        st.markdown(f"""
        <div style="display: flex; gap: 20px; font-size: 0.8rem; color: #8b949e; margin-top: 4px; margin-bottom: 16px;">
            <span>Hydrostatic Head Loss (<strong style="color: #f0f6fc;">h_f</strong>): <span style="color: #d4af37; font-family: 'JetBrains Mono', monospace;">{head_loss_m:.3f} m</span></span>
            <span>Relative Roughness (<strong style="color: #f0f6fc;">ε/D</strong>): <span style="color: #d4af37; font-family: 'JetBrains Mono', monospace;">{current_pipe.relative_roughness:.6f}</span></span>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.markdown('<div class="card-title">Pressure Drop Characteristic Curve</div>', unsafe_allow_html=True)

        sweep_col1, sweep_col2 = st.columns(2)
        with sweep_col1:
            min_flow_factor = st.slider("Min Flow Factor (% of current):", 10, 80, 20) / 100.0
        with sweep_col2:
            max_flow_factor = st.slider("Max Flow Factor (% of current):", 120, 400, 250) / 100.0

        q_min_sweep = max(0.000001, q_m3s * min_flow_factor)
        q_max_sweep = q_m3s * max_flow_factor

        df_flow_curve = current_pipe.generate_flow_curve(current_fluid, q_min_sweep, q_max_sweep, num_points=60)

        # Plotly chart with Sophisticated Dark styling
        fig_curve = go.Figure()
        fig_curve.add_trace(go.Scatter(
            x=df_flow_curve["Flow Rate (L/min)"],
            y=df_flow_curve["Pressure Drop (kPa)"],
            mode="lines",
            name="ΔP Curve",
            line=dict(color="#d4af37", width=2.5),
            hovertemplate="<b>Flow:</b> %{x:.1f} L/min<br><b>Pressure Drop:</b> %{y:.2f} kPa<extra></extra>"
        ))
        
        # Operating point marker
        fig_curve.add_trace(go.Scatter(
            x=[q_m3s * 60000.0],
            y=[dp_pa / 1000.0],
            mode="markers+text",
            name="Current Op Point",
            text=[" Current Op Point"],
            textposition="top right",
            marker=dict(color="#f0f6fc", size=9, line=dict(color="#d4af37", width=2), symbol="circle")
        ))

        fig_curve.update_layout(
            **PLOTLY_DARK_LAYOUT,
            title="System Pressure Drop vs Volumetric Flow Rate",
            xaxis_title="Volumetric Flow Rate (L/min)",
            yaxis_title="Frictional Pressure Drop ΔP (kPa)",
            hovermode="x unified",
            height=380,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_curve, use_container_width=True)

        # Table & CSV Export Button
        with st.expander("📊 View Detailed Data Table & Export Results"):
            st.dataframe(df_flow_curve.style.format({
                "Flow Rate (m³/s)": "{:.6f}",
                "Flow Rate (L/min)": "{:.2f}",
                "Flow Rate (m³/h)": "{:.2f}",
                "Velocity (m/s)": "{:.3f}",
                "Reynolds Number": "{:,.0f}",
                "Friction Factor (f)": "{:.5f}",
                "Pressure Drop (Pa)": "{:,.1f}",
                "Pressure Drop (kPa)": "{:.3f}",
                "Pressure Drop (bar)": "{:.4f}"
            }), use_container_width=True, height=240)

            csv_buffer = io.StringIO()
            df_flow_curve.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📥 Export Pipe Flow Analysis to CSV",
                data=csv_buffer.getvalue(),
                file_name=f"pipe_flow_analysis_{fluid_option.lower()}.csv",
                mime="text/csv"
            )

        with st.expander("📖 Theoretical Governing Equations"):
            st.markdown(r"""
            **1. Reynolds Number ($Re$):**
            $$Re = \frac{\rho \cdot v \cdot D}{\mu}$$
            - $Re < 2300$: Laminar Flow
            - $2300 \le Re \le 4000$: Transitional Flow
            - $Re > 4000$: Turbulent Flow

            **2. Darcy-Weisbach Friction Factor ($f$):**
            - Laminar: $f = \frac{64}{Re}$
            - Turbulent (Haaland explicit formulation):
            $$\frac{1}{\sqrt{f}} = -1.8 \log_{10}\left[ \left(\frac{\varepsilon / D}{3.7}\right)^{1.11} + \frac{6.9}{Re} \right]$$

            **3. Darcy-Weisbach Pressure Drop ($\Delta P$):**
            $$\Delta P = f \cdot \frac{L}{D} \cdot \frac{\rho \cdot v^2}{2}$$
            """)


# ==============================================================================
# MODULE B: HEAT TRANSFER CALCULATOR
# ==============================================================================
elif selected_module == "Module B: Heat Transfer Calculator":
    st.markdown('<div class="module-badge">Module B / Thermal Systems</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Heat Transfer Engineering Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Dual-mode thermal modeling: 1D Fourier conduction and Newton\'s Law of Cooling transient dynamics.</div>', unsafe_allow_html=True)

    tab_conduction, tab_cooling = st.tabs([
        "🧱 Section 1: Steady-State Conduction (Flat Wall)",
        "🌡️ Section 2: Newton's Law of Cooling (Transient)"
    ])

    # --------------------------------------------------------------------------
    # SECTION 1: STEADY-STATE CONDUCTION
    # --------------------------------------------------------------------------
    with tab_conduction:
        st.subheader("1D Steady-State Conduction Across a Planar Wall")
        st.caption("Calculates heat conduction rate, heat flux, and thermal resistance according to Fourier's Law.")

        c_col1, c_col2 = st.columns([1, 1], gap="large")

        with c_col1:
            st.markdown('<div class="card-title">Wall Material & Geometric Dimensions</div>', unsafe_allow_html=True)
            
            mat_choice = st.selectbox(
                "Material Selection Preset:",
                [
                    "Copper (k = 385 W/m·K)",
                    "Aluminum (k = 205 W/m·K)",
                    "Carbon Steel (k = 50 W/m·K)",
                    "Concrete (k = 1.4 W/m·K)",
                    "Common Brick (k = 0.72 W/m·K)",
                    "Glass (k = 0.80 W/m·K)",
                    "Fiberglass Insulation (k = 0.038 W/m·K)",
                    "Custom Material"
                ]
            )

            mat_k_presets = {
                "Copper (k = 385 W/m·K)": 385.0,
                "Aluminum (k = 205 W/m·K)": 205.0,
                "Carbon Steel (k = 50 W/m·K)": 50.0,
                "Concrete (k = 1.4 W/m·K)": 1.4,
                "Common Brick (k = 0.72 W/m·K)": 0.72,
                "Glass (k = 0.80 W/m·K)": 0.80,
                "Fiberglass Insulation (k = 0.038 W/m·K)": 0.038,
            }

            if mat_choice == "Custom Material":
                k_val = st.number_input(
                    "Thermal Conductivity k (W/(m·K)):",
                    min_value=0.001,
                    max_value=5000.0,
                    value=1.5,
                    step=0.1,
                    help="Material thermal conductivity in Watts per meter-Kelvin."
                )
            else:
                k_val = mat_k_presets[mat_choice]
                st.markdown(f"""
                <div style="background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 8px 12px; margin-bottom: 12px; font-size: 0.78rem;">
                    <span style="color: #8b949e;">Conductivity (k):</span> <strong style="color: #d4af37;">{k_val} W/(m·K)</strong>
                </div>
                """, unsafe_allow_html=True)

            area_val = st.number_input(
                "Surface Area A (m²):",
                min_value=0.01,
                max_value=10000.0,
                value=12.0,
                step=1.0,
                help="Cross-sectional area perpendicular to heat flow direction."
            )

            thickness_cm = st.number_input(
                "Wall Thickness L (cm):",
                min_value=0.1,
                max_value=500.0,
                value=15.0,
                step=1.0,
                help="Thickness of the planar slab."
            )
            thickness_m = thickness_cm / 100.0

            st.markdown('<div class="card-title" style="margin-top: 14px;">Boundary Temperatures</div>', unsafe_allow_html=True)
            t1_val = st.number_input(
                "Surface 1 Temperature T₁ (°C):",
                value=95.0,
                step=5.0,
                help="Temperature at the hot or outer boundary."
            )
            t2_val = st.number_input(
                "Surface 2 Temperature T₂ (°C):",
                value=20.0,
                step=5.0,
                help="Temperature at the cold or inner boundary."
            )

        with c_col2:
            st.markdown('<div class="card-title">Fourier Conduction Thermal Performance</div>', unsafe_allow_html=True)
            try:
                cond_results = HeatTransfer.fourier_conduction(
                    thermal_conductivity=k_val,
                    area=area_val,
                    t_hot=t1_val,
                    t_cold=t2_val,
                    thickness=thickness_m
                )
            except Exception as e:
                st.error(f"Calculation Error: {e}")
                st.stop()

            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric("Heat Flow (Q̇)", f"{cond_results['heat_rate_kw']:.2f} kW", f"{cond_results['heat_rate_watts']:,.0f} W")
                st.metric("Thermal Resistance", f"{cond_results['thermal_resistance']:.5f} K/W")
            with res_col2:
                st.metric("Heat Flux (q″)", f"{cond_results['heat_flux']:.1f} W/m²")
                st.metric("Temperature ΔT", f"{cond_results['delta_t']:.1f} °C")

            st.divider()
            
            # Interactive Temperature Profile across wall thickness
            x_pts = np.linspace(0, thickness_cm, 50)
            t_profile = t1_val + (t2_val - t1_val) * (x_pts / thickness_cm)

            fig_profile = px.line(
                x=x_pts,
                y=t_profile,
                labels={"x": "Wall Position x (cm)", "y": "Temperature T(x) (°C)"},
                title=f"Steady-State Temperature Gradient Across Wall ({thickness_cm} cm)"
            )
            fig_profile.update_traces(line=dict(color="#d4af37", width=2.5))
            fig_profile.update_layout(
                **PLOTLY_DARK_LAYOUT,
                height=300,
                margin=dict(l=40, r=40, t=50, b=40)
            )
            st.plotly_chart(fig_profile, use_container_width=True)

            with st.expander("📖 Fourier's Conduction Law Formulation"):
                st.latex(r"\dot{Q} = k \cdot A \cdot \frac{T_1 - T_2}{L} = \frac{\Delta T}{R_{th}}")
                st.latex(r"q'' = \frac{\dot{Q}}{A} = k \cdot \frac{\Delta T}{L}, \quad R_{th} = \frac{L}{k \cdot A}")

    # --------------------------------------------------------------------------
    # SECTION 2: NEWTON'S LAW OF COOLING
    # --------------------------------------------------------------------------
    with tab_cooling:
        st.subheader("Newton's Law of Cooling & Transient Thermal Curve")
        st.caption("Models lumped thermal relaxation where the rate of temperature change is proportional to the difference with ambient.")

        cool_col1, cool_col2 = st.columns([1, 1], gap="large")

        with cool_col1:
            st.markdown('<div class="card-title">Thermal Boundary Conditions</div>', unsafe_allow_html=True)
            t_initial = st.slider("Initial Temperature T₀ (°C):", min_value=-20.0, max_value=400.0, value=90.0, step=1.0)
            t_ambient = st.slider("Ambient Environment Temperature T_∞ (°C):", min_value=-40.0, max_value=100.0, value=22.0, step=1.0)

            if t_initial > t_ambient:
                min_target = t_ambient + 0.1
                max_target = t_initial - 0.1
                default_target = t_ambient + (t_initial - t_ambient) * 0.3
                mode_desc = "Cooling Mode (T₀ > T_∞)"
            elif t_initial < t_ambient:
                min_target = t_initial + 0.1
                max_target = t_ambient - 0.1
                default_target = t_initial + (t_ambient - t_initial) * 0.7
                mode_desc = "Heating Mode (T₀ < T_∞)"
            else:
                min_target = t_ambient - 1.0
                max_target = t_ambient + 1.0
                default_target = t_ambient
                mode_desc = "Equilibrium (T₀ = T_∞)"

            st.markdown(f"""
            <div style="background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 6px 12px; margin-bottom: 12px; font-size: 0.75rem; color: #d4af37;">
                • System Mode: <strong>{mode_desc}</strong>
            </div>
            """, unsafe_allow_html=True)

            t_target = st.slider(
                "Target Temperature T_target (°C):",
                min_value=float(min_target),
                max_value=float(max_target),
                value=float(default_target),
                step=0.5
            )

            st.markdown('<div class="card-title" style="margin-top: 14px;">Cooling Rate Parameter (k)</div>', unsafe_allow_html=True)
            k_cool_min = st.slider(
                "Cooling Constant k (1/min):",
                min_value=0.005,
                max_value=1.0,
                value=0.08,
                step=0.005,
                help="Lumped parameter k = (h * A) / (m * Cp) expressed per minute."
            )
            k_cool_sec = k_cool_min / 60.0

            observation_mins = st.slider(
                "Observation Time Window (minutes):",
                min_value=5,
                max_value=300,
                value=60,
                step=5
            )

        with cool_col2:
            st.markdown('<div class="card-title">Transient Calculations & Thermal Curve</div>', unsafe_allow_html=True)
            
            try:
                time_sec = HeatTransfer.newtons_cooling_time(
                    t_initial=t_initial,
                    t_target=t_target,
                    t_ambient=t_ambient,
                    cooling_constant=k_cool_sec
                )
                time_min = time_sec / 60.0
                st.markdown(f"""
                <div style="background-color: #161b22; border: 1px solid rgba(212, 175, 55, 0.4); border-radius: 8px; padding: 12px 16px; margin-bottom: 14px;">
                    <span style="font-size: 0.7rem; color: #8b949e; text-transform: uppercase; letter-spacing: 0.15em;">Time to Reach Target ({t_target:.1f} °C)</span>
                    <h3 style="font-family: 'Cinzel', serif; color: #d4af37; margin: 4px 0 0 0; font-size: 1.5rem;">{time_min:.2f} <span style="font-size: 0.9rem; color: #8b949e; font-style: italic;">minutes</span> <span style="font-size: 0.8rem; color: #8b949e;">({time_sec:.0f} s)</span></h3>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Note: {e}")
                time_min = None

            # Generate time series
            df_cooling = HeatTransfer.generate_cooling_curve(
                t_initial=t_initial,
                t_ambient=t_ambient,
                cooling_constant=k_cool_sec,
                total_time=observation_mins * 60.0,
                num_points=120
            )

            fig_cool = go.Figure()
            fig_cool.add_trace(go.Scatter(
                x=df_cooling["Time (min)"],
                y=df_cooling["Temperature (°C)"],
                mode="lines",
                name="Object T(t)",
                line=dict(color="#d4af37", width=2.5)
            ))

            # Ambient baseline
            fig_cool.add_hline(
                y=t_ambient,
                line_dash="dash",
                line_color="#8b949e",
                annotation_text=f"Ambient T_∞ ({t_ambient}°C)",
                annotation_position="bottom right",
                annotation_font=dict(color="#8b949e", size=10)
            )

            # Target temperature line
            fig_cool.add_hline(
                y=t_target,
                line_dash="dot",
                line_color="#3fb950",
                annotation_text=f"Target ({t_target}°C)",
                annotation_position="top right",
                annotation_font=dict(color="#3fb950", size=10)
            )

            # Intersect point if calculated
            if time_min is not None and time_min <= observation_mins:
                fig_cool.add_trace(go.Scatter(
                    x=[time_min],
                    y=[t_target],
                    mode="markers+text",
                    name="Target Reached",
                    text=[f" {time_min:.1f} min"],
                    textposition="top right",
                    marker=dict(color="#f0f6fc", size=8, line=dict(color="#d4af37", width=2), symbol="diamond")
                ))

            fig_cool.update_layout(
                **PLOTLY_DARK_LAYOUT,
                title="Newton's Law of Cooling Dynamic Temperature Curve",
                xaxis_title="Elapsed Time (minutes)",
                yaxis_title="Temperature (°C)",
                height=340,
                margin=dict(l=40, r=40, t=50, b=40)
            )
            st.plotly_chart(fig_cool, use_container_width=True)

            with st.expander("📖 Newton's Law of Cooling Formulation"):
                st.latex(r"\frac{dT}{dt} = -k (T - T_\infty)")
                st.latex(r"T(t) = T_\infty + (T_0 - T_\infty)e^{-k t}")
                st.latex(r"t = -\frac{1}{k}\ln\left(\frac{T_{target} - T_\infty}{T_0 - T_\infty}\right)")


# ==============================================================================
# MODULE C: ROCK & FLUID DATA DASHBOARD
# ==============================================================================
elif selected_module == "Module C: Rock & Fluid Data Dashboard":
    st.markdown('<div class="module-badge">Module C / Petrophysical Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Rock & Fluid Data Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Interactive petrophysical analytics, dynamic porosity/permeability crossplotting, and distribution modeling.</div>', unsafe_allow_html=True)

    col_upload1, col_upload2 = st.columns([2, 1])
    with col_upload1:
        uploaded_file = st.file_uploader(
            "Upload Petrophysics / Rock & Fluid CSV File:",
            type=["csv"],
            help="Upload a CSV with numeric rock properties (e.g. Porosity, Permeability, Depth)."
        )
    with col_upload2:
        use_sample = st.checkbox("Use Built-in Reservoir Petrophysics Sample Dataset", value=(uploaded_file is None))

    df_active: pd.DataFrame = None

    if uploaded_file is not None:
        try:
            df_active = pd.read_csv(uploaded_file)
            st.success(f"✅ Loaded file: `{uploaded_file.name}` ({len(df_active)} rows, {len(df_active.columns)} columns)")
        except Exception as e:
            st.error(f"Error parsing uploaded CSV: {e}")
            st.stop()
    elif use_sample:
        df_active = get_sample_petrophysics_data()
        st.markdown("""
        <div style="background-color: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 8px 12px; margin-bottom: 12px; font-size: 0.78rem; color: #8b949e;">
            ℹ️ Active Dataset: <strong style="color: #d4af37;">Reservoir Core Benchmark (120 samples)</strong>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Please upload a CSV file or check 'Use Built-in Reservoir Petrophysics Sample Dataset' to explore the dashboard.")
        st.stop()

    numeric_cols = df_active.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_cols) == 0:
        st.error("Uploaded CSV contains no numerical columns. Please upload a dataset with numeric properties.")
        st.stop()

    st.divider()

    # 1. Summary Statistics
    st.markdown('<div class="card-title">1. Exploratory Summary Statistics (df.describe())</div>', unsafe_allow_html=True)
    tab_stats, tab_preview = st.tabs(["📈 Statistical Summary Table", "🔍 Raw Data Preview"])
    with tab_stats:
        st.dataframe(df_active.describe().T.style.format("{:.3f}"), use_container_width=True)
    with tab_preview:
        st.dataframe(df_active.head(50), use_container_width=True, height=240)

    st.divider()

    # 2. Dynamic Filtering
    st.markdown('<div class="card-title">2. Dynamic Dataset Filtering</div>', unsafe_allow_html=True)
    default_filter_col = "Porosity_pct" if "Porosity_pct" in df_active.columns else numeric_cols[0]
    
    f_col1, f_col2, f_col3 = st.columns([1, 1, 1])
    
    with f_col1:
        filter_column = st.selectbox("Primary Filter Column:", numeric_cols, index=numeric_cols.index(default_filter_col))
    
    min_col_val = float(df_active[filter_column].min())
    max_col_val = float(df_active[filter_column].max())

    with f_col2:
        filter_threshold = st.slider(
            f"Filter Samples where {filter_column} ≥ Value:",
            min_value=min_col_val,
            max_value=max_col_val,
            value=min_col_val,
            step=(max_col_val - min_col_val) / 100.0 if max_col_val > min_col_val else 1.0,
            format="%.2f"
        )

    cat_cols = df_active.select_dtypes(include=["object", "category"]).columns.tolist()
    with f_col3:
        if len(cat_cols) > 0:
            cat_choice = st.selectbox("Filter by Category (Optional):", ["All"] + list(df_active[cat_cols[0]].unique()))
        else:
            cat_choice = "All"

    filtered_df = df_active[df_active[filter_column] >= filter_threshold]
    if len(cat_cols) > 0 and cat_choice != "All":
        filtered_df = filtered_df[filtered_df[cat_cols[0]] == cat_choice]

    st.markdown(f"""
    <div style="font-size: 0.8rem; color: #8b949e; margin-bottom: 12px;">
        Filtered Sample Count: <strong style="color: #d4af37; font-family: 'JetBrains Mono', monospace;">{len(filtered_df)}</strong> of {len(df_active)} samples (<strong style="color: #f0f6fc;">{len(filtered_df)/max(1, len(df_active))*100:.1f}%</strong>)
    </div>
    """, unsafe_allow_html=True)

    if filtered_df.empty:
        st.warning("⚠️ No data points match the selected filter threshold. Please adjust the slider.")
        st.stop()

    st.divider()

    # 3. Interactive Charts
    st.markdown('<div class="card-title">3. Petrophysical Distribution & Crossplot Charts</div>', unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2, gap="large")

    with chart_col1:
        hist_col = st.selectbox("Histogram Variable:", numeric_cols, index=numeric_cols.index(filter_column), key="hist_var")
        bins_count = st.slider("Number of Histogram Bins:", min_value=5, max_value=50, value=20)

        fig_hist = px.histogram(
            filtered_df,
            x=hist_col,
            nbins=bins_count,
            color_discrete_sequence=["#d4af37"],
            marginal="box",
            title=f"Distribution of {hist_col}"
        )
        mean_val = filtered_df[hist_col].mean()
        fig_hist.add_vline(
            x=mean_val,
            line_dash="dash",
            line_color="#f0f6fc",
            annotation_text=f"Mean: {mean_val:.2f}",
            annotation_font=dict(color="#f0f6fc", size=10)
        )
        fig_hist.update_layout(
            **PLOTLY_DARK_LAYOUT,
            height=360,
            margin=dict(l=30, r=30, t=50, b=40)
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with chart_col2:
        default_x = "Porosity_pct" if "Porosity_pct" in numeric_cols else numeric_cols[0]
        default_y = "Permeability_mD" if "Permeability_mD" in numeric_cols else (numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0])
        
        scat_x = st.selectbox("X-Axis (e.g. Porosity):", numeric_cols, index=numeric_cols.index(default_x), key="scat_x")
        scat_y = st.selectbox("Y-Axis (e.g. Permeability):", numeric_cols, index=numeric_cols.index(default_y), key="scat_y")
        
        color_by = st.selectbox("Color Data Points By:", ["None"] + (cat_cols if len(cat_cols) > 0 else []) + numeric_cols, index=1 if len(cat_cols) > 0 else 0)
        log_y = st.checkbox("Logarithmic Y-Axis (Recommended for Permeability)", value=(scat_y == "Permeability_mD"))

        fig_scatter = px.scatter(
            filtered_df,
            x=scat_x,
            y=scat_y,
            color=None if color_by == "None" else color_by,
            color_discrete_sequence=["#d4af37", "#3fb950", "#58a6ff", "#f85149"],
            hover_data=[col for col in filtered_df.columns if col in ["Sample_ID", "Depth_m"]],
            log_y=log_y,
            trendline="ols" if (len(filtered_df) > 3 and not log_y) else None,
            title=f"Crossplot: {scat_y} vs {scat_x}"
        )
        fig_scatter.update_traces(marker=dict(size=8, opacity=0.85, line=dict(width=1, color="#30363d")))
        fig_scatter.update_layout(
            **PLOTLY_DARK_LAYOUT,
            height=360,
            margin=dict(l=30, r=30, t=50, b=40)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # 4. Export Section
    st.divider()
    st.markdown('<div class="card-title">4. Dataset Export</div>', unsafe_allow_html=True)
    
    col_exp1, col_exp2 = st.columns([2, 1])
    with col_exp1:
        st.write(f"Export the dynamically filtered dataset ({len(filtered_df)} records) as a standard CSV.")
    with col_exp2:
        csv_filtered_buffer = io.StringIO()
        filtered_df.to_csv(csv_filtered_buffer, index=False)
        st.download_button(
            label="📥 Download Filtered CSV",
            data=csv_filtered_buffer.getvalue(),
            file_name="filtered_rock_fluid_data.csv",
            mime="text/csv",
            use_container_width=True
        )
