import streamlit as st
import pandas as pd
from typing import Dict, Any

from src.config import format_currency
from src.ui.components import render_kpi_card, render_narrative_box
from src.ui.charts import plot_runway_depletion, plot_macro_stress_comparison
from src.liquidity_engine import get_liquidity_engine
from src.stress_tester import get_stress_tester

def render_stress_liquidity_tab(df: pd.DataFrame, current_kpis: Dict[str, Any]):
    """Renders Tab 9: Institutional Macroeconomic Stress-Testing and Cash Burn & Runway Cockpit."""
    st.markdown("### 🌍 Macroeconomic Stress & Liquidity Studio")
    st.caption("Evaluate cash burn dynamics, operational runway, SaaS Rule of 40 valuation health, and institutional CCAR-grade macro shocks.")

    sub_liquidity, sub_stress = st.tabs([
        "📉 Cash Burn, Runway & Rule of 40",
        "⚡ Macroeconomic Stress Simulator",
    ])

    liq_engine = get_liquidity_engine()
    stress_tester = get_stress_tester()

    # Base financial parameters from app context
    rev = current_kpis.get("revenue", 2500000.0)
    profit = current_kpis.get("profit", 500000.0)
    margin = current_kpis.get("margin_pct", 20.0)
    cogs = rev * (1.0 - (margin / 100.0)) * 0.4
    rnd = rev * 0.20
    admin = rev * 0.12
    mktg = rev * 0.24

    # ----------------------------------------------------
    # SUBTAB 1: CASH BURN, RUNWAY & RULE OF 40
    # ----------------------------------------------------
    with sub_liquidity:
        st.markdown("#### 📉 Cash Reserves, Burn Rate & Solvency Horizon")
        st.caption("Simulate liquidity depletion over 8 quarters and monitor the SaaS Rule of 40 valuation scorecard.")

        col_in1, col_in2, col_in3 = st.columns([1.5, 1.2, 1.2])
        with col_in1:
            starting_cash_lakhs = st.number_input(
                "Starting Cash Reserves (₹ Lakhs)",
                min_value=10.0,
                max_value=5000.0,
                value=250.0,
                step=25.0,
                help="Cash in bank at beginning of Q1 (e.g. ₹250 Lakhs = ₹2.50 Crores)",
            )
            starting_cash = starting_cash_lakhs * 1e5
        with col_in2:
            growth_rate = st.slider("Expected QoQ Revenue Growth", min_value=-0.10, max_value=0.30, value=0.06, step=0.01, format="%d%%")
        with col_in3:
            capex_pct = st.slider("CapEx / Reinvestment (% Rev)", min_value=0.01, max_value=0.15, value=0.04, step=0.01, format="%d%%")

        # Compute runway
        runway_res = liq_engine.compute_runway(
            starting_cash=starting_cash,
            quarterly_revenue=rev,
            quarterly_cogs=cogs,
            quarterly_rnd=rnd,
            quarterly_admin=admin,
            quarterly_mktg=mktg,
            revenue_growth_rate=growth_rate,
            capex_ratio=capex_pct,
        )

        # KPI Cards for Liquidity
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            burn_val = runway_res["q1_monthly_burn"]
            st.metric(
                "Q1 Net Monthly Burn",
                format_currency(burn_val) if burn_val > 0 else "Cash Positive",
                delta=f"-{format_currency(burn_val * 3)} / Qtr" if burn_val > 0 else "Profitable",
                delta_color="inverse" if burn_val > 0 else "normal",
            )
        with m2:
            rm = runway_res["runway_months"]
            rm_str = f"{rm:.1f} Months" if rm < 900 else "Infinite (>3 Yrs)"
            st.metric(
                "Cash Runway Horizon",
                rm_str,
                delta=runway_res["zero_cash_date_str"],
                delta_color="normal" if rm >= 18 else ("off" if rm >= 12 else "inverse"),
            )
        with m3:
            st.metric(
                "Zero Cash Date",
                runway_res["zero_cash_date_str"],
                delta=f"Quarter: {runway_res['zero_cash_quarter']}",
                delta_color="off",
            )
        with m4:
            # Rule of 40
            yoy_growth = growth_rate * 4 * 100  # annualized
            r40 = liq_engine.compute_rule_of_40(yoy_growth, margin)
            st.metric(
                "Rule of 40 Score",
                f"{r40['score']:.1f}%",
                delta=r40["badge"],
                delta_color="normal" if r40["score"] >= 40 else "inverse",
            )

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

        # Rule of 40 Banner
        r40_html = (
            f"<div style='padding: 1rem 1.2rem; border-radius: 12px; background: rgba(30, 41, 59, 0.7); "
            f"border: 1px solid {r40['color']}40; margin-bottom: 1.2rem; display: flex; justify-content: space-between; align-items: center;'>"
            f"<div>"
            f"<span style='font-size: 0.8rem; text-transform: uppercase; font-weight: 700; color: {r40['color']}; letter-spacing: 0.05em;'>{r40['tier']}</span>"
            f"<p style='margin: 4px 0 0 0; color: #E2E8F0; font-size: 0.92rem;'>{r40['description']}</p>"
            f"</div>"
            f"<div style='text-align: right;'>"
            f"<span style='font-size: 1.6rem; font-weight: 800; color: {r40['color']};'>{r40['score']:.1f}%</span><br>"
            f"<span style='font-size: 0.75rem; color: #94A3B8;'>Growth: {yoy_growth:.1f}% | Margin: {margin:.1f}%</span>"
            f"</div>"
            f"</div>"
        )
        st.markdown(r40_html, unsafe_allow_html=True)

        # Plot Runway Depletion
        st.plotly_chart(plot_runway_depletion(runway_res["timeline_df"]), width="stretch")

        # Multi-Quarter Ledger Table
        with st.expander("🔍 8-Quarter Projected Liquidity Ledger", expanded=False):
            disp_df = runway_res["timeline_df"].copy()
            for c in ["Revenue", "Total_Costs", "Operating_Profit", "Net_Cash_Flow", "Beginning_Cash", "Ending_Cash", "Quarterly_Burn", "Monthly_Burn"]:
                disp_df[c] = disp_df[c].apply(lambda x: format_currency(x, compact=False))
            st.dataframe(disp_df, hide_index=True, width="stretch")

    # ----------------------------------------------------
    # SUBTAB 2: MACROECONOMIC STRESS SIMULATOR
    # ----------------------------------------------------
    with sub_stress:
        st.markdown("#### ⚡ Institutional Macroeconomic Stress-Testing Suite")
        st.caption("Apply Federal Reserve / RBI macroeconomic stress scenarios and evaluate balance sheet shock absorption.")

        # Preset Selector
        preset_names = list(stress_tester.PRESETS.keys())
        selected_preset = st.selectbox("Select Macroeconomic Stress Scenario", options=preset_names, index=1)
        preset_cfg = stress_tester.PRESETS[selected_preset]
        st.info(f"💡 **Scenario Overview**: {preset_cfg['description']}")

        # Shock Levers
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            inf_cogs = st.slider("Inflation on COGS (%)", 0.0, 40.0, float(preset_cfg["inflation_cogs_pct"]), step=1.0)
        with col_s2:
            rate_bps = st.slider("Interest Rate Spike (bps)", 0, 800, int(preset_cfg["rate_hike_bps"]), step=50, help="100 bps = 1.0% cost of debt")
        with col_s3:
            cac_inf = st.slider("Marketing CAC Surge (%)", 0.0, 60.0, float(preset_cfg["cac_inflation_pct"]), step=2.0)
        with col_s4:
            demand_drop = st.slider("Demand Contraction (%)", 0.0, 40.0, float(preset_cfg["demand_contraction_pct"]), step=1.0)

        # Compute Stressed Outcome
        stress_res = stress_tester.apply_stress(
            base_revenue=rev,
            base_cogs=cogs,
            base_rnd=rnd,
            base_admin=admin,
            base_mktg=mktg,
            inflation_cogs_pct=inf_cogs,
            rate_hike_bps=rate_bps,
            cac_inflation_pct=cac_inf,
            demand_contraction_pct=demand_drop,
        )

        resilience = stress_res["resilience"]

        # Resilience Banner
        res_html = (
            f"<div style='padding: 1.1rem 1.3rem; border-radius: 12px; background: rgba(30, 41, 59, 0.7); "
            f"border: 1px solid {resilience['color']}40; margin: 1rem 0; display: flex; justify-content: space-between; align-items: center;'>"
            f"<div>"
            f"<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 4px;'>"
            f"<span style='font-size: 1.1rem;'>{resilience['badge']}</span>"
            f"<span style='font-size: 0.95rem; font-weight: 700; color: #F8FAFC;'>Institutional Resilience Rating: {resilience['tier']}</span>"
            f"</div>"
            f"<p style='margin: 0; color: #CBD5E1; font-size: 0.9rem;'>{resilience['diagnosis']}</p>"
            f"</div>"
            f"<div style='text-align: right;'>"
            f"<span style='font-size: 2.1rem; font-weight: 800; color: {resilience['color']};'>{resilience['score']} / 100</span><br>"
            f"<span style='font-size: 0.75rem; color: #94A3B8;'>CCAR Durability Index</span>"
            f"</div>"
            f"</div>"
        )
        st.markdown(res_html, unsafe_allow_html=True)

        # Stressed vs Baseline Delta Cards
        c_b1, c_b2, c_b3, c_b4 = st.columns(4)
        with c_b1:
            st_prof = stress_res["stressed"]["profit"]
            prof_diff = stress_res["deltas"]["profit_delta"]
            st.metric(
                "Stressed Net Profit",
                format_currency(st_prof),
                delta=f"{format_currency(prof_diff)} Under Stress",
                delta_color="normal" if prof_diff >= 0 else "inverse",
            )
        with c_b2:
            st_marg = stress_res["stressed"]["margin_pct"]
            marg_diff = stress_res["deltas"]["margin_delta"]
            st.metric(
                "Stressed Operating Margin",
                f"{st_marg:.1f}%",
                delta=f"{marg_diff:+.1f}% vs Nominal",
                delta_color="normal" if marg_diff >= 0 else "inverse",
            )
        with c_b3:
            rev_loss = stress_res["deltas"]["revenue_loss"]
            st.metric(
                "Demand Revenue Impact",
                format_currency(stress_res["stressed"]["revenue"]),
                delta=f"{format_currency(rev_loss)} Topline Hit",
                delta_color="inverse",
            )
        with c_b4:
            cost_hike = stress_res["deltas"]["cost_increase"]
            st.metric(
                "Inflation Cost Expansion",
                format_currency(stress_res["stressed"]["total_costs"]),
                delta=f"+{format_currency(cost_hike)} Opex Creep",
                delta_color="inverse",
            )

        # Plot Macro Comparison
        st.plotly_chart(
            plot_macro_stress_comparison(stress_res["baseline"], stress_res["stressed"]),
            width="stretch",
        )
