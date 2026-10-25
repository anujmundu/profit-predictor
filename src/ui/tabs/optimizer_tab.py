import streamlit as st
import pandas as pd

from src.config import format_currency
from src.optimizer import solve_optimal_budget
from src.ui.charts import plot_budget_donut

def render_optimizer_tab():
    """Renders the Inverse Goal-Seek Optimizer tab using SLSQP constrained optimization."""
    st.markdown("### 🎯 Inverse Goal-Seek: Prescriptive Budget Solver")
    st.caption("Tell the AI your profit target. The mathematical solver finds the exact capital allocation that minimizes total expenditure.")

    c_target, c_weights = st.columns([1.5, 2.5])

    with c_target:
        target_profit = st.number_input(
            "Target Net Profit (₹)",
            min_value=50000.0,
            max_value=350000.0,
            value=180000.0,
            step=10000.0,
            help="Desired quarterly profit milestone to achieve",
        )

    with c_weights:
        st.markdown("**Capital Allocation Constraints & Cost Weights**")
        w1, w2, w3 = st.columns(3)
        with w1:
            w_rnd = st.slider("R&D Weight / Cost", 0.5, 2.0, 1.0, 0.1, help="Higher weight penalizes high R&D spend")
        with w2:
            w_admin = st.slider("Admin Weight", 0.5, 2.0, 1.2, 0.1, help="Higher weight prioritizes lean administration")
        with w3:
            w_mktg = st.slider("Marketing Weight", 0.5, 2.0, 1.0, 0.1, help="Weight for advertising expenditure")

    with st.expander("⚙️ Advanced Departmental Budget Caps (Min / Max Bounds)", expanded=False):
        b1, b2, b3 = st.columns(3)
        with b1:
            min_rnd = st.number_input("Min R&D (₹)", 0.0, 100000.0, 30000.0, 5000.0)
            max_rnd = st.number_input("Max R&D (₹)", 100000.0, 400000.0, 250000.0, 10000.0)
        with b2:
            min_admin = st.number_input("Min Admin (₹)", 0.0, 80000.0, 40000.0, 5000.0)
            max_admin = st.number_input("Max Admin (₹)", 80000.0, 300000.0, 180000.0, 10000.0)
        with b3:
            min_mktg = st.number_input("Min Marketing (₹)", 0.0, 80000.0, 20000.0, 5000.0)
            max_mktg = st.number_input("Max Marketing (₹)", 80000.0, 500000.0, 350000.0, 10000.0)

    if st.button("⚡ Solve Optimal Budget Allocation", type="primary", width="stretch"):
        with st.spinner("Executing sequential quadratic programming (SLSQP) optimizer..."):
            res = solve_optimal_budget(
                target_profit=target_profit,
                min_rnd=min_rnd,
                max_rnd=max_rnd,
                min_admin=min_admin,
                max_admin=max_admin,
                min_mktg=min_mktg,
                max_mktg=max_mktg,
                weight_rnd=w_rnd,
                weight_admin=w_admin,
                weight_mktg=w_mktg,
            )

        if res["success"]:
            st.success(f"✅ Optimal Allocation Found! Achieved Predicted Profit: **{format_currency(res['achieved_profit'])}**")
        else:
            st.warning(f"⚠️ {res['message']}")

        # KPI Summary
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric("Target Profit", format_currency(res["target_profit"]))
        with k2:
            st.metric("Achieved Profit", format_currency(res["achieved_profit"]), delta=f"{format_currency(res['achieved_profit'] - res['target_profit'])}")
        with k3:
            st.metric("Total Optimal Budget", format_currency(res["total_budget"]), help="Minimum capital required")
        with k4:
            st.metric("ROI Multiplier", f"{res['roi_ratio']}x", help="Profit generated per rupee of spend")

        # Visualizations
        col_donut, col_details = st.columns([1.2, 1.8])

        with col_donut:
            alloc_dict = {
                "R&D Spend": res["optimal_rnd"],
                "Marketing Spend": res["optimal_marketing"],
                "Administration": res["optimal_admin"],
            }
            st.plotly_chart(plot_budget_donut(alloc_dict), width="stretch")

        with col_details:
            st.markdown("#### 📋 Recommended Departmental Budget Split")
            breakdown_df = pd.DataFrame([
                {
                    "Department": "Research & Development (R&D)",
                    "Recommended Spend": format_currency(res["optimal_rnd"]),
                    "Share of Budget": f"{res['allocation_pct']['R&D Spend']}%",
                    "Strategic Purpose": "Drives core product differentiation & long-term retention",
                },
                {
                    "Department": "Performance Marketing",
                    "Recommended Spend": format_currency(res["optimal_marketing"]),
                    "Share of Budget": f"{res['allocation_pct']['Marketing Spend']}%",
                    "Strategic Purpose": "Customer acquisition & revenue scaling",
                },
                {
                    "Department": "Administration Overhead",
                    "Recommended Spend": format_currency(res["optimal_admin"]),
                    "Share of Budget": f"{res['allocation_pct']['Administration']}%",
                    "Strategic Purpose": "Essential compliance, HR, and corporate governance",
                },
            ])
            st.dataframe(breakdown_df, hide_index=True, width="stretch")
