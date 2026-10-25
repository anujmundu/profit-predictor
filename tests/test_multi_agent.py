import pytest
from src.copilot import get_cfo_copilot

def test_deliberate_boardroom():
    copilot = get_cfo_copilot()
    kpis = {
        "profit": 1200000.0,
        "revenue": 4500000.0,
        "margin_pct": 26.6,
    }

    res = copilot.deliberate_boardroom(
        strategic_goal="Achieve ₹20 Lakhs Net Profit next quarter",
        current_kpis=kpis,
    )

    assert "comptroller_stance" in res
    assert "cro_stance" in res
    assert "consensus_stance" in res
    assert "opt_result" in res
    assert "Comptroller" in res["comptroller_stance"]
    assert "Chief Revenue Officer" in res["cro_stance"]
    assert "Chief Strategist" in res["consensus_stance"]
    assert res["target_amount"] > 0
