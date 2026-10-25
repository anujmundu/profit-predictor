import pytest
from src.sensitivity import get_sensitivity_engine

def test_sensitivity_tornado():
    engine = get_sensitivity_engine()
    tornado = engine.compute_tornado(
        base_revenue=1500000.0,
        base_cogs=500000.0,
        base_rnd=150000.0,
        base_mktg=120000.0,
        base_admin=90000.0,
        swing_pct=10.0,
    )

    assert len(tornado) == 6
    # Should be sorted descending by swing
    for i in range(len(tornado) - 1):
        assert tornado[i]["swing"] >= tornado[i + 1]["swing"]

def test_sensitivity_profit_surface():
    engine = get_sensitivity_engine()
    surface = engine.compute_profit_surface(grid_points=10)

    assert "mktg_vals" in surface
    assert "rnd_vals" in surface
    assert "profit_grid" in surface
    assert "sweet_spot" in surface
    assert "max_profit" in surface["sweet_spot"]
