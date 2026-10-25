import streamlit as st
import pandas as pd

from src.config import format_currency
from src.explainer import get_explainer
from src.ui.charts import plot_shap_attributions
from models.registry import get_registry

def render_explainability_tab():
    """Renders SHAP explainability, feature attribution, and natural language diagnostic tools."""
    st.markdown("### 🔮 Model Explainability & Feature Attribution (SHAP)")
    st.caption("Understand the exact mathematical rationale behind any predicted profit figure via Shapley values.")

    explainer = get_explainer()
    registry = get_registry()

    c1, c2, c3 = st.columns(3)
    with c1:
        rnd = st.number_input("R&D Spend (₹)", min_value=0, max_value=500000, value=150000, step=5000)
    with c2:
        admin = st.number_input("Administration Cost (₹)", min_value=0, max_value=500000, value=120000, step=5000)
    with c3:
        marketing = st.number_input("Marketing Spend (₹)", min_value=0, max_value=800000, value=250000, step=5000)

    # Calculate SHAP breakdown
    explanation = explainer.explain_instance(rnd, admin, marketing)

    base_val = explanation["base_value"]
    pred_val = explanation["prediction"]
    attributions = explanation["attributions"]

    # Metrics Row
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Base Population Average", format_currency(base_val), help="Average profit across historical baseline")
    with m2:
        st.metric("Model Prediction", format_currency(pred_val), delta=f"{format_currency(pred_val - base_val)} from baseline")
    with m3:
        top_feat = attributions[0]
        st.metric("Primary Driver", top_feat["feature"], delta=f"{top_feat['impact']} impact ({format_currency(top_feat['shap_value'])})")

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # SHAP Plot
    st.plotly_chart(plot_shap_attributions(attributions), width="stretch")

    # Plain English Breakdown
    st.markdown("#### 💬 Plain-Language Driver Decomposition")
    reasons = []
    for a in attributions:
        direction = "lifted" if a["shap_value"] >= 0 else "reduced"
        reasons.append(f"- **{a['feature']}** ({format_currency(a['input_value'])}): {direction} projected profit by **{format_currency(abs(a['shap_value']))}** compared to baseline expectations.")

    st.markdown("\n".join(reasons))

    # Global Feature Importance from Registry
    with st.expander("🌐 Global Model Feature Importance (All Startups)", expanded=False):
        meta = registry.metadata
        if "feature_importances" in meta:
            feat_imp = meta["feature_importances"]
            imp_df = pd.DataFrame([
                {"Feature": k, "Relative Importance": f"{v*100:.1f}%", "Weight": v}
                for k, v in feat_imp.items()
            ]).sort_values("Weight", ascending=False)
            st.dataframe(imp_df[["Feature", "Relative Importance"]], hide_index=True, width="stretch")
