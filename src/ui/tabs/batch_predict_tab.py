import streamlit as st
import pandas as pd
import plotly.express as px

from src.config import CORE_FEATURES, format_currency
from src.data_loader import load_sample_batch_data
from models.registry import get_registry

def render_batch_predict_tab():
    """Renders single company expense prediction and high-performance batch CSV scoring."""
    registry = get_registry()

    tab_single, tab_batch = st.tabs(["🎯 Single Prediction Studio", "📂 Enterprise Batch CSV Scoring"])

    with tab_single:
        st.markdown("#### 🎯 Instant Company Expense Predictor")
        st.caption("Input budget allocations to evaluate the expected profit outcome with confidence intervals.")

        c1, c2, c3 = st.columns(3)
        with c1:
            rnd = st.number_input("R&D Spend (₹)", min_value=0, value=165000, step=5000, key="single_rnd")
        with c2:
            admin = st.number_input("Administration Overhead (₹)", min_value=0, value=135000, step=5000, key="single_admin")
        with c3:
            marketing = st.number_input("Marketing Spend (₹)", min_value=0, value=320000, step=5000, key="single_mktg")

        conf_level = st.select_slider("Confidence Level", options=[0.70, 0.80, 0.90, 0.95], value=0.80, format_func=lambda x: f"{int(x*100)}%")

        if st.button("🚀 Calculate Forecast", type="primary"):
            with st.spinner("Executing model inference with bootstrap uncertainty..."):
                res = registry.predict_single(rnd, admin, marketing, confidence_level=conf_level)

                st.success(f"### Projected Net Profit: {format_currency(res['predicted_profit'], compact=False)}")

                k1, k2, k3 = st.columns(3)
                with k1:
                    st.metric("Lower Bound", format_currency(res["lower_bound"], compact=False), delta=f"-{format_currency(res['margin_error'])}")
                with k2:
                    st.metric("Expected Profit", format_currency(res["predicted_profit"], compact=False))
                with k3:
                    st.metric("Upper Bound", format_currency(res["upper_bound"], compact=False), delta=f"+{format_currency(res['margin_error'])}")

                st.info(f"💡 **Uncertainty Range ({res['confidence_level']}% CI)**: The true net profit has an estimated {res['confidence_level']}% likelihood of landing between **{format_currency(res['lower_bound'])}** and **{format_currency(res['upper_bound'])}**.")

    with tab_batch:
        st.markdown("#### 📂 Batch Multi-Company Profit Scoring")
        st.caption("Upload a corporate expense CSV to predict profits, flag outliers, and download scored datasets.")

        col_upload, col_sample, col_bench = st.columns([2.2, 1, 1.2])
        with col_upload:
            uploaded_file = st.file_uploader("Upload Custom CSV File", type=["csv"], help=f"CSV must contain: {CORE_FEATURES}")
        with col_sample:
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            use_sample = st.button("Load 500 Sample", width="stretch")
        with col_bench:
            from src.data_loader import load_benchmark_catalog, load_benchmark_dataset
            cat = load_benchmark_catalog()
            bench_slugs = [c["slug"] for c in cat] if cat else []
            chosen_bench = st.selectbox("Or Benchmark Dataset", options=bench_slugs, index=0 if bench_slugs else None)
            load_bench = st.button(f"Load {chosen_bench}", width="stretch")

        batch_df = None
        if uploaded_file is not None:
            try:
                batch_df = pd.read_csv(uploaded_file)
            except Exception as e:
                st.error(f"Error reading CSV file: {e}")
        elif use_sample:
            batch_df = load_sample_batch_data()
        elif load_bench and chosen_bench:
            batch_df = load_benchmark_dataset(chosen_bench)


        if batch_df is not None:
            missing_cols = [c for c in CORE_FEATURES if c not in batch_df.columns]
            if missing_cols:
                st.error(f"Missing required columns: {missing_cols}. Expected columns: {CORE_FEATURES}")
            else:
                with st.spinner(f"Scoring {len(batch_df)} companies..."):
                    scored_df = registry.predict_batch(batch_df)

                st.markdown(f"**Evaluated Records**: {len(scored_df):,} companies")

                # Metrics
                avg_profit = scored_df["Predicted Profit"].mean()
                total_profit = scored_df["Predicted Profit"].sum()
                unprofitable = (scored_df["Predicted Profit"] < 0).sum()

                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Average Profit", format_currency(avg_profit))
                with m2:
                    st.metric("Aggregate Portfolio Profit", format_currency(total_profit))
                with m3:
                    st.metric("Unprofitable Flags", unprofitable, delta="High Risk" if unprofitable > 0 else "Optimal", delta_color="inverse")

                # Interactive Distribution Plot
                fig = px.histogram(
                    scored_df,
                    x="Predicted Profit",
                    nbins=30,
                    title="<b>Batch Profit Distribution</b>",
                    color_discrete_sequence=["#6366F1"],
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(30, 41, 59, 0.35)",
                    font=dict(family="Plus Jakarta Sans", color="#94A3B8"),
                    xaxis=dict(gridcolor="rgba(148, 163, 184, 0.08)"),
                    yaxis=dict(gridcolor="rgba(148, 163, 184, 0.08)"),
                )
                st.plotly_chart(fig, width="stretch")

                # Results Table
                st.markdown("#### Scored Dataset Preview")
                st.dataframe(scored_df.head(100), width="stretch", height=300)

                # Export CSV
                csv_bytes = scored_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Scored Predictions CSV",
                    data=csv_bytes,
                    file_name="scored_profit_predictions.csv",
                    mime="text/csv",
                    type="primary",
                )
