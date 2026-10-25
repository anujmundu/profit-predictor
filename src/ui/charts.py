import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict, Any

from src.config import PALETTE, CURRENCY_SYMBOL

def create_base_layout(title: str = "", height: int = 380) -> go.Layout:
    """Returns consistent, elegant dark glassmorphic Plotly layout with collision-free spacing."""
    return go.Layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=13.5, color="#F1F5F9", family="Plus Jakarta Sans"),
            x=0.01,
            y=0.98,
            xanchor="left",
            yanchor="top",
        ),
        paper_bgcolor="rgba(15, 23, 42, 0.0)",
        plot_bgcolor="rgba(30, 41, 59, 0.35)",
        height=height,
        margin=dict(l=45, r=20, t=55, b=65),
        font=dict(family="Plus Jakarta Sans", color="#94A3B8"),
        xaxis=dict(
            gridcolor="rgba(148, 163, 184, 0.08)",
            zerolinecolor="rgba(148, 163, 184, 0.12)",
            tickfont=dict(size=10, color="#94A3B8"),
            tickangle=-45,
        ),
        yaxis=dict(
            gridcolor="rgba(148, 163, 184, 0.08)",
            zerolinecolor="rgba(148, 163, 184, 0.12)",
            tickfont=dict(size=10, color="#94A3B8"),
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(size=10.5, color="#CBD5E1"),
        ),
        hoverlabel=dict(
            bgcolor="#1E293B",
            font_size=12,
            font_family="Plus Jakarta Sans",
            bordercolor="#475569",
        ),
    )

def plot_forecast_trend(timeline: pd.DataFrame) -> go.Figure:
    """Historical + Forecast Trend with Shaded Confidence Interval Band."""
    fig = go.Figure(layout=create_base_layout("Profit & Revenue Forecast Trajectory", height=380))

    quarters = timeline["Quarter"]

    # Shaded confidence band (Upper & Lower)
    fig.add_trace(go.Scatter(
        x=quarters,
        y=timeline["CI_Upper"],
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=quarters,
        y=timeline["CI_Lower"],
        mode="lines",
        line=dict(width=0),
        fill="tonexty",
        fillcolor="rgba(99, 102, 241, 0.18)",
        name="80% Confidence Interval",
        hoverinfo="skip",
    ))

    # Revenue Line
    fig.add_trace(go.Scatter(
        x=quarters,
        y=timeline["Revenue"],
        mode="lines+markers",
        name="Gross Revenue",
        line=dict(color="#06B6D4", width=2.5),
        marker=dict(size=5),
        hovertemplate="Quarter: %{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>",
    ))

    # Profit Line
    fig.add_trace(go.Scatter(
        x=quarters,
        y=timeline["Profit"],
        mode="lines+markers",
        name="Net Profit",
        line=dict(color="#6366F1", width=3.5),
        marker=dict(size=7, symbol="diamond"),
        hovertemplate="Quarter: %{x}<br>Profit: ₹%{y:,.0f}<extra></extra>",
    ))

    # Add vertical divider between historical and forecast
    forecast_starts = timeline[timeline["Is_Forecast"] == True]
    if not forecast_starts.empty:
        split_q = forecast_starts.iloc[0]["Quarter"]
        split_idx = list(quarters).index(split_q)
        fig.add_vline(
            x=split_idx,
            line_width=1.5,
            line_dash="dash",
            line_color="#94A3B8",
            annotation_text="Forecast Horizon",
            annotation_position="bottom left",
            annotation_font_color="#A5B4FC",
            annotation_font_size=10,
        )

    fig.update_layout(
        title=dict(
            text="<b>Profit & Revenue Forecast Trajectory</b>",
            font=dict(size=14, color="#F1F5F9", family="Plus Jakarta Sans"),
            x=0.01,
            y=0.98,
            xanchor="left",
            yanchor="top",
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#CBD5E1"),
        ),
        margin=dict(l=45, r=20, t=50, b=70),
        xaxis=dict(tickangle=-45, tickfont=dict(size=10, color="#94A3B8")),
    )
    return fig

def plot_margin_trend(timeline: pd.DataFrame) -> go.Figure:
    """Profit Margin % over time with 25% target line."""
    fig = go.Figure(layout=create_base_layout("Operating Profit Margin (%) & Benchmark", height=380))

    fig.add_trace(go.Scatter(
        x=timeline["Quarter"],
        y=timeline["Margin_Pct"],
        mode="lines+markers",
        name="Operating Margin %",
        line=dict(color="#10B981", width=3),
        marker=dict(size=6),
        fill="tozeroy",
        fillcolor="rgba(16, 185, 129, 0.08)",
        hovertemplate="Quarter: %{x}<br>Margin: %{y:.2f}%<extra></extra>",
    ))

    # Target line at 25%
    fig.add_hline(
        y=25.0,
        line_dash="dot",
        line_color="#F59E0B",
        annotation_text="Target Benchmark (25%)",
        annotation_position="top right",
        annotation_font_color="#FCD34D",
        annotation_font_size=10,
    )

    fig.update_yaxes(ticksuffix="%")
    fig.update_layout(
        title=dict(
            text="<b>Operating Profit Margin (%) & Benchmark</b>",
            font=dict(size=14, color="#F1F5F9", family="Plus Jakarta Sans"),
            x=0.01,
            y=0.98,
            xanchor="left",
            yanchor="top",
        ),
        showlegend=False,
        margin=dict(l=45, r=20, t=50, b=70),
        xaxis=dict(tickangle=-45, tickfont=dict(size=10, color="#94A3B8")),
    )
    return fig

def plot_waterfall_drivers(drivers: List[Dict[str, Any]]) -> go.Figure:
    """Waterfall driver attribution chart showing baseline to target profit breakdown."""
    fig = go.Figure(layout=create_base_layout("Driver Attribution Waterfall (Baseline → Projected Profit)"))

    labels = [d["label"] for d in drivers]
    values = [d["value"] for d in drivers]
    measures = ["absolute" if d["type"] == "total" else "relative" for d in drivers]

    fig.add_trace(go.Waterfall(
        name="Impact",
        orientation="v",
        measure=measures,
        x=labels,
        textposition="outside",
        text=[f"₹{v/1e5:.1f}L" if abs(v) >= 1e5 else f"₹{v:,.0f}" for v in values],
        y=values,
        connector=dict(line=dict(color="rgba(255, 255, 255, 0.2)")),
        decreasing=dict(marker=dict(color="#EF4444")),
        increasing=dict(marker=dict(color="#10B981")),
        totals=dict(marker=dict(color="#6366F1")),
    ))

    fig.update_layout(showlegend=False)
    return fig

def plot_scenario_comparison(scenarios: Dict[str, pd.DataFrame]) -> go.Figure:
    """Compares Baseline, Custom, Optimistic, and Pessimistic scenario forecasts."""
    fig = go.Figure(layout=create_base_layout("Multi-Scenario Profit Trajectory Comparison"))

    colors = {
        "Baseline": "#94A3B8",
        "Custom": "#6366F1",
        "Optimistic": "#10B981",
        "Pessimistic": "#EF4444",
    }
    dash_styles = {
        "Baseline": "dash",
        "Custom": "solid",
        "Optimistic": "dot",
        "Pessimistic": "dot",
    }

    for name, df in scenarios.items():
        fig.add_trace(go.Scatter(
            x=df["Quarter"],
            y=df["Profit"],
            mode="lines+markers",
            name=name,
            line=dict(color=colors.get(name, "#FFFFFF"), width=2.5 if name != "Custom" else 3.5, dash=dash_styles.get(name, "solid")),
            marker=dict(size=6),
            hovertemplate=f"<b>{name}</b><br>Quarter: %{{x}}<br>Profit: ₹%{{y:,.0f}}<extra></extra>",
        ))

    return fig

def plot_shap_attributions(attributions: List[Dict[str, Any]]) -> go.Figure:
    """Horizontal bar chart for SHAP feature attribution."""
    fig = go.Figure(layout=create_base_layout("SHAP Feature Attribution (Impact on Predicted Profit)", height=280))

    features = [a["feature"] for a in attributions]
    shap_vals = [a["shap_value"] for a in attributions]
    colors = ["#10B981" if sv >= 0 else "#EF4444" for sv in shap_vals]

    fig.add_trace(go.Bar(
        x=shap_vals,
        y=features,
        orientation="h",
        marker=dict(color=colors, line=dict(width=1, color="rgba(255,255,255,0.2)")),
        text=[f"{CURRENCY_SYMBOL}{sv:+,.0f}" for sv in shap_vals],
        textposition="auto",
        hovertemplate="Feature: %{y}<br>SHAP Impact: ₹%{x:,.2f}<extra></extra>",
    ))

    fig.update_layout(showlegend=False)
    fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor="rgba(255,255,255,0.4)")
    return fig

def plot_monte_carlo_distribution(sim_profits, target_profit: float, var_95: float) -> go.Figure:
    """Renders 10,000-run Monte Carlo probability distribution with 95% VaR threshold."""
    fig = go.Figure(layout=create_base_layout("10,000-Run Monte Carlo Profit Probability Distribution"))

    # Histogram
    fig.add_trace(go.Histogram(
        x=sim_profits,
        nbinsx=60,
        name="Simulated Profit Frequency",
        marker=dict(
            color="#6366F1",
            line=dict(color="#4338CA", width=0.5),
        ),
        opacity=0.75,
        hovertemplate="Profit: ₹%{x:,.0f}<br>Count: %{y}<extra></extra>",
    ))

    # VaR 95% line
    fig.add_vline(
        x=var_95,
        line_width=2.5,
        line_dash="dash",
        line_color="#EF4444",
        annotation_text=f"VaR 95% (₹{var_95/1e5:.1f}L)",
        annotation_position="top left",
        annotation_font_color="#F87171",
        annotation_font_size=11,
    )

    # Target line
    if target_profit > 0:
        fig.add_vline(
            x=target_profit,
            line_width=2.5,
            line_dash="dot",
            line_color="#10B981",
            annotation_text=f"Board Target (₹{target_profit/1e5:.1f}L)",
            annotation_position="top right",
            annotation_font_color="#34D399",
            annotation_font_size=11,
        )

    fig.update_layout(
        xaxis_title="Net Profit (₹)",
        yaxis_title="Simulation Frequency",
        showlegend=False,
    )
    return fig

def plot_tornado_sensitivity(tornado_data: List[Dict[str, Any]]) -> go.Figure:
    """Renders Tornado sensitivity elasticity ranking chart."""
    fig = go.Figure(layout=create_base_layout("Sensitivity Tornado: Profit Impact of ±10% Lever Swings", height=340))

    levers = [d["lever"] for d in reversed(tornado_data)]
    low_deltas = [d["low_delta"] for d in reversed(tornado_data)]
    high_deltas = [d["high_delta"] for d in reversed(tornado_data)]

    # Downside swing
    fig.add_trace(go.Bar(
        y=levers,
        x=low_deltas,
        name="Downside (-10% shock)",
        orientation="h",
        marker=dict(color="#EF4444"),
        hovertemplate="%{y}<br>Downside: ₹%{x:,.0f}<extra></extra>",
    ))

    # Upside swing
    fig.add_trace(go.Bar(
        y=levers,
        x=high_deltas,
        name="Upside (+10% lift)",
        orientation="h",
        marker=dict(color="#10B981"),
        hovertemplate="%{y}<br>Upside: ₹%{x:,.0f}<extra></extra>",
    ))

    fig.update_layout(
        barmode="overlay",
        xaxis_title="Profit Impact Relative to Baseline (₹)",
        legend=dict(orientation="h", y=1.08, x=1),
    )
    fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor="rgba(255,255,255,0.4)")
    return fig

def plot_profit_contour_surface(
    mktg_vals: List[float], rnd_vals: List[float], profit_grid: List[List[float]], sweet_spot: Dict[str, Any]
) -> go.Figure:
    """Renders 2D interactive profit surface with maximum efficiency sweet spot."""
    fig = go.Figure(layout=create_base_layout("2D Profit Frontier & Sweet Spot Optimization Zone", height=420))

    # Contour
    fig.add_trace(go.Contour(
        z=profit_grid,
        x=[m / 1e5 for m in mktg_vals],
        y=[r / 1e5 for r in rnd_vals],
        colorscale="Viridis",
        contours=dict(
            coloring="heatmap",
            showlabels=True,
            labelfont=dict(size=10, color="white"),
        ),
        colorbar=dict(title="Profit (₹)"),
        hovertemplate="Marketing: ₹%{x:.2f}L<br>R&D: ₹%{y:.2f}L<br>Projected Profit: ₹%{z:,.0f}<extra></extra>",
    ))

    # Sweet Spot Marker
    fig.add_trace(go.Scatter(
        x=[sweet_spot["marketing_spend"] / 1e5],
        y=[sweet_spot["rnd_spend"] / 1e5],
        mode="markers+text",
        marker=dict(color="#EF4444", size=14, symbol="star"),
        text=["★ Optimal Sweet Spot"],
        textposition="top center",
        textfont=dict(color="#F8FAFC", size=11, family="Plus Jakarta Sans"),
        name="Sweet Spot",
        hoverinfo="skip",
    ))

    fig.update_layout(
        xaxis_title="Marketing Spend (₹ Lakhs)",
        yaxis_title="R&D Spend (₹ Lakhs)",
        showlegend=False,
    )
    return fig

def plot_budget_donut(allocation_dict: Dict[str, float]) -> go.Figure:
    """Renders donut chart of recommended budget distribution."""
    fig = go.Figure(layout=create_base_layout("Optimal Capital Allocation Breakdown", height=300))

    labels = list(allocation_dict.keys())
    values = list(allocation_dict.values())
    colors = ["#6366F1", "#06B6D4", "#F59E0B"]

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#0F172A", width=2)),
        textinfo="label+percent",
        textfont=dict(size=11),
        hovertemplate="%{label}: %{percent} (₹%{value:,.0f})<extra></extra>",
    ))

    fig.update_layout(showlegend=False, margin=dict(t=25, b=20, l=20, r=20))
    return fig

def plot_runway_depletion(timeline_df: pd.DataFrame) -> go.Figure:
    """Renders cash balance trajectory and quarterly net burn/cash flow."""
    fig = go.Figure(layout=create_base_layout("Multi-Quarter Cash Reserve & Runway Trajectory", height=380))

    quarters = timeline_df["Quarter_Label"]

    # Cash Balance Area
    fig.add_trace(go.Scatter(
        x=quarters,
        y=timeline_df["Ending_Cash"],
        mode="lines+markers",
        name="Cash Reserves",
        line=dict(color="#10B981", width=3.5),
        fill="tozeroy",
        fillcolor="rgba(16, 185, 129, 0.15)",
        marker=dict(size=7, symbol="circle"),
        hovertemplate="Quarter: %{x}<br>Ending Cash: ₹%{y:,.0f}<extra></extra>",
    ))

    # Net Cash Flow Bars (secondary perspective)
    bar_colors = ["#10B981" if cf >= 0 else "#EF4444" for cf in timeline_df["Net_Cash_Flow"]]
    fig.add_trace(go.Bar(
        x=quarters,
        y=timeline_df["Net_Cash_Flow"],
        name="Net Cash Flow (Burn / Inflow)",
        marker=dict(color=bar_colors, line=dict(color="rgba(255,255,255,0.15)", width=1)),
        opacity=0.6,
        hovertemplate="Quarter: %{x}<br>Net Cash Flow: ₹%{y:,.0f}<extra></extra>",
    ))

    # Zero Cash Danger Line
    fig.add_hline(
        y=0.0,
        line_dash="dash",
        line_color="#EF4444",
        line_width=2,
        annotation_text="Zero Cash Threshold (Insolvency)",
        annotation_position="bottom right",
        annotation_font_color="#F87171",
        annotation_font_size=10,
    )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(size=10.5, color="#CBD5E1"),
        ),
        margin=dict(l=45, r=20, t=50, b=70),
        xaxis=dict(tickangle=-45, tickfont=dict(size=10, color="#94A3B8")),
    )
    return fig

def plot_macro_stress_comparison(base_metrics: Dict[str, Any], stressed_metrics: Dict[str, Any]) -> go.Figure:
    """Renders grouped bar chart comparing Baseline vs. Macro Stressed performance."""
    fig = go.Figure(layout=create_base_layout("Institutional Macro Shock: Baseline vs. Stressed P&L", height=380))

    categories = ["Gross Revenue", "Operating Costs", "Net Operating Profit"]
    base_vals = [base_metrics["revenue"], base_metrics["total_costs"], base_metrics["profit"]]
    stressed_vals = [stressed_metrics["revenue"], stressed_metrics["total_costs"], stressed_metrics["profit"]]

    # Baseline Bars
    fig.add_trace(go.Bar(
        x=categories,
        y=base_vals,
        name="Baseline (Nominal Conditions)",
        marker=dict(color="#6366F1"),
        hovertemplate="%{x}<br>Baseline: ₹%{y:,.0f}<extra></extra>",
        text=[f"₹{v/1e5:.1f}L" if abs(v) >= 1e5 else f"₹{v:,.0f}" for v in base_vals],
        textposition="outside",
    ))

    # Stressed Bars
    stressed_colors = ["#38BDF8", "#F59E0B", "#EF4444" if stressed_vals[2] < 0 else "#10B981"]
    fig.add_trace(go.Bar(
        x=categories,
        y=stressed_vals,
        name="Macro Stressed Performance",
        marker=dict(color=stressed_colors),
        hovertemplate="%{x}<br>Stressed: ₹%{y:,.0f}<extra></extra>",
        text=[f"₹{v/1e5:.1f}L" if abs(v) >= 1e5 else f"₹{v:,.0f}" for v in stressed_vals],
        textposition="outside",
    ))

    fig.update_layout(
        barmode="group",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(size=10.5, color="#CBD5E1"),
        ),
        margin=dict(l=45, r=20, t=50, b=70),
    )
    return fig

