import pytest
from src.optimizer import solve_optimal_budget

def test_goal_seek_optimizer_convergence():
    target = 150000.0
    res = solve_optimal_budget(target_profit=target)

    assert "achieved_profit" in res
    assert "optimal_rnd" in res
    assert "optimal_marketing" in res
    assert "optimal_admin" in res
    assert "total_budget" in res
    assert res["total_budget"] > 0
    # Check that achieved profit is within reasonable bounds of target
    assert res["achieved_profit"] >= target * 0.90

def test_goal_seek_optimizer_bounds():
    res = solve_optimal_budget(
        target_profit=120000.0,
        min_rnd=50000.0,
        max_rnd=100000.0,
    )
    assert 49000.0 <= res["optimal_rnd"] <= 101000.0
