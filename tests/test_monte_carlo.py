import pytest
import numpy as np
from src.monte_carlo import run_monte_carlo

def test_monte_carlo_statistics():
    res = run_monte_carlo(
        base_revenue=2000000.0,
        base_cogs=800000.0,
        base_rnd=200000.0,
        base_mktg=150000.0,
        base_admin=100000.0,
        demand_volatility_pct=10.0,
        cogs_inflation_pct=5.0,
        n_simulations=5000,
    )

    assert res["n_simulations"] == 5000
    assert "mean_profit" in res
    assert "var_95_level" in res
    assert "cvar_95" in res
    assert "target_probability" in res
    # VaR 95% should be less than the mean profit
    assert res["var_95_level"] <= res["mean_profit"]
    # CVaR (tail loss average) should be <= VaR level
    assert res["cvar_95"] <= res["var_95_level"]
