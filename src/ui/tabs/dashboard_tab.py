import streamlit as st
import pandas as pd
from typing import Dict, Any

from src.config import format_currency
from src.ui.components import render_kpi_card, render_narrative_box
from src.ui.charts import plot_forecast_trend, plot_margin_trend, plot_waterfall_drivers
from src.financial_engine import get_engine
from src.explainer import get_explainer

def render_dashboard_tab(df: pd.DataFrame):
    """Renders the executive dashboard with KPIs, narrative brief, core charts, and drill-down."""
    engine = get_engine()
    explainer = get_explainer()

    # Aggregate timeline based on sidebar filters
    timeline = engine.get_aggregated_timeline(df)
    kpis = engine.compute_kpis(timeline)

    # 1. Top KPI Summary Row (4 cards in responsive columns)
    st.markdown("### 📌 Executive KPI Summary")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        render_kpi_card(
            title=f"Predicted Profit ({kpis['period']})",
            value=format_currency(kpis["profit"]),
            delta_str=f"{abs(kpis['profit_delta_pct']):.1f}% QoQ",
            is_positive=kpis["profit_delta_pct"] >= 0,
            subtitle="Next Forecast Period",
            ci_str=f"± {format_currency(kpis['profit_ci_delta'])} (80% CI)",
            icon="💰"
        )

    with c2:
        render_kpi_card(
            title="Projected Revenue",
            value=format_currency(kpis["revenue"]),
            delta_str=f"{abs(kpis['revenue_delta_pct']):.1f}% QoQ",
            is_positive=kpis["revenue_delta_pct"] >= 0,
            subtitle="Topline Expansion",
            icon="📈"
        )

    with c3:
        render_kpi_card(
            title="Projected Total Costs",
            value=format_currency(kpis["costs"]),
            delta_str=f"{abs(kpis['costs_delta_pct']):.1f}% QoQ",
            is_positive=kpis["costs_delta_pct"] <= 0,  # lower cost is positive
            subtitle="COGS + R&D + Mktg + Admin",
            icon="📊"
        )

    with c4:
        render_kpi_card(
            title="Operating Margin %",
            value=f"{kpis['margin_pct']:.1f}%",
            delta_str=f"{abs(kpis['margin_delta_bps']):.0f} bps",
            is_positive=kpis["margin_delta_bps"] >= 0,
            subtitle="Target: >25.0%",
            icon="🎯"
        )

    st.markdown("<div style='margin-top: 1.2rem;'></div>", unsafe_allow_html=True)

    # 2. AI Executive Narrative Brief
    forecast_rows = timeline[timeline["Is_Forecast"] == True]
    sample_fore = forecast_rows.iloc[0] if not forecast_rows.empty else timeline.iloc[-1]

    narrative = explainer.generate_narrative(
        predicted_profit=kpis["profit"],
        profit_delta_pct=kpis["profit_delta_pct"],
        revenue=kpis["revenue"],
        revenue_delta_pct=kpis["revenue_delta_pct"],
        cogs=sample_fore["COGS"],
        rnd=sample_fore["R&D Spend"],
        mktg=sample_fore["Marketing Spend"],
        admin=sample_fore["Administration"],
        period=kpis["period"],
    )
    render_narrative_box(narrative)

    # 3. Primary Visualizations
    col_left, col_right = st.columns([1.55, 1.1])

    with col_left:
        st.plotly_chart(plot_forecast_trend(timeline), width="stretch")

    with col_right:
        st.plotly_chart(plot_margin_trend(timeline), width="stretch")

    # 4. Driver Waterfall for Next Period
    hist_rows = timeline[timeline["Is_Forecast"] == False]
    last_hist = hist_rows.iloc[-1] if not hist_rows.empty else sample_fore

    drivers = engine.compute_waterfall_drivers(last_hist, sample_fore)
    st.plotly_chart(plot_waterfall_drivers(drivers), width="stretch")

    # 5. Detail and Drill-Down Matrix
    with st.expander("🔍 Detailed Multi-Segment Financial Ledger (Actuals vs Predictions)", expanded=False):
        st.markdown("Filter, sort, and inspect historical performance and forward-looking predictions by region and product.")
        display_df = df.copy()
        # Formatted columns for display
        for col in ["Revenue", "COGS", "R&D Spend", "Marketing Spend", "Administration", "Profit", "CI_Lower", "CI_Upper"]:
            display_df[col] = display_df[col].apply(lambda x: f"₹{x:,.2f}")
        display_df["Margin_Pct"] = display_df["Margin_Pct"].apply(lambda x: f"{x:.2f}%")
        st.dataframe(display_df, width="stretch", height=350)
