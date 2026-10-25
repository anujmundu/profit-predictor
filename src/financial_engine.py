import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.config import ENTERPRISE_DATA_PATH, DATA_PROCESSED_DIR

class FinancialEngine:
    """Enterprise financial planning, time-series forecasting, and scenario simulation engine."""

    def __init__(self):
        self._ensure_dataset_exists()

    def _ensure_dataset_exists(self):
        """Generates realistic multi-quarter historical and baseline forecast data if not present."""
        if ENTERPRISE_DATA_PATH.exists():
            return

        DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        np.random.seed(42)

        quarters = [
            # Historical (2022 Q1 - 2025 Q4: 16 quarters)
            "2022-Q1", "2022-Q2", "2022-Q3", "2022-Q4",
            "2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4",
            "2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4",
            "2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4",
            # Forecast (2026 Q1 - 2026 Q4: 4 quarters)
            "2026-Q1", "2026-Q2", "2026-Q3", "2026-Q4",
        ]

        regions = ["North America", "Europe", "Asia-Pacific"]
        products = ["Enterprise SaaS", "Cloud AI Services", "Edge Hardware"]

        records = []
        base_revenues = {
            "Enterprise SaaS": 1800000,
            "Cloud AI Services": 1200000,
            "Edge Hardware": 800000,
        }

        growth_trend = np.linspace(1.0, 1.65, len(quarters))

        for q_idx, quarter in enumerate(quarters):
            is_forecast = "2026" in quarter
            q_factor = growth_trend[q_idx]

            for reg in regions:
                reg_weight = 1.2 if reg == "North America" else (0.9 if reg == "Europe" else 0.8)
                for prod in products:
                    noise = np.random.normal(0, 0.04)
                    rev = base_revenues[prod] * q_factor * reg_weight * (1 + noise)

                    # Cost structure
                    cogs_ratio = 0.35 if prod != "Edge Hardware" else 0.52
                    cogs = rev * cogs_ratio * (1 + np.random.normal(0, 0.02))

                    rnd_ratio = 0.18 if prod == "Cloud AI Services" else 0.12
                    rnd = rev * rnd_ratio * (1 + np.random.normal(0, 0.03))

                    mktg_ratio = 0.14
                    mktg = rev * mktg_ratio * (1 + np.random.normal(0, 0.03))

                    admin_ratio = 0.08
                    admin = rev * admin_ratio * (1 + np.random.normal(0, 0.02))

                    total_costs = cogs + rnd + mktg + admin
                    profit = rev - total_costs
                    margin_pct = (profit / rev) * 100.0

                    # Uncertainty bounds (wider in forecast)
                    uncertainty_factor = 0.04 if not is_forecast else (0.07 + (q_idx - 16) * 0.02)
                    ci_lower = profit * (1.0 - uncertainty_factor)
                    ci_upper = profit * (1.0 + uncertainty_factor)

                    records.append({
                        "Quarter": quarter,
                        "Year": int(quarter.split("-")[0]),
                        "Period": quarter.split("-")[1],
                        "Region": reg,
                        "Product": prod,
                        "Is_Forecast": is_forecast,
                        "Revenue": round(rev, 2),
                        "COGS": round(cogs, 2),
                        "R&D Spend": round(rnd, 2),
                        "Marketing Spend": round(mktg, 2),
                        "Administration": round(admin, 2),
                        "Total Costs": round(total_costs, 2),
                        "Profit": round(profit, 2),
                        "Margin_Pct": round(margin_pct, 2),
                        "CI_Lower": round(ci_lower, 2),
                        "CI_Upper": round(ci_upper, 2),
                    })

        df = pd.DataFrame(records)
        df.to_csv(ENTERPRISE_DATA_PATH, index=False)

    def load_data(self) -> pd.DataFrame:
        """Loads enterprise financial series data."""
        self._ensure_dataset_exists()
        return pd.read_csv(ENTERPRISE_DATA_PATH)

    def get_aggregated_timeline(self, df_filtered: pd.DataFrame) -> pd.DataFrame:
        """Aggregates timeline by quarter with confidence intervals and margin %."""
        agg = df_filtered.groupby("Quarter", as_index=False).agg({
            "Revenue": "sum",
            "COGS": "sum",
            "R&D Spend": "sum",
            "Marketing Spend": "sum",
            "Administration": "sum",
            "Total Costs": "sum",
            "Profit": "sum",
            "CI_Lower": "sum",
            "CI_Upper": "sum",
            "Is_Forecast": "first",
        })
        agg["Margin_Pct"] = (agg["Profit"] / agg["Revenue"]) * 100.0
        # Sort chronologically
        agg["SortKey"] = agg["Quarter"].apply(lambda q: (int(q.split("-")[0]) * 10) + int(q.split("-Q")[1]))
        agg = agg.sort_values("SortKey").drop(columns=["SortKey"]).reset_index(drop=True)
        return agg

    def compute_kpis(self, timeline: pd.DataFrame) -> Dict[str, Any]:
        """Calculates executive KPI metrics for the next period vs previous period."""
        # Find next forecast quarter and last historical quarter
        forecast_mask = timeline["Is_Forecast"] == True
        hist_mask = timeline["Is_Forecast"] == False

        forecast_rows = timeline[forecast_mask]
        hist_rows = timeline[hist_mask]

        if not forecast_rows.empty:
            next_row = forecast_rows.iloc[0]
            last_hist_row = hist_rows.iloc[-1] if not hist_rows.empty else next_row
        else:
            next_row = timeline.iloc[-1]
            last_hist_row = timeline.iloc[-2] if len(timeline) > 1 else next_row

        profit_val = next_row["Profit"]
        profit_ci_delta = (next_row["CI_Upper"] - next_row["CI_Lower"]) / 2.0
        rev_val = next_row["Revenue"]
        costs_val = next_row["Total Costs"]
        margin_pct = next_row["Margin_Pct"]

        # Trends
        prev_profit = last_hist_row["Profit"]
        profit_delta_pct = ((profit_val - prev_profit) / abs(prev_profit) * 100) if prev_profit != 0 else 0.0

        prev_rev = last_hist_row["Revenue"]
        rev_delta_pct = ((rev_val - prev_rev) / abs(prev_rev) * 100) if prev_rev != 0 else 0.0

        prev_costs = last_hist_row["Total Costs"]
        costs_delta_pct = ((costs_val - prev_costs) / abs(prev_costs) * 100) if prev_costs != 0 else 0.0

        prev_margin = last_hist_row["Margin_Pct"]
        margin_delta_bps = (margin_pct - prev_margin) * 100  # basis points

        return {
            "period": next_row["Quarter"],
            "profit": profit_val,
            "profit_ci_delta": profit_ci_delta,
            "profit_delta_pct": profit_delta_pct,
            "revenue": rev_val,
            "revenue_delta_pct": rev_delta_pct,
            "costs": costs_val,
            "costs_delta_pct": costs_delta_pct,
            "margin_pct": margin_pct,
            "margin_delta_bps": margin_delta_bps,
        }

    def simulate_scenarios(
        self,
        timeline: pd.DataFrame,
        price_change_pct: float = 0.0,
        volume_change_pct: float = 0.0,
        cogs_change_pct: float = 0.0,
        marketing_change_pct: float = 0.0,
        rnd_change_pct: float = 0.0,
    ) -> Dict[str, pd.DataFrame]:
        """
        Simulates:
        - Baseline (no change)
        - Custom User Scenario (user sliders)
        - Optimistic (+10% volume, +5% price, -4% cogs, +15% mktg)
        - Pessimistic (-8% volume, -3% price, +6% cogs, -10% mktg)
        """
        def apply_deltas(df: pd.DataFrame, dp: float, dv: float, dc: float, dm: float, dr: float) -> pd.DataFrame:
            res = df.copy()
            # Revenue = Base Revenue * (1 + price_change) * (1 + volume_change)
            rev_factor = (1.0 + dp / 100.0) * (1.0 + dv / 100.0)
            res["Revenue"] = res["Revenue"] * rev_factor
            # COGS scales with volume and cost change
            res["COGS"] = res["COGS"] * (1.0 + dv / 100.0) * (1.0 + dc / 100.0)
            res["Marketing Spend"] = res["Marketing Spend"] * (1.0 + dm / 100.0)
            res["R&D Spend"] = res["R&D Spend"] * (1.0 + dr / 100.0)
            res["Total Costs"] = res["COGS"] + res["Marketing Spend"] + res["R&D Spend"] + res["Administration"]
            res["Profit"] = res["Revenue"] - res["Total Costs"]
            res["Margin_Pct"] = (res["Profit"] / res["Revenue"]) * 100.0
            return res

        forecast_mask = timeline["Is_Forecast"] == True
        hist_timeline = timeline[~forecast_mask]
        fore_timeline = timeline[forecast_mask]

        # Scenarios applied to forecast portion only
        custom_fore = apply_deltas(
            fore_timeline, price_change_pct, volume_change_pct, cogs_change_pct, marketing_change_pct, rnd_change_pct
        )
        optimistic_fore = apply_deltas(fore_timeline, 5.0, 10.0, -4.0, 15.0, 10.0)
        pessimistic_fore = apply_deltas(fore_timeline, -3.0, -8.0, 6.0, -10.0, -5.0)

        custom_df = pd.concat([hist_timeline, custom_fore]).reset_index(drop=True)
        optimistic_df = pd.concat([hist_timeline, optimistic_fore]).reset_index(drop=True)
        pessimistic_df = pd.concat([hist_timeline, pessimistic_fore]).reset_index(drop=True)

        return {
            "Baseline": timeline,
            "Custom": custom_df,
            "Optimistic": optimistic_df,
            "Pessimistic": pessimistic_df,
        }

    def compute_waterfall_drivers(
        self, baseline_row: pd.Series, scenario_row: pd.Series
    ) -> List[Dict[str, Any]]:
        """Calculates waterfall bridge from Baseline Profit to Scenario Profit."""
        base_profit = baseline_row["Profit"]
        target_profit = scenario_row["Profit"]

        rev_impact = scenario_row["Revenue"] - baseline_row["Revenue"]
        cogs_impact = -(scenario_row["COGS"] - baseline_row["COGS"])
        rnd_impact = -(scenario_row["R&D Spend"] - baseline_row["R&D Spend"])
        mktg_impact = -(scenario_row["Marketing Spend"] - baseline_row["Marketing Spend"])
        admin_impact = -(scenario_row["Administration"] - baseline_row["Administration"])

        drivers = [
            {"label": "Baseline Profit", "value": round(base_profit, 2), "type": "total"},
            {"label": "Revenue Delta", "value": round(rev_impact, 2), "type": "relative"},
            {"label": "COGS Efficiencies", "value": round(cogs_impact, 2), "type": "relative"},
            {"label": "R&D Investment", "value": round(rnd_impact, 2), "type": "relative"},
            {"label": "Marketing Lift", "value": round(mktg_impact, 2), "type": "relative"},
            {"label": "Admin Overhead", "value": round(admin_impact, 2), "type": "relative"},
            {"label": "Projected Profit", "value": round(target_profit, 2), "type": "total"},
        ]
        return drivers

def get_engine() -> FinancialEngine:
    return FinancialEngine()
