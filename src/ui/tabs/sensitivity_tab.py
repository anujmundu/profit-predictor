import streamlit as st
import pandas as pd

from src.config import format_currency
from src.sensitivity import get_sensitivity_engine
from src.ui.charts import plot_tornado_sensitivity, plot_profit_contour_surface

def render_sensitivity_tab(base_revenue: float, base_cogs: float, base_rnd: float, base_mktg: float, base_admin: float):
    """Renders the Tornado Sensitivity analysis and 2D Profit Frontier Sweet Spot contour."""
    st.markdown("### 🌪️ Sensitivity Tornado & 2D Elasticity Frontier")
    st.caption("Identify which levers create the highest bottom-line leverage and uncover the optimal capital allocation sweet spot.")

    engine = get_sensitivity_engine()

    tab_tornado, tab_contour = st.tabs(["🌪️ Driver Sensitivity Tornado", "🗺️ 2D Profit Frontier Sweet Spot"])

    with tab_tornado:
        c1, c2 = st.columns([1.5, 3.5])
        with c1:
            swing_pct = st.slider("Lever Stress Swing (± %)", min_value=2.0, max_value=25.0, value=10.0, step=1.0)
            st.info(
                f"**Elasticity Insight**: The tornado chart ranks drivers by profit volatility when shocked by ±{swing_pct}%. "
                "The widest bars represent your highest-leverage management decisions."
            )

        with c2:
            tornado_data = engine.compute_tornado(
                base_revenue=base_revenue,
                base_cogs=base_cogs,
                base_rnd=base_rnd,
                base_mktg=base_mktg,
                base_admin=base_admin,
                swing_pct=swing_pct,
            )
            st.plotly_chart(plot_tornado_sensitivity(tornado_data), width="stretch")

        # Ranked Breakdown Table
        st.markdown("#### 📋 Elasticity Leverage Leaderboard")
        rank_df = pd.DataFrame([
            {
                "Rank": f"#{idx+1}",
                "Business Driver": d["lever"],
                "Downside Impact (-10%)": format_currency(d["low_delta"]),
                "Upside Impact (+10%)": format_currency(d["high_delta"]),
                "Total Profit Swing": format_currency(d["swing"]),
            }
            for idx, d in enumerate(tornado_data)
        ])
        st.dataframe(rank_df, hide_index=True, width="stretch")

    with tab_contour:
        st.markdown("#### 🗺️ 2D Capital Efficiency Surface (Marketing vs R&D)")
        st.caption("Interactive contour map discovering the maximum profit sweet spot and diagnosing diminishing marginal returns.")

        col_ctrl, col_plot = st.columns([1.2, 2.8])
        with col_ctrl:
            admin_spend = st.number_input("Fixed Administration Baseline (₹)", min_value=30000.0, max_value=250000.0, value=120000.0, step=10000.0)
            st.markdown(
                """
                <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px; font-size: 0.85rem; color: #94A3B8;">
                    <strong style="color: #F8FAFC;">💡 Diminishing Returns Warning:</strong><br>
                    Notice how excessive marketing spend without matching R&D innovation causes profit contours to flatten. 
                    The red star marks the <strong>Profit Maximization Frontier</strong>.
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_plot:
            with st.spinner("Generating 2D multi-variable prediction grid..."):
                surface_data = engine.compute_profit_surface(admin_spend=admin_spend)

            st.plotly_chart(
                plot_profit_contour_surface(
                    mktg_vals=surface_data["mktg_vals"],
                    rnd_vals=surface_data["rnd_vals"],
                    profit_grid=surface_data["profit_grid"],
                    sweet_spot=surface_data["sweet_spot"],
                ),
                width="stretch",
            )

        # Sweet spot metric row
        sp = surface_data["sweet_spot"]
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.metric("Optimal R&D Allocation", format_currency(sp["rnd_spend"]))
        with s2:
            st.metric("Optimal Marketing Spend", format_currency(sp["marketing_spend"]))
        with s3:
            st.metric("Fixed Admin Overhead", format_currency(sp["admin_spend"]))
        with s4:
            st.metric("Peak Achievable Profit", format_currency(sp["max_profit"]), delta="★ Sweet Spot Peak", delta_color="normal")
