import pytest
import pandas as pd
from src.financial_engine import FinancialEngine

def test_financial_engine_dataset_generation():
    engine = FinancialEngine()
    df = engine.load_data()
    assert not df.empty
    assert "Quarter" in df.columns
    assert "Profit" in df.columns
    assert "Revenue" in df.columns
    assert "COGS" in df.columns

def test_financial_engine_kpis():
    engine = FinancialEngine()
    df = engine.load_data()
    timeline = engine.get_aggregated_timeline(df)
    kpis = engine.compute_kpis(timeline)

    assert "profit" in kpis
    assert "revenue" in kpis
    assert "costs" in kpis
    assert "margin_pct" in kpis
    assert isinstance(kpis["profit"], float)

def test_financial_engine_scenarios():
    engine = FinancialEngine()
    df = engine.load_data()
    timeline = engine.get_aggregated_timeline(df)
    scenarios = engine.simulate_scenarios(
        timeline=timeline,
        price_change_pct=5.0,
        volume_change_pct=10.0,
        cogs_change_pct=-5.0,
        marketing_change_pct=10.0,
        rnd_change_pct=5.0,
    )

    assert "Baseline" in scenarios
    assert "Custom" in scenarios
    assert "Optimistic" in scenarios
    assert "Pessimistic" in scenarios

    # Optimistic profit should exceed pessimistic profit in forecast
    opt_fore = scenarios["Optimistic"][scenarios["Optimistic"]["Is_Forecast"] == True]["Profit"].sum()
    pess_fore = scenarios["Pessimistic"][scenarios["Pessimistic"]["Is_Forecast"] == True]["Profit"].sum()
    assert opt_fore > pess_fore
