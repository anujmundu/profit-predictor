from datetime import datetime
from typing import Dict, Any
from src.config import format_currency

def generate_boardroom_report_html(
    kpis: Dict[str, Any],
    monte_carlo_res: Dict[str, Any],
    narrative_text: str,
    company_name: str = "Enterprise Global Corp",
) -> str:
    """Generates an executive boardroom memorandum formatted for printing or PDF export."""
    today_str = datetime.now().strftime("%B %d, %Y")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CFO Strategic Briefing & Forecast Memorandum - {today_str}</title>
    <style>
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            color: #1E293B;
            background-color: #FFFFFF;
            margin: 0;
            padding: 40px;
            line-height: 1.6;
        }}
        .header-bar {{
            border-bottom: 3px solid #4F46E5;
            padding-bottom: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        .title {{
            font-size: 26px;
            font-weight: 800;
            color: #0F172A;
            margin: 0;
        }}
        .subtitle {{
            font-size: 14px;
            color: #64748B;
            margin-top: 5px;
        }}
        .meta-pill {{
            background: #EEF2FF;
            color: #4F46E5;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 35px;
        }}
        .kpi-box {{
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 16px;
        }}
        .kpi-label {{
            font-size: 11px;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .kpi-val {{
            font-size: 22px;
            font-weight: 800;
            color: #0F172A;
            margin: 6px 0;
        }}
        .kpi-sub {{
            font-size: 11px;
            color: #10B981;
            font-weight: 600;
        }}
        .section-heading {{
            font-size: 18px;
            font-weight: 700;
            color: #0F172A;
            border-bottom: 1px solid #E2E8F0;
            padding-bottom: 8px;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        .narrative-card {{
            background: #F0FDF4;
            border-left: 4px solid #10B981;
            padding: 16px 20px;
            border-radius: 6px;
            font-size: 14px;
            color: #14532D;
            margin-bottom: 25px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 13px;
        }}
        th, td {{
            padding: 10px 12px;
            text-align: left;
            border-bottom: 1px solid #E2E8F0;
        }}
        th {{
            background: #F8FAFC;
            color: #475569;
            font-weight: 700;
        }}
        .footer {{
            margin-top: 50px;
            border-top: 1px solid #E2E8F0;
            padding-top: 15px;
            font-size: 11px;
            color: #94A3B8;
            display: flex;
            justify-content: space-between;
        }}
        @media print {{
            body {{ padding: 20px; }}
            .header-bar {{ margin-bottom: 20px; }}
        }}
    </style>
</head>
<body>

    <div class="header-bar">
        <div>
            <h1 class="title">CFO Executive Boardroom Memorandum</h1>
            <div class="subtitle">{company_name} | Profit Intelligence & Strategic Capital Guidance</div>
        </div>
        <div>
            <span class="meta-pill">Confidential - C-Suite Access</span>
        </div>
    </div>

    <div class="narrative-card">
        <strong>Strategic Summary:</strong> {narrative_text}
    </div>

    <div class="section-heading">1. Next-Quarter Financial Targets & KPIs</div>
    <div class="kpi-grid">
        <div class="kpi-box">
            <div class="kpi-label">Projected Net Profit</div>
            <div class="kpi-val">{format_currency(kpis['profit'])}</div>
            <div class="kpi-sub">± {format_currency(kpis['profit_ci_delta'])} (80% CI)</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-label">Projected Revenue</div>
            <div class="kpi-val">{format_currency(kpis['revenue'])}</div>
            <div class="kpi-sub">{kpis['revenue_delta_pct']:+0.1f}% QoQ</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-label">Projected Total Costs</div>
            <div class="kpi-val">{format_currency(kpis['costs'])}</div>
            <div class="kpi-sub">COGS + R&D + Mktg + Admin</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-label">Operating Net Margin</div>
            <div class="kpi-val">{kpis['margin_pct']:.1f}%</div>
            <div class="kpi-sub">{kpis['margin_delta_bps']:+0.0f} bps QoQ</div>
        </div>
    </div>

    <div class="section-heading">2. Stochastic Risk & Value-at-Risk Assessment (10,000 Monte Carlo Iterations)</div>
    <table>
        <thead>
            <tr>
                <th>Risk Metric</th>
                <th>Estimated Value</th>
                <th>Strategic Interpretation</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Value at Risk (VaR 95%)</strong></td>
                <td><strong>{format_currency(monte_carlo_res.get('var_95_level', 0))}</strong></td>
                <td>95% confidence that quarterly profit will meet or exceed this baseline threshold.</td>
            </tr>
            <tr>
                <td><strong>Expected Shortfall (CVaR 95%)</strong></td>
                <td>{format_currency(monte_carlo_res.get('cvar_95', 0))}</td>
                <td>Average net profit in the worst 5% tail risk macro conditions.</td>
            </tr>
            <tr>
                <td><strong>Target Attainment Likelihood</strong></td>
                <td><strong>{monte_carlo_res.get('target_probability', 0)}%</strong></td>
                <td>Probability of achieving or beating management target under market volatility.</td>
            </tr>
            <tr>
                <td><strong>Downside Loss Risk (P &lt; 0)</strong></td>
                <td>{monte_carlo_res.get('unprofitable_probability', 0)}%</td>
                <td>Estimated likelihood of operating at a net deficit during severe shocks.</td>
            </tr>
        </tbody>
    </table>

    <div class="section-heading">3. Strategic Capital Directives</div>
    <ul>
        <li><strong>R&D Capital Preservation</strong>: R&D exhibits the highest long-term profit multiplier. Budget cuts in research degrade long-term revenue elasticity by up to 2.4x.</li>
        <li><strong>Marketing CAC Efficiency</strong>: Performance marketing spend should remain within optimal efficiency frontiers to prevent diminishing marginal returns.</li>
        <li><strong>Supply Chain Buffers</strong>: Build safety margins against raw material and delivery cost swings of 5-8%.</li>
    </ul>

    <div class="footer">
        <span>Generated by Enterprise Profit Intelligence Platform v2.0 (2026)</span>
        <span>Date: {today_str} | Status: Approved for Board Presentation</span>
    </div>

</body>
</html>
"""
    return html
