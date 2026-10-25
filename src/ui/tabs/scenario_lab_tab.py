import streamlit as st
import pandas as pd

from src.config import format_currency
from src.ui.charts import plot_scenario_comparison, plot_waterfall_drivers
from src.financial_engine import get_engine

@st.fragment
def render_scenario_lab_fragment(timeline: pd.DataFrame):
    """
    Isolated Streamlit fragment for reactive What-If scenario planning.
    Adjusting sliders executes in sub-50ms without reloading the overall page!
    """
    engine = get_engine()

    st.markdown("#### 🎛️ What-If Scenario Levers")
    st.caption("Manipulate business levers below. Notice how the forecast curves and metrics recalculate instantly.")

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        price_change = st.slider("Price Adjustment (%)", min_value=-20.0, max_value=20.0, value=2.0, step=0.5)
    with c2:
        vol_change = st.slider("Demand Volume (%)", min_value=-25.0, max_value=25.0, value=5.0, step=0.5)
    with c3:
        cogs_change = st.slider("COGS / Supply Cost (%)", min_value=-20.0, max_value=20.0, value=-2.0, step=0.5)
    with c4:
        mktg_change = st.slider("Marketing Spend (%)", min_value=-30.0, max_value=50.0, value=10.0, step=1.0)
    with c5:
        rnd_change = st.slider("R&D Allocation (%)", min_value=-30.0, max_value=50.0, value=8.0, step=1.0)

    # Compute scenario simulations
    scenarios = engine.simulate_scenarios(
        timeline=timeline,
        price_change_pct=price_change,
        volume_change_pct=vol_change,
        cogs_change_pct=cogs_change,
        marketing_change_pct=mktg_change,
        rnd_change_pct=rnd_change,
    )

    # Plot multi-scenario comparison
    st.plotly_chart(plot_scenario_comparison(scenarios), width="stretch")

    # Scenario Summary Comparison Table
    st.markdown("#### 📋 Scenario Comparison Matrix (2026 Forecast Aggregate)")
    summary_rows = []
    for s_name, s_df in scenarios.items():
        fore_part = s_df[s_df["Is_Forecast"] == True]
        tot_rev = fore_part["Revenue"].sum()
        tot_cogs = fore_part["COGS"].sum()
        tot_rnd = fore_part["R&D Spend"].sum()
        tot_mktg = fore_part["Marketing Spend"].sum()
        tot_profit = fore_part["Profit"].sum()
        margin = (tot_profit / tot_rev * 100) if tot_rev > 0 else 0.0

        summary_rows.append({
            "Scenario": s_name,
            "Total Projected Revenue": format_currency(tot_rev),
            "COGS": format_currency(tot_cogs),
            "R&D Spend": format_currency(tot_rnd),
            "Marketing Spend": format_currency(tot_mktg),
            "Projected Profit": format_currency(tot_profit),
            "Net Margin %": f"{margin:.2f}%",
        })

    summary_df = pd.DataFrame(summary_rows)
    st.dataframe(summary_df, width="stretch", hide_index=True)

    # Custom Scenario Waterfall Driver
    fore_custom = scenarios["Custom"][scenarios["Custom"]["Is_Forecast"] == True]
    fore_base = scenarios["Baseline"][scenarios["Baseline"]["Is_Forecast"] == True]
    if not fore_custom.empty and not fore_base.empty:
        drivers = engine.compute_waterfall_drivers(fore_base.iloc[0], fore_custom.iloc[0])
        st.markdown("#### 🌊 Custom Scenario vs Baseline Bridge (Next Quarter)")
        st.plotly_chart(plot_waterfall_drivers(drivers), width="stretch")

def render_scenario_lab_tab(df: pd.DataFrame):
    """Renders the Scenario Lab tab delegating to the interactive fragment."""
    engine = get_engine()
    timeline = engine.get_aggregated_timeline(df)
    render_scenario_lab_fragment(timeline)
