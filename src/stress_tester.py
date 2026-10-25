import numpy as np
import pandas as pd
from typing import Dict, Any, List
from src.config import format_currency

class MacroeconomicStressTester:
    """Simulates institutional CCAR-grade macroeconomic stress shocks and computes resilience scores."""

    PRESETS = {
        "Baseline (No Shock)": {
            "inflation_cogs_pct": 0.0,
            "rate_hike_bps": 0,
            "cac_inflation_pct": 0.0,
            "demand_contraction_pct": 0.0,
            "description": "Standard business operations under nominal macroeconomic conditions.",
        },
        "2026 Stagflation Shock": {
            "inflation_cogs_pct": 14.0,
            "rate_hike_bps": 350,
            "cac_inflation_pct": 22.0,
            "demand_contraction_pct": 12.0,
            "description": "Persistent supply-chain cost surge paired with elevated central bank policy rates and consumer budget tightening.",
        },
        "Venture Capital Freeze (Down-Round Tech Winter)": {
            "inflation_cogs_pct": 5.0,
            "rate_hike_bps": 200,
            "cac_inflation_pct": 38.0,
            "demand_contraction_pct": 18.0,
            "description": "Severe contraction in tech procurement budgets, ad inventory inflation, and extended enterprise sales cycles.",
        },
        "Hyper-Inflationary Supply Disruption": {
            "inflation_cogs_pct": 25.0,
            "rate_hike_bps": 450,
            "cac_inflation_pct": 15.0,
            "demand_contraction_pct": 8.0,
            "description": "Geopolitical disruption triggering energy, raw material, and cloud infrastructure price surges.",
        },
    }

    def apply_stress(
        self,
        base_revenue: float,
        base_cogs: float,
        base_rnd: float,
        base_admin: float,
        base_mktg: float,
        inflation_cogs_pct: float = 12.0,
        rate_hike_bps: int = 300,
        cac_inflation_pct: float = 20.0,
        demand_contraction_pct: float = 10.0,
    ) -> Dict[str, Any]:
        """
        Applies macroeconomic shocks across top-line and operating expenses.
        
        Args:
            base_revenue: Baseline revenue
            base_cogs: Baseline Cost of Goods Sold
            base_rnd: Baseline R&D
            base_admin: Baseline Administration
            base_mktg: Baseline Marketing
            inflation_cogs_pct: Inflation rate on COGS (% increase)
            rate_hike_bps: Basis points rate hike (e.g. 300 bps = 3.0% cost of debt/capital)
            cac_inflation_pct: Increase in marketing cost per customer acquisition (% increase)
            demand_contraction_pct: Drop in demand/sales volume (% reduction)
        """
        # Baseline calculations
        base_opex = base_rnd + base_admin + base_mktg
        base_total_costs = base_cogs + base_opex
        base_profit = base_revenue - base_total_costs
        base_margin = (base_profit / base_revenue * 100) if base_revenue > 0 else 0.0

        # Stressed adjustments
        # 1. Demand shock hits revenue
        stressed_revenue = base_revenue * (1.0 - (demand_contraction_pct / 100.0))

        # 2. Inflation shock hits COGS
        stressed_cogs = base_cogs * (1.0 + (inflation_cogs_pct / 100.0))

        # 3. Rate hike increases carrying/financing costs on administration overhead
        rate_impact_admin = base_admin * (rate_hike_bps / 10000.0)
        stressed_admin = base_admin + rate_impact_admin

        # 4. CAC inflation increases marketing budget needed for equivalent traction
        stressed_mktg = base_mktg * (1.0 + (cac_inflation_pct / 100.0))

        # 5. R&D under stress retains base headcount with modest supply inflation
        stressed_rnd = base_rnd * (1.0 + (inflation_cogs_pct * 0.3 / 100.0))

        stressed_opex = stressed_rnd + stressed_admin + stressed_mktg
        stressed_total_costs = stressed_cogs + stressed_opex
        stressed_profit = stressed_revenue - stressed_total_costs
        stressed_margin = (stressed_profit / stressed_revenue * 100) if stressed_revenue > 0 else 0.0

        profit_delta = stressed_profit - base_profit
        margin_delta = stressed_margin - base_margin

        # Compute Institutional Resilience Score (0 to 100)
        resilience_score = self._compute_resilience_score(
            base_profit=base_profit,
            stressed_profit=stressed_profit,
            base_margin=base_margin,
            stressed_margin=stressed_margin,
            cost_expansion_ratio=(stressed_total_costs / base_total_costs) if base_total_costs > 0 else 1.0,
        )

        return {
            "baseline": {
                "revenue": base_revenue,
                "cogs": base_cogs,
                "rnd": base_rnd,
                "admin": base_admin,
                "mktg": base_mktg,
                "opex": base_opex,
                "total_costs": base_total_costs,
                "profit": base_profit,
                "margin_pct": base_margin,
            },
            "stressed": {
                "revenue": stressed_revenue,
                "cogs": stressed_cogs,
                "rnd": stressed_rnd,
                "admin": stressed_admin,
                "mktg": stressed_mktg,
                "opex": stressed_opex,
                "total_costs": stressed_total_costs,
                "profit": stressed_profit,
                "margin_pct": stressed_margin,
            },
            "deltas": {
                "profit_delta": profit_delta,
                "margin_delta": margin_delta,
                "revenue_loss": stressed_revenue - base_revenue,
                "cost_increase": stressed_total_costs - base_total_costs,
            },
            "resilience": resilience_score,
            "parameters": {
                "inflation_cogs_pct": inflation_cogs_pct,
                "rate_hike_bps": rate_hike_bps,
                "cac_inflation_pct": cac_inflation_pct,
                "demand_contraction_pct": demand_contraction_pct,
            },
        }

    def _compute_resilience_score(
        self,
        base_profit: float,
        stressed_profit: float,
        base_margin: float,
        stressed_margin: float,
        cost_expansion_ratio: float,
    ) -> Dict[str, Any]:
        """Calculates 0-100 Resilience Score based on margin preservation and solvency buffer."""
        # 1. Profit Retention (max 40 pts)
        if base_profit > 0:
            retention_ratio = max(0.0, stressed_profit / base_profit)
            profit_pts = min(40.0, retention_ratio * 40.0)
        else:
            profit_pts = 0.0 if stressed_profit < base_profit else 20.0

        # 2. Margin Solvency (max 35 pts)
        if stressed_margin >= 20.0:
            margin_pts = 35.0
        elif stressed_margin >= 10.0:
            margin_pts = 25.0
        elif stressed_margin >= 0.0:
            margin_pts = 15.0
        elif stressed_margin >= -10.0:
            margin_pts = 5.0
        else:
            margin_pts = 0.0

        # 3. Cost Absorption Capacity (max 25 pts)
        cost_pct_growth = max(0.0, (cost_expansion_ratio - 1.0) * 100)
        cost_pts = max(0.0, 25.0 - (cost_pct_growth * 0.75))

        total_score = max(5.0, min(100.0, profit_pts + margin_pts + cost_pts))

        if total_score >= 80.0:
            tier = "Fortress Balance Sheet"
            badge = "🛡️ Fortress"
            color = "#10B981"
            diagnosis = (
                "Company demonstrates exceptional capital durability. High gross margins absorb inflationary "
                "surges with minimal risk of breaching solvency covenants."
            )
        elif total_score >= 60.0:
            tier = "Resilient (Absorptive Buffer)"
            badge = "✅ Resilient"
            color = "#6366F1"
            diagnosis = (
                "Adequate shock absorption capacity. Profit compresses during stress but operating margin "
                "remains safely positive without requiring emergency restructuring."
            )
        elif total_score >= 40.0:
            tier = "Vulnerable (Margin Compression)"
            badge = "⚠️ Vulnerable"
            color = "#F59E0B"
            diagnosis = (
                "Significant sensitivity to external shocks. Stressed conditions push operating profit near "
                "breakeven. Recommend pre-emptive overhead rationalization."
            )
        else:
            tier = "Critical Distress Risk"
            badge = "🚨 Critical Distress"
            color = "#EF4444"
            diagnosis = (
                "Severe macroeconomic fragility. Under simulated stress, company burns substantial capital. "
                "Immediate defensive capital allocation and emergency opex freeze required."
            )

        return {
            "score": round(total_score, 1),
            "tier": tier,
            "badge": badge,
            "color": color,
            "diagnosis": diagnosis,
        }

def get_stress_tester() -> MacroeconomicStressTester:
    return MacroeconomicStressTester()
