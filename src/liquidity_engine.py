import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime, timedelta

from src.config import format_currency

class LiquidityEngine:
    """Calculates cash burn, operational runway, zero-cash horizon, and Rule of 40 scorecard."""

    def compute_runway(
        self,
        starting_cash: float,
        quarterly_revenue: float,
        quarterly_cogs: float,
        quarterly_rnd: float,
        quarterly_admin: float,
        quarterly_mktg: float,
        revenue_growth_rate: float = 0.05,
        capex_ratio: float = 0.04,
        working_capital_drag: float = 0.02,
        n_quarters: int = 8,
    ) -> Dict[str, Any]:
        """
        Simulates multi-quarter cash depletion, burn rate, and runway exhaustion date.
        
        Args:
            starting_cash: Initial cash reserves in INR (₹)
            quarterly_revenue: Base gross revenue for Q1
            quarterly_cogs: Cost of Goods Sold for Q1
            quarterly_rnd: R&D expenditure
            quarterly_admin: G&A overhead
            quarterly_mktg: Sales & Marketing budget
            revenue_growth_rate: Expected QoQ revenue expansion rate (e.g. 0.05 = 5%)
            capex_ratio: Capital expenditure as % of revenue (e.g. 0.04)
            working_capital_drag: Working capital lag as % of revenue
            n_quarters: Projection horizon (default 8 quarters / 24 months)
        """
        timeline = []
        current_cash = starting_cash
        current_rev = quarterly_revenue

        runway_months = None
        zero_cash_quarter = None
        is_cash_flow_positive = False

        today = datetime.now()

        for q in range(1, n_quarters + 1):
            # Scale revenue with quarterly compounding
            rev = current_rev * ((1.0 + revenue_growth_rate) ** (q - 1))
            cogs = quarterly_cogs * ((1.0 + revenue_growth_rate * 0.7) ** (q - 1))
            rnd = quarterly_rnd * ((1.0 + revenue_growth_rate * 0.4) ** (q - 1))
            admin = quarterly_admin * ((1.0 + revenue_growth_rate * 0.3) ** (q - 1))
            mktg = quarterly_mktg * ((1.0 + revenue_growth_rate * 0.5) ** (q - 1))

            total_opex = rnd + admin + mktg
            operating_profit = rev - cogs - total_opex

            # Cash Adjustments: CapEx & Working Capital
            capex = rev * capex_ratio
            working_cap = rev * working_capital_drag
            net_cash_flow = operating_profit - capex - working_cap

            # Beginning & Ending Cash
            beginning_cash = current_cash
            current_cash = beginning_cash + net_cash_flow

            # Quarterly Burn is negative cash flow (if burning cash)
            quarterly_burn = abs(net_cash_flow) if net_cash_flow < 0 else 0.0
            monthly_burn = quarterly_burn / 3.0

            if net_cash_flow >= 0 and not is_cash_flow_positive:
                is_cash_flow_positive = True

            # Detect runway exhaustion
            quarter_label = f"Q{q}"
            if current_cash <= 0 and zero_cash_quarter is None:
                zero_cash_quarter = quarter_label
                # Exact fractional months
                if monthly_burn > 0:
                    fractional_months = (beginning_cash / monthly_burn)
                    runway_months = (q - 1) * 3 + fractional_months

            timeline.append({
                "Quarter_Num": q,
                "Quarter_Label": quarter_label,
                "Revenue": rev,
                "Total_Costs": cogs + total_opex,
                "Operating_Profit": operating_profit,
                "Net_Cash_Flow": net_cash_flow,
                "Beginning_Cash": max(0.0, beginning_cash),
                "Ending_Cash": max(0.0, current_cash),
                "Quarterly_Burn": quarterly_burn,
                "Monthly_Burn": monthly_burn,
                "Is_Burning": net_cash_flow < 0,
            })

        # Baseline Q1 Monthly Burn
        q1_burn = timeline[0]["Quarterly_Burn"]
        q1_monthly_burn = timeline[0]["Monthly_Burn"]

        if runway_months is None:
            if is_cash_flow_positive and q1_burn == 0:
                runway_months = 999.0  # Infinite / Cash flow positive
                zero_cash_date_str = "Profitable / Self-Sustaining"
            else:
                runway_months = (starting_cash / q1_monthly_burn) if q1_monthly_burn > 0 else 999.0
                days_left = int(runway_months * 30.4)
                exhaustion_date = today + timedelta(days=days_left)
                zero_cash_date_str = exhaustion_date.strftime("%b %Y")
        else:
            days_left = int(runway_months * 30.4)
            exhaustion_date = today + timedelta(days=days_left)
            zero_cash_date_str = exhaustion_date.strftime("%b %Y")

        timeline_df = pd.DataFrame(timeline)

        return {
            "starting_cash": starting_cash,
            "q1_net_cash_flow": timeline[0]["Net_Cash_Flow"],
            "q1_monthly_burn": q1_monthly_burn,
            "runway_months": runway_months,
            "zero_cash_quarter": zero_cash_quarter or "Beyond 24 Months",
            "zero_cash_date_str": zero_cash_date_str,
            "is_cash_flow_positive": is_cash_flow_positive,
            "timeline_df": timeline_df,
        }

    def compute_rule_of_40(
        self,
        yoy_revenue_growth_pct: float,
        operating_margin_pct: float,
    ) -> Dict[str, Any]:
        """
        Computes the enterprise Rule of 40 scorecard.
        Rule of 40 = YoY Revenue Growth % + Operating Margin %
        """
        score = yoy_revenue_growth_pct + operating_margin_pct

        if score >= 40.0:
            tier = "Elite (Top Decile Valuation)"
            color = "#10B981"  # Emerald
            badge = "🏆 Elite"
            description = (
                f"Outstanding capital efficiency ({score:.1f}%). Premium valuation multiples typically "
                "reward firms exceeding the 40% threshold with low cost of capital."
            )
        elif score >= 25.0:
            tier = "Healthy (Solid Fundamentals)"
            color = "#6366F1"  # Indigo
            badge = "✅ Healthy"
            description = (
                f"Solid business health ({score:.1f}%). Growth and margin are well-balanced with acceptable "
                "reinvestment efficiency."
            )
        elif score >= 10.0:
            tier = "Moderate (Growth/Margin Tension)"
            color = "#F59E0B"  # Amber
            badge = "⚠️ Moderate"
            description = (
                f"Moderate score ({score:.1f}%). Operational drag or elevated customer acquisition costs "
                "are depressing net margins."
            )
        else:
            tier = "Distressed (Operational Drag)"
            color = "#EF4444"  # Red
            badge = "🚨 At Risk"
            description = (
                f"Critically low score ({score:.1f}%). Company is either undergrowing or operating with heavy losses. "
                "Immediate cost discipline or unit economics restructuring required."
            )

        return {
            "score": score,
            "revenue_growth_pct": yoy_revenue_growth_pct,
            "operating_margin_pct": operating_margin_pct,
            "tier": tier,
            "color": color,
            "badge": badge,
            "description": description,
        }

    def compute_unit_economics(
        self,
        mktg_spend: float,
        revenue: float,
        gross_margin: float,
        assumed_customers: int = 100,
        churn_rate_annual: float = 0.12,
    ) -> Dict[str, Any]:
        """Estimates CAC, LTV, and Payback period from expense allocations."""
        if assumed_customers <= 0:
            assumed_customers = 100

        cac = mktg_spend / assumed_customers
        arpu = revenue / assumed_customers
        gross_profit_per_customer = arpu * gross_margin
        ltv = gross_profit_per_customer / churn_rate_annual if churn_rate_annual > 0 else 0.0

        ltv_cac_ratio = (ltv / cac) if cac > 0 else 0.0
        payback_months = (cac / (gross_profit_per_customer / 12.0)) if gross_profit_per_customer > 0 else 99.0

        return {
            "cac": cac,
            "ltv": ltv,
            "ltv_cac_ratio": ltv_cac_ratio,
            "payback_months": min(60.0, max(1.0, payback_months)),
            "health": "Optimal" if ltv_cac_ratio >= 3.0 else ("Acceptable" if ltv_cac_ratio >= 1.5 else "Overheating CAC"),
        }

def get_liquidity_engine() -> LiquidityEngine:
    return LiquidityEngine()
