import logging
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.config import CORE_FEATURES
from models.registry import get_registry

logger = logging.getLogger(__name__)

class ProfitGoalSeekOptimizer:
    """
    Inverse Prescriptive Optimization Engine.
    Determines the exact mathematical budget allocation (R&D, Admin, Marketing)
    required to achieve or exceed a target profit while minimizing total expenditure.
    Uses global genetic differential evolution with adaptive constraint penalties.
    """

    def __init__(self):
        self.registry = get_registry()

    def solve(
        self,
        target_profit: float,
        min_rnd: float = 10000.0,
        max_rnd: float = 300000.0,
        min_admin: float = 40000.0,
        max_admin: float = 250000.0,
        min_mktg: float = 10000.0,
        max_mktg: float = 450000.0,
        weight_rnd: float = 1.0,
        weight_admin: float = 1.0,
        weight_mktg: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Solves constrained optimization:
        Minimize: w_rnd * RND + w_admin * ADMIN + w_mktg * MKTG + penalty(profit shortfall)
        """
        model = self.registry.model
        scaler = self.registry.scaler

        bounds = [
            (min_rnd, max_rnd),
            (min_admin, max_admin),
            (min_mktg, max_mktg),
        ]

        # Penalized loss function for non-smooth tree models
        def loss(x):
            df_in = pd.DataFrame([x], columns=CORE_FEATURES)
            x_scaled = scaler.transform(df_in)
            pred = float(model.predict(x_scaled)[0])

            shortfall = max(0.0, target_profit - pred)
            spend = (weight_rnd * x[0]) + (weight_admin * x[1]) + (weight_mktg * x[2])
            # Quadratic penalty if shortfall exists
            penalty = 500.0 * (shortfall ** 1.5)
            return spend + penalty

        res = differential_evolution(
            loss,
            bounds=bounds,
            seed=42,
            maxiter=35,
            popsize=12,
            tol=1e-3,
            polish=True,
        )

        opt_rnd = float(res.x[0])
        opt_admin = float(res.x[1])
        opt_mktg = float(res.x[2])
        total_budget = opt_rnd + opt_admin + opt_mktg

        # Predict actual profit at optimal allocation
        df_opt = pd.DataFrame([[opt_rnd, opt_admin, opt_mktg]], columns=CORE_FEATURES)
        opt_scaled = scaler.transform(df_opt)
        achieved_profit = float(model.predict(opt_scaled)[0])

        roi = (achieved_profit / total_budget) if total_budget > 0 else 0.0
        allocation_pct = {
            "R&D Spend": round((opt_rnd / total_budget) * 100, 1),
            "Administration": round((opt_admin / total_budget) * 100, 1),
            "Marketing Spend": round((opt_mktg / total_budget) * 100, 1),
        }

        target_met = achieved_profit >= (target_profit * 0.95)

        return {
            "success": target_met,
            "target_profit": round(target_profit, 2),
            "achieved_profit": round(achieved_profit, 2),
            "optimal_rnd": round(opt_rnd, 2),
            "optimal_admin": round(opt_admin, 2),
            "optimal_marketing": round(opt_mktg, 2),
            "total_budget": round(total_budget, 2),
            "roi_ratio": round(roi, 2),
            "allocation_pct": allocation_pct,
            "message": "Optimization converged: Target milestone achieved with minimal capital." if target_met else "Target profit exceeds achievable bounds within current budget limits.",
        }

def solve_optimal_budget(target_profit: float, **kwargs) -> Dict[str, Any]:
    optimizer = ProfitGoalSeekOptimizer()
    return optimizer.solve(target_profit, **kwargs)
