import numpy as np
from typing import Dict, Any

def run_monte_carlo(
    base_revenue: float,
    base_cogs: float,
    base_rnd: float = 200000.0,
    base_mktg: float = 180000.0,
    base_admin: float = 120000.0,
    demand_volatility_pct: float = 8.0,
    cogs_inflation_pct: float = 5.0,
    price_volatility_pct: float = 3.0,
    target_profit: float = 0.0,
    n_simulations: int = 10000,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """
    Vectorized 10,000-run Monte Carlo Risk Simulation.
    Calculates Value at Risk (VaR 95%), Expected Shortfall (CVaR), and probability of target attainment.
    """
    np.random.seed(random_seed)

    # Stochastic Shocks
    demand_shocks = np.random.normal(0, demand_volatility_pct / 100.0, n_simulations)
    cogs_shocks = np.random.normal(0, cogs_inflation_pct / 100.0, n_simulations)
    price_shocks = np.random.normal(0, price_volatility_pct / 100.0, n_simulations)

    sim_revenues = base_revenue * (1.0 + demand_shocks) * (1.0 + price_shocks)
    sim_cogs = base_cogs * (1.0 + demand_shocks) * (1.0 + cogs_shocks)
    fixed_opex = base_rnd + base_mktg + base_admin

    sim_profits = sim_revenues - (sim_cogs + fixed_opex)

    # Statistical distribution metrics
    mean_profit = float(np.mean(sim_profits))
    median_profit = float(np.median(sim_profits))
    std_profit = float(np.std(sim_profits))

    p5 = float(np.percentile(sim_profits, 5))
    p10 = float(np.percentile(sim_profits, 10))
    p90 = float(np.percentile(sim_profits, 90))
    p95 = float(np.percentile(sim_profits, 95))

    # Value at Risk (95% confidence level)
    # The minimum profit expected with 95% certainty
    var_95_level = p5
    var_95_loss_from_mean = max(0.0, mean_profit - p5)

    # Conditional VaR (Expected Shortfall): average of worst 5% outcomes
    tail_losses = sim_profits[sim_profits <= p5]
    cvar_95 = float(np.mean(tail_losses)) if len(tail_losses) > 0 else p5

    # Target Probability
    if target_profit <= 0:
        target_profit = mean_profit
    target_probability = float(np.mean(sim_profits >= target_profit) * 100.0)

    # Downside loss risk (prob of negative profit)
    unprofitable_probability = float(np.mean(sim_profits < 0) * 100.0)

    return {
        "n_simulations": n_simulations,
        "mean_profit": round(mean_profit, 2),
        "median_profit": round(median_profit, 2),
        "std_profit": round(std_profit, 2),
        "p5": round(p5, 2),
        "p10": round(p10, 2),
        "p90": round(p90, 2),
        "p95": round(p95, 2),
        "var_95_level": round(var_95_level, 2),
        "var_95_loss": round(var_95_loss_from_mean, 2),
        "cvar_95": round(cvar_95, 2),
        "target_profit": round(target_profit, 2),
        "target_probability": round(target_probability, 1),
        "unprofitable_probability": round(unprofitable_probability, 1),
        "sim_profits": sim_profits,  # Raw array for Plotly histogram
    }
