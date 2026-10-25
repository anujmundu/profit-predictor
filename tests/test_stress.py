import pytest
from src.stress_tester import get_stress_tester

def test_macro_stress_tester_apply():
    tester = get_stress_tester()
    res = tester.apply_stress(
        base_revenue=3000000.0,
        base_cogs=600000.0,
        base_rnd=500000.0,
        base_admin=300000.0,
        base_mktg=800000.0,
        inflation_cogs_pct=15.0,
        rate_hike_bps=300,
        cac_inflation_pct=20.0,
        demand_contraction_pct=10.0,
    )

    assert "baseline" in res
    assert "stressed" in res
    assert "resilience" in res

    # Stressed revenue should be lower than baseline
    assert res["stressed"]["revenue"] < res["baseline"]["revenue"]
    # Stressed total costs should be higher than baseline
    assert res["stressed"]["total_costs"] > res["baseline"]["total_costs"]
    # Resilience score should be between 0 and 100
    assert 0 <= res["resilience"]["score"] <= 100
    assert "tier" in res["resilience"]

def test_stress_presets():
    tester = get_stress_tester()
    assert len(tester.PRESETS) >= 3
    assert "2026 Stagflation Shock" in tester.PRESETS
