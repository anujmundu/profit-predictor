import pytest
from src.liquidity_engine import get_liquidity_engine

def test_liquidity_engine_runway():
    engine = get_liquidity_engine()
    res = engine.compute_runway(
        starting_cash=20000000.0,  # 2 Cr
        quarterly_revenue=2500000.0,
        quarterly_cogs=500000.0,
        quarterly_rnd=600000.0,
        quarterly_admin=400000.0,
        quarterly_mktg=1200000.0,
        revenue_growth_rate=0.05,
    )

    assert "runway_months" in res
    assert res["runway_months"] > 0
    assert "timeline_df" in res
    assert len(res["timeline_df"]) == 8
    assert res["timeline_df"]["Ending_Cash"].iloc[0] <= 20000000.0 or res["is_cash_flow_positive"]

def test_rule_of_40_tiers():
    engine = get_liquidity_engine()
    
    # Elite score (>40%)
    elite = engine.compute_rule_of_40(yoy_revenue_growth_pct=25.0, operating_margin_pct=20.0)
    assert elite["score"] == 45.0
    assert "Elite" in elite["tier"]
    
    # Distressed score (<10%)
    distressed = engine.compute_rule_of_40(yoy_revenue_growth_pct=-5.0, operating_margin_pct=2.0)
    assert distressed["score"] == -3.0
    assert "Distressed" in distressed["tier"]

def test_unit_economics():
    engine = get_liquidity_engine()
    ue = engine.compute_unit_economics(
        mktg_spend=300000.0,
        revenue=1500000.0,
        gross_margin=0.70,
        assumed_customers=100,
    )

    assert ue["cac"] == 3000.0
    assert ue["ltv"] > 0
    assert ue["ltv_cac_ratio"] > 0
    assert ue["payback_months"] > 0
