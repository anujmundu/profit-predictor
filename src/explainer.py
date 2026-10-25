import numpy as np
import pandas as pd
from typing import Dict, Any, List
import shap
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.config import CORE_FEATURES, format_currency
from models.registry import get_registry

class AIProfitExplainer:
    """Provides universal SHAP-based feature attributions and executive narratives across all 10 models."""

    def __init__(self):
        self.registry = get_registry()
        self._explainer = None
        self._cached_model_name = None
        self._bg_data = None

    def _get_background_data(self) -> np.ndarray:
        if self._bg_data is None:
            raw_path = Path(__file__).resolve().parent.parent / "data" / "raw" / "50_Startups.csv"
            if raw_path.exists():
                raw_df = pd.read_csv(raw_path)
                features_df = raw_df[CORE_FEATURES]
                scaled = self.registry.scaler.transform(features_df)
                self._bg_data = shap.sample(scaled, 15)
            else:
                self._bg_data = np.zeros((15, len(CORE_FEATURES)))
        return self._bg_data

    def _get_explainer(self):
        current_model_name = self.registry._active_model_name
        if self._cached_model_name == current_model_name and self._explainer is not None:
            return self._explainer

        model = self.registry.model
        model_cls_name = type(model).__name__

        # 1. Native TreeExplainer for decision tree / forest models only
        is_tree = any(t in model_cls_name for t in ["Forest", "Tree", "GradientBoosting", "XGB", "LGBM"])
        if is_tree:
            try:
                expl = shap.TreeExplainer(model)
                self._explainer = expl
                self._cached_model_name = current_model_name
                return expl
            except Exception:
                pass

        # 2. LinearExplainer for linear model family
        is_linear = any(l in model_cls_name for l in ["Ridge", "Lasso", "ElasticNet", "LinearRegression", "BayesianRidge"])
        if is_linear:
            try:
                bg = self._get_background_data()
                expl = shap.LinearExplainer(model, bg)
                self._explainer = expl
                self._cached_model_name = current_model_name
                return expl
            except Exception:
                pass

        # 3. Universal KernelExplainer for VotingRegressor, SVR, KNN, and other composite models
        try:
            bg = self._get_background_data()
            expl = shap.KernelExplainer(model.predict, bg)
            self._explainer = expl
            self._cached_model_name = current_model_name
            return expl
        except Exception:
            self._explainer = None
            self._cached_model_name = current_model_name
            return None

    def explain_instance(self, rnd: float, admin: float, marketing: float) -> Dict[str, Any]:
        """Calculates SHAP values for a single prediction with multi-model fallback."""
        input_df = pd.DataFrame([[rnd, admin, marketing]], columns=CORE_FEATURES)
        scaled_input = self.registry.scaler.transform(input_df)

        expl = self._get_explainer()
        shap_values = None
        base_val = None

        if expl is not None:
            try:
                raw_sv = expl.shap_values(scaled_input)
                if hasattr(raw_sv, "values"):
                    shap_values = np.ravel(raw_sv.values)
                elif isinstance(raw_sv, list):
                    shap_values = np.ravel(raw_sv[0])
                else:
                    shap_values = np.ravel(raw_sv)

                raw_ev = expl.expected_value
                if hasattr(raw_ev, "values"):
                    base_val = float(np.ravel(raw_ev.values)[0])
                elif isinstance(raw_ev, (list, np.ndarray)):
                    base_val = float(np.ravel(raw_ev)[0])
                else:
                    base_val = float(raw_ev)
            except Exception:
                shap_values = None

        # Robust Fallback: Model Perturbation Attribution if SHAP library encounters edge cases
        if shap_values is None or base_val is None:
            bg = self._get_background_data()
            bg_mean = bg.mean(axis=0)
            base_val = float(self.registry.model.predict(bg).mean())
            target_pred = float(self.registry.model.predict(scaled_input)[0])
            total_delta = target_pred - base_val

            pert_deltas = []
            for i in range(len(CORE_FEATURES)):
                cf = scaled_input.copy()
                cf[0, i] = bg_mean[i]
                cf_pred = float(self.registry.model.predict(cf)[0])
                pert_deltas.append(target_pred - cf_pred)

            sum_p = sum(abs(p) for p in pert_deltas)
            if sum_p > 0:
                shap_values = [p * (abs(total_delta) / sum_p) for p in pert_deltas]
            else:
                shap_values = [total_delta / len(CORE_FEATURES)] * len(CORE_FEATURES)

        attributions = []
        for feature, val, sv in zip(CORE_FEATURES, [rnd, admin, marketing], shap_values):
            attributions.append({
                "feature": feature,
                "input_value": val,
                "shap_value": float(sv),
                "impact": "Positive" if sv >= 0 else "Negative",
                "abs_impact": abs(float(sv)),
            })

        attributions = sorted(attributions, key=lambda x: x["abs_impact"], reverse=True)

        return {
            "base_value": base_val,
            "prediction": base_val + float(np.sum(shap_values)),
            "attributions": attributions,
        }

    def generate_narrative(
        self,
        predicted_profit: float,
        profit_delta_pct: float,
        revenue: float,
        revenue_delta_pct: float,
        cogs: float,
        rnd: float,
        mktg: float,
        admin: float,
        period: str = "Next Quarter",
    ) -> str:
        """Generates an executive-ready plain-language narrative explaining drivers and outlook."""
        direction = "expansion" if profit_delta_pct > 0 else ("contraction" if profit_delta_pct < 0 else "steady trajectory")
        trend_word = "strong tailwinds" if profit_delta_pct >= 10 else ("steady operational momentum" if profit_delta_pct >= 0 else "cyclical headwinds")

        # Key drivers
        top_driver = "R&D innovation" if rnd > mktg else "marketing campaign momentum"
        margin = (predicted_profit / revenue * 100) if revenue > 0 else 0.0
        qoq_phrase = f"({direction} of {abs(profit_delta_pct):.1f}% QoQ)" if profit_delta_pct != 0 else "(steady baseline performance)"

        narrative = (
            f"Executive Outlook for {period}: Net profit is projected at {format_currency(predicted_profit)} "
            f"{qoq_phrase}, reflecting {trend_word} across core operations. "
            f"Gross revenue is tracking at {format_currency(revenue)} ({'+' if revenue_delta_pct >= 0 else ''}{revenue_delta_pct:.1f}% QoQ) "
            f"with an operating margin of {margin:.1f}%. "
            f"The primary catalyst is strategic {top_driver}, supported by allocated budgets of {format_currency(rnd)} in R&D and {format_currency(mktg)} in Marketing.\n\n"
        )

        if profit_delta_pct < 0:
            narrative += (
                f"Risk Mitigation: Rising administrative overhead ({format_currency(admin)}) and supply-chain COGS "
                f"({format_currency(cogs)}) pose margin pressure. Recommended action: tighten non-strategic operational expenditure."
            )
        else:
            narrative += (
                f"Strategic Guidance: Capital efficiency remains high. Continued disciplined reinvestment into high-margin segments "
                f"is recommended to sustain long-term return on invested capital."
            )

        return narrative

def get_explainer() -> AIProfitExplainer:
    return AIProfitExplainer()
