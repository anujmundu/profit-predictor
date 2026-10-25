import streamlit as st
import pandas as pd

from src.config import format_currency
from src.monte_carlo import run_monte_carlo
from src.ui.charts import plot_monte_carlo_distribution

def render_risk_simulation_tab(current_revenue: float, current_cogs: float, current_profit: float):
    """Renders the 10,000-run Monte Carlo risk and Value-at-Risk (VaR) simulation tab."""
    st.markdown("### 🎲 10,000-Run Monte Carlo Risk & Value-at-Risk (VaR) Engine")
    st.caption("Stress test your financial plan across 10,000 randomized market futures with supply chain shocks and demand volatility.")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        demand_vol = st.slider("Demand Volatility (σ %)", 2.0, 25.0, 8.0, 0.5, help="Standard deviation of consumer demand shocks")
    with c2:
        cogs_inf = st.slider("Supply / COGS Inflation (σ %)", 1.0, 20.0, 5.0, 0.5, help="Volatility in raw materials and logistics")
    with c3:
        price_vol = st.slider("Price Elasticity Shock (σ %)", 0.5, 15.0, 3.0, 0.5, help="Realized pricing swings")
    with c4:
        target_board = st.number_input(
            "Board Target Profit (₹)",
            min_value=100000.0,
            max_value=5000000.0,
            value=float(max(150000.0, current_profit)),
            step=25000.0,
        )

    # Run Monte Carlo
    with st.spinner("Executing 10,000 vectorized stochastic iterations..."):
        mc_res = run_monte_carlo(
            base_revenue=current_revenue,
            base_cogs=current_cogs,
            demand_volatility_pct=demand_vol,
            cogs_inflation_pct=cogs_inf,
            price_volatility_pct=price_vol,
            target_profit=target_board,
            n_simulations=10000,
        )

    # KPI Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(
            "Value at Risk (VaR 95%)",
            format_currency(mc_res["var_95_level"]),
            help="95% confidence that profit will not fall below this floor",
            delta="Capital Protection Floor",
            delta_color="normal",
        )
    with m2:
        st.metric(
            "Expected Shortfall (CVaR)",
            format_currency(mc_res["cvar_95"]),
            help="Average profit in the worst 5% tail risk macro conditions",
            delta="Worst-Case Tail Risk",
            delta_color="inverse",
        )
    with m3:
        target_prob = mc_res["target_probability"]
        prob_color = "normal" if target_prob >= 70 else "inverse"
        st.metric(
            "Target Attainment Likelihood",
            f"{target_prob:.1f}%",
            delta="Board Milestone Confidence",
            delta_color=prob_color,
        )
    with m4:
        st.metric(
            "Expected Mean Profit",
            format_currency(mc_res["mean_profit"]),
            delta=f"Median: {format_currency(mc_res['median_profit'])}",
        )

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # Distribution Chart
    st.plotly_chart(
        plot_monte_carlo_distribution(
            mc_res["sim_profits"],
            target_profit=target_board,
            var_95=mc_res["var_95_level"],
        ),
        width="stretch",
    )

    # Executive Interpretation Box
    st.markdown(
        f"""
        <div style="background: rgba(30, 41, 59, 0.65); border: 1px solid rgba(99, 102, 241, 0.25); border-radius: 12px; padding: 1.1rem; margin-top: 1rem;">
            <h5 style="color: #A5B4FC; margin: 0 0 8px 0;">🛡️ CFO Risk & Resilience Briefing</h5>
            <p style="margin: 0; color: #CBD5E1; font-size: 0.9rem;">
                Under current macroeconomic volatility parameters (Demand σ={demand_vol}%, COGS σ={cogs_inf}%), there is a 
                <strong>{target_prob:.1f}% probability</strong> of meeting or beating the board milestone of 
                <strong>{format_currency(target_board)}</strong>. 
                With 95% statistical confidence, net profit will remain above <strong>{format_currency(mc_res['var_95_level'])}</strong>. 
                Downside loss deficit risk (P &lt; 0) is estimated at <strong>{mc_res['unprofitable_probability']:.1f}%</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
