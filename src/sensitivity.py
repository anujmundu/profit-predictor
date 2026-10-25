import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.config import CORE_FEATURES
from models.registry import get_registry

class SensitivityEngine:
    """Calculates sensitivity tornado rankings, 2D profit frontier contour maps, and marginal ROAS."""

    def __init__(self):
        self.registry = get_registry()

    def compute_tornado(
        self,
        base_revenue: float,
        base_cogs: float,
        base_rnd: float,
        base_mktg: float,
        base_admin: float,
        swing_pct: float = 10.0,
    ) -> List[Dict[str, Any]]:
        """
        Computes profit swings for +/- swing_pct across primary business levers.
        Ranks from widest swing (most sensitive) to narrowest swing.
        """
        base_profit = base_revenue - (base_cogs + base_rnd + base_mktg + base_admin)
        factor = swing_pct / 100.0

        levers = [
            {
                "name": "Product Pricing",
                "low_profit": (base_revenue * (1.0 - factor)) - (base_cogs + base_rnd + base_mktg + base_admin),
                "high_profit": (base_revenue * (1.0 + factor)) - (base_cogs + base_rnd + base_mktg + base_admin),
            },
            {
                "name": "Market Demand Volume",
                "low_profit": (base_revenue * (1.0 - factor)) - (base_cogs * (1.0 - factor) + base_rnd + base_mktg + base_admin),
                "high_profit": (base_revenue * (1.0 + factor)) - (base_cogs * (1.0 + factor) + base_rnd + base_mktg + base_admin),
            },
            {
                "name": "COGS / Supply Cost",
                "low_profit": base_revenue - (base_cogs * (1.0 + factor) + base_rnd + base_mktg + base_admin), # higher cogs = lower profit
                "high_profit": base_revenue - (base_cogs * (1.0 - factor) + base_rnd + base_mktg + base_admin),
            },
            {
                "name": "Marketing Spend",
                "low_profit": base_revenue - (base_cogs + base_rnd + (base_mktg * (1.0 + factor)) + base_admin),
                "high_profit": base_revenue - (base_cogs + base_rnd + (base_mktg * (1.0 - factor)) + base_admin),
            },
            {
                "name": "R&D Allocation",
                "low_profit": base_revenue - (base_cogs + (base_rnd * (1.0 + factor)) + base_mktg + base_admin),
                "high_profit": base_revenue - (base_cogs + (base_rnd * (1.0 - factor)) + base_mktg + base_admin),
            },
            {
                "name": "Admin Overhead",
                "low_profit": base_revenue - (base_cogs + base_rnd + base_mktg + (base_admin * (1.0 + factor))),
                "high_profit": base_revenue - (base_cogs + base_rnd + base_mktg + (base_admin * (1.0 - factor))),
            },
        ]

        results = []
        for l in levers:
            swing = abs(l["high_profit"] - l["low_profit"])
            results.append({
                "lever": l["name"],
                "base_profit": round(base_profit, 2),
                "low_profit": round(l["low_profit"], 2),
                "high_profit": round(l["high_profit"], 2),
                "low_delta": round(l["low_profit"] - base_profit, 2),
                "high_delta": round(l["high_profit"] - base_profit, 2),
                "swing": round(swing, 2),
            })

        # Sort descending by swing
        return sorted(results, key=lambda x: x["swing"], reverse=True)

    def compute_profit_surface(
        self,
        admin_spend: float = 120000.0,
        rnd_range: Tuple[float, float] = (50000.0, 250000.0),
        mktg_range: Tuple[float, float] = (50000.0, 350000.0),
        grid_points: int = 25,
    ) -> Dict[str, Any]:
        """
        Generates 2D contour grid for Marketing ($X$) vs R&D ($Y$) to discover the maximum profit sweet spot.
        """
        mktg_vals = np.linspace(mktg_range[0], mktg_range[1], grid_points)
        rnd_vals = np.linspace(rnd_range[0], rnd_range[1], grid_points)

        # Meshgrid
        M, R = np.meshgrid(mktg_vals, rnd_vals)
        flat_mktg = M.flatten()
        flat_rnd = R.flatten()
        flat_admin = np.full_like(flat_mktg, admin_spend)

        df_grid = pd.DataFrame({
            "R&D Spend": flat_rnd,
            "Administration": flat_admin,
            "Marketing Spend": flat_mktg,
        })

        scaled_grid = self.registry.scaler.transform(df_grid[CORE_FEATURES])
        preds = self.registry.model.predict(scaled_grid)
        Z = preds.reshape(grid_points, grid_points)

        # Find Sweet Spot (Maximum Profit point)
        max_idx = np.unravel_index(np.argmax(Z), Z.shape)
        sweet_rnd = float(rnd_vals[max_idx[0]])
        sweet_mktg = float(mktg_vals[max_idx[1]])
        max_profit = float(Z[max_idx])

        return {
            "mktg_vals": mktg_vals.tolist(),
            "rnd_vals": rnd_vals.tolist(),
            "profit_grid": Z.tolist(),
            "sweet_spot": {
                "rnd_spend": round(sweet_rnd, 2),
                "marketing_spend": round(sweet_mktg, 2),
                "admin_spend": round(admin_spend, 2),
                "max_profit": round(max_profit, 2),
            },
        }

def get_sensitivity_engine() -> SensitivityEngine:
    return SensitivityEngine()
