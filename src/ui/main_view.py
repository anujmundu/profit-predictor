import streamlit as st
import pandas as pd

from src.ui.styles import inject_custom_styles
from src.ui.components import render_header
from src.ui.tabs.dashboard_tab import render_dashboard_tab
from src.ui.tabs.scenario_lab_tab import render_scenario_lab_tab
from src.ui.tabs.explainability_tab import render_explainability_tab
from src.ui.tabs.batch_predict_tab import render_batch_predict_tab
from src.ui.tabs.model_health_tab import render_model_health_tab
from src.ui.tabs.optimizer_tab import render_optimizer_tab
from src.ui.tabs.risk_simulation_tab import render_risk_simulation_tab
from src.ui.tabs.sensitivity_tab import render_sensitivity_tab
from src.ui.tabs.stress_liquidity_tab import render_stress_liquidity_tab
from src.data_loader import load_enterprise_series
from src.financial_engine import get_engine
from src.copilot import get_cfo_copilot
from src.monte_carlo import run_monte_carlo
from src.report_generator import generate_boardroom_report_html
from src.config import format_currency

def run_app():
    """Main application runner orchestrating global filters, styles, AI Copilot, and modular tab views."""
    st.set_page_config(
        page_title="Enterprise Profit Intelligence & CFO Operating System",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_custom_styles()

    # Load enterprise multi-quarter series
    df_raw = load_enterprise_series()
    engine = get_engine()
    copilot = get_cfo_copilot()

    # Sidebar Global Controls
    with st.sidebar:
        st.markdown("### ⚙️ Global Filters")
        st.caption("Customize scope across enterprise dimensions")

        # Region Filter
        all_regions = sorted(df_raw["Region"].unique().tolist())
        selected_regions = st.multiselect(
            "Geographic Regions",
            options=all_regions,
            default=all_regions,
        )

        # Product Line Filter
        all_products = sorted(df_raw["Product"].unique().tolist())
        selected_products = st.multiselect(
            "Product Lines",
            options=all_products,
            default=all_products,
        )

        # Time Horizon
        min_year = int(df_raw["Year"].min())
        max_year = int(df_raw["Year"].max())
        year_range = st.slider("Time Horizon", min_value=min_year, max_value=max_year, value=(min_year, max_year))

        # 10-Model Architecture Selector
        from models.registry import get_registry
        from src.data_loader import load_benchmark_catalog
        registry = get_registry()
        avail_models = registry.get_available_models()
        default_model_idx = avail_models.index("Ensemble (Voting Meta-Model)") if "Ensemble (Voting Meta-Model)" in avail_models else 0
        selected_model = st.selectbox(
            "🧠 Active ML Architecture (10 Models)",
            options=avail_models,
            index=default_model_idx,
            help="Switch between 10 competing machine learning algorithms",
        )
        registry.set_active_model(selected_model)

        # 50-Sector Benchmark Selector
        catalog = load_benchmark_catalog()
        if catalog:
            sector_names = [f"{item['name']} ({item['super_sector']})" for item in catalog]
            selected_sector_str = st.selectbox(
                "🌐 Industry Benchmark (50+ Sectors)",
                options=sector_names,
                index=0,
                help="Calibrate expense ratios, CAC intensity, and margins to any of 50 global sectors",
            )
            from src.data_loader import get_benchmarks_zip_bytes
            st.download_button(
                label="📥 Download 50 Datasets (.ZIP)",
                data=get_benchmarks_zip_bytes(),
                file_name="50_industry_benchmark_datasets.zip",
                mime="application/zip",
                help="Download all 50 industry benchmark CSV datasets and catalog in one ZIP file",
                width="stretch"
            )

        st.markdown("---")
        st.markdown("### 🏢 Enterprise Profile")
        st.write("**Currency**: INR (₹ Lakhs/Crores)")
        st.write(f"**Sector**: {selected_sector_str.split(' (')[0] if catalog else 'B2B SaaS'}")
        st.write(f"**Active Model**: {selected_model}")
        st.write("**Reporting**: Multi-Quarter Ledger")
        st.caption("Platform: 10-Model Zoo & 50 Benchmarks Matrix")

    # Filter Dataset
    filtered_df = df_raw[
        (df_raw["Region"].isin(selected_regions)) &
        (df_raw["Product"].isin(selected_products)) &
        (df_raw["Year"] >= year_range[0]) &
        (df_raw["Year"] <= year_range[1])
    ]

    if filtered_df.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust the sidebar selections.")
        return

    # Compute baseline timeline & KPIs for app context
    timeline = engine.get_aggregated_timeline(filtered_df)
    kpis = engine.compute_kpis(timeline)
    forecast_rows = timeline[timeline["Is_Forecast"] == True]
    sample_fore = forecast_rows.iloc[0] if not forecast_rows.empty else timeline.iloc[-1]

    # Executive Header with Boardroom Export Button
    col_hdr, col_btn = st.columns([3.2, 1.2])
    with col_hdr:
        render_header(
            title="Enterprise Profit Intelligence & AI CFO Suite",
            subtitle="Autonomous financial decision-support: Prescriptive Optimization, 10,000 Monte Carlo simulations, and driver attribution",
            badge="Autonomous AI CFO OS",
        )
    with col_btn:
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        # Quick Boardroom report generator
        mc_quick = run_monte_carlo(
            base_revenue=kpis["revenue"],
            base_cogs=sample_fore["COGS"],
            target_profit=kpis["profit"],
            n_simulations=1000,
        )
        report_html = generate_boardroom_report_html(
            kpis=kpis,
            monte_carlo_res=mc_quick,
            narrative_text=f"Projected net profit for {kpis['period']} is {kpis['profit']:,.0f} ({kpis['profit_delta_pct']:+.1f}% QoQ).",
        )
        st.download_button(
            label="📄 Export Boardroom Memorandum",
            data=report_html,
            file_name="CFO_Boardroom_Briefing.html",
            mime="text/html",
            width="stretch",
            type="primary",
        )

    # 🧠 Embedded AI CFO Copilot Assistant
    with st.expander("💬 Autonomous AI CFO Copilot & 3-Agent Boardroom Deliberation", expanded=False):
        c_in, c_mode, c_act = st.columns([3.0, 1.2, 0.8])
        with c_in:
            copilot_query = st.text_input(
                "Ask your AI CFO a question or scenario",
                placeholder="e.g., 'How can we achieve ₹25L profit next quarter?' or 'Simulate a 10% drop in demand with 5% inflation'",
            )
        with c_mode:
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            boardroom_mode = st.checkbox("🏛️ 3-Agent Debate", value=False, help="Enable multi-agent debate between Comptroller, CRO, and Chief Strategist.")
        with c_act:
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            ask_btn = st.button("Consult CFO", width="stretch")

        if ask_btn and copilot_query:
            if boardroom_mode:
                delib = copilot.deliberate_boardroom(copilot_query, kpis)
                st.markdown(f"#### 🏛️ Boardroom Deliberation Committee: Target {format_currency(delib['target_amount'])}")
                cd1, cd2 = st.columns(2)
                with cd1:
                    st.info(delib["comptroller_stance"])
                with cd2:
                    st.warning(delib["cro_stance"])
                st.success(delib["consensus_stance"])
            else:
                copilot_res = copilot.process_query(copilot_query, kpis)
                st.markdown(copilot_res["response"])

    # 9 Modular High-Impact Tabs
    tabs = st.tabs([
        "📊 Executive Overview",
        "🎯 Goal-Seek Optimizer",
        "🎲 Monte Carlo Risk (VaR)",
        "🌪️ Sensitivity & Frontiers",
        "🧪 Scenario Lab",
        "🔮 SHAP Explainability",
        "📂 Batch Scoring Studio",
        "🛡️ Model Governance",
        "🌍 Macro Stress & Liquidity",
    ])

    with tabs[0]:
        try:
            render_dashboard_tab(filtered_df)
        except Exception as e:
            st.error(f"Error loading Executive Overview: {e}")

    with tabs[1]:
        try:
            render_optimizer_tab()
        except Exception as e:
            st.error(f"Error loading Goal-Seek Optimizer: {e}")

    with tabs[2]:
        try:
            render_risk_simulation_tab(
                current_revenue=kpis["revenue"],
                current_cogs=sample_fore["COGS"],
                current_profit=kpis["profit"],
            )
        except Exception as e:
            st.error(f"Error loading Risk Simulation: {e}")

    with tabs[3]:
        try:
            render_sensitivity_tab(
                base_revenue=kpis["revenue"],
                base_cogs=sample_fore["COGS"],
                base_rnd=sample_fore["R&D Spend"],
                base_mktg=sample_fore["Marketing Spend"],
                base_admin=sample_fore["Administration"],
            )
        except Exception as e:
            st.error(f"Error loading Sensitivity Analysis: {e}")

    with tabs[4]:
        try:
            render_scenario_lab_tab(filtered_df)
        except Exception as e:
            st.error(f"Error loading Scenario Lab: {e}")

    with tabs[5]:
        try:
            render_explainability_tab()
        except Exception as e:
            st.error(f"Error loading SHAP Explainability: {e}")

    with tabs[6]:
        try:
            render_batch_predict_tab()
        except Exception as e:
            st.error(f"Error loading Batch Scoring Studio: {e}")

    with tabs[7]:
        try:
            render_model_health_tab()
        except Exception as e:
            st.error(f"Error loading Model Governance: {e}")

    with tabs[8]:
        try:
            render_stress_liquidity_tab(filtered_df, kpis)
        except Exception as e:
            st.error(f"Error loading Macro Stress & Liquidity Studio: {e}")
