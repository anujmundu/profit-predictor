# 📈 Enterprise Profit Intelligence & Autonomous AI CFO Operating System

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![API](https://img.shields.io/badge/FastAPI-0.109%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-19%20passed-brightgreen.svg)](tests/)

An enterprise-grade financial intelligence, multi-model predictive analytics, and prescriptive capital allocation platform. Designed for modern CFOs, corporate strategists, and investment committees, this platform combines competitive machine learning tournaments, cooperative game-theory explainability (SHAP), stochastic Monte Carlo risk distributions, macroeconomic stress testing, and autonomous multi-agent boardroom deliberation.

---

## 🏛️ Executive Architecture & Core Modules

### 1. 📊 Executive KPI Summary & Multi-Quarter P&L Ledger
- **Financial Statement Generation**: Real-time automated generation of multi-quarter P&L ledgers including Gross Revenue, Cost of Goods Sold (COGS), Gross Profit, Operating Expenses (R&D, Administration, Marketing), EBITDA, Corporate Tax (25%), Interest, Depreciation, and Profit After Tax (PAT).
- **Collision-Free Visualizations**: Synchronized dual Plotly charts contrasting revenue-to-profit conversion alongside departmental budget allocations.
- **Enterprise Ledger Audit**: Downloadable multi-quarter GAAP/IFRS financial projection tables with quarter-over-quarter (QoQ) variance tracking.

### 2. 🎯 Prescriptive Capital Allocator (Inverse Goal-Seek Engine)
- **Constrained Optimization**: Solves the inverse problem—given a desired target profit and a strict total budget ceiling, mathematically discovers the optimal allocation across R&D, Administration, and Marketing spend.
- **Hybrid Solvers**: Combines global **Differential Evolution** (for non-convex parameter spaces) with bounded **Sequential Least Squares Quadratic Programming (SLSQP)** for microsecond convergence.
- **Spend Delta Analysis**: Clear visual delta bridges illustrating exactly which department budgets to expand, maintain, or contract.

### 3. 🎲 Monte Carlo Risk Simulator (10,000 Iterations)
- **Stochastic Volatility Perturbation**: Evaluates earnings volatility under parametric Gaussian macroeconomic uncertainty.
- **Value at Risk (VaR)**: Precise computation of **VaR 95%** and **VaR 99%** quantifying maximum expected drawdown over a given horizon.
- **Conditional Value at Risk (CVaR / Expected Shortfall)**: Tail-risk expectation evaluating average losses beyond the VaR threshold.
- **Probability of Loss**: Dynamic calculation of $P(\text{Profit} < 0)$ with 5-percentile multi-horizon fan charts.

### 4. 🌪️ Tornado Sensitivity & 2D Sweet-Spot Frontier
- **Elasticity Ranking**: Automated numerical partial derivative estimation ($\frac{\partial \text{Profit}}{\partial \text{Spend}}$) ranking departmental spend by profit leverage.
- **Directional Swing Analysis**: $\pm 20\%$ directional variance bands exposing asymmetric sensitivities.
- **2D Profit Sweet-Spot Heatmap**: Bivariate contour meshgrid identifying the global profit maximum surface coordinates.

### 5. 🧪 Multi-Scenario Strategic Planning Lab
- **Comparative Scenario Simulation**: Real-time multi-scenario modeling (**Bull Case**, **Base Case**, **Bear Case**, and **User Custom**).
- **Multivariate Radar Diagnostics**: Radar charts benchmarking margin profiles, capital efficiency, and operational agility across scenarios.

### 6. 🔮 Model Explainability & Feature Attribution (SHAP)
- **Cooperative Game Theory**: Shapley values decomposing predictions into exact monetary rupee attributions per feature ($\sum \phi_i = \hat{y} - \bar{y}$).
- **Adaptive Multi-Model Router**:
  - *Tree Ensembles* (RandomForest, ExtraTrees, GradientBoosting): Handled via native C-optimized `shap.TreeExplainer`.
  - *Linear Models* (Ridge, Lasso, ElasticNet, BayesianRidge): Handled via `shap.LinearExplainer`.
  - *Ensemble Meta-Models* (VotingRegressor, SVR, KNN): Handled via representative background `shap.KernelExplainer` with zero-failure marginal perturbation fallback.
- **Plain-Language Driver Synthesis**: Automated executive commentary translating mathematical Shapley vectors into plain-language board updates.

### 7. 📁 Batch Scoring Studio & Portfolio Ledger
- **High-Throughput Scoring**: Evaluates multi-company cohorts via CSV drag-and-drop.
- **Consensus & Dispersion**: Computes portfolio-wide predictions with inter-model standard deviation spread to flag high-uncertainty portfolio companies.
- **Export Ready**: Scored portfolio ledger downloadable in CSV format.

### 8. 🛡️ Model Governance & Tournament Leaderboard
- **10-Model Cross-Validation Tournament**: Continuous comparative benchmarking across:
  1. *VotingRegressor* (Ensemble Meta-Model)
  2. *Random Forest Regressor*
  3. *Gradient Boosting Regressor*
  4. *Extra Trees Regressor*
  5. *Ridge Regressor*
  6. *Lasso Regressor*
  7. *ElasticNet Regressor*
  8. *Bayesian Ridge Regressor*
  9. *Support Vector Regressor (SVR)*
  10. *K-Nearest Neighbors Regressor (KNN)*
- **Governance Audit**: Displays $R^2$, RMSE, MAE, MAPE, model checksums, training timestamps, and serialization health.

### 9. 🌊 Macro Stress Testing, Liquidity & 3-Agent AI CFO Boardroom
- **Cash Burn & Runway**: Monthly Gross Burn, Net Burn, Operating Cash Flow, Zero-Cash Date forecast, and SaaS **Rule of 40** (Growth % + FCF Margin %).
- **Macro Shocks**: Simulates extreme macroeconomic conditions:
  - *Stagflation Shock* (+15% Inflation, -12% Demand)
  - *Tech Winter* (40% Multiple Compression, -20% CAC Efficiency)
  - *Supply Chain Crisis* (+25% COGS Shock)
  - *Hyper-Growth Expansion* (+35% Demand Surge)
- **Autonomous 3-Agent Boardroom Deliberation**:
  - **Agent 1 (Growth Champion)**: Advocates aggressive reinvestment into R&D and market share expansion.
  - **Agent 2 (Fiscal Conservative)**: Enforces runway preservation, margin defense, and overhead containment.
  - **Agent 3 (Risk Auditor)**: Analyzes tail risks, regulatory exposure, and macroeconomic downside.
  - **Consensus Resolution**: Synthesizes a formal boardroom memorandum with capital allocation votes.

---

## 🌐 55 Pre-Calibrated Sector Benchmark Datasets

Includes **55 individual industry benchmark datasets** spanning 7 macro sectors (SaaS, FinTech, DeepTech, HealthTech, CleanTech, E-Commerce, Consumer). 
- Available for instant preview in the sidebar.
- Downloadable as a single packaged archive: [`data/benchmarks_50_plus_sectors.zip`](data/benchmarks_50_plus_sectors.zip).

---

## 🏗️ Repository Architecture

```text
F:\Profit Prediction\
├── .github/
│   └── workflows/
│       └── ci.yml              # Automated GitHub Actions test pipeline
├── .streamlit/
│   └── config.toml             # Glassmorphic dark design system tokens
├── api/
│   ├── main.py                 # FastAPI microservice (/predict, /batch-predict, /health)
│   └── schemas.py              # Pydantic v2 schemas
├── data/
│   ├── benchmarks/             # 55 Pre-calibrated sector CSV datasets & catalog.json
│   ├── benchmarks_50_plus_sectors.zip # One-click download archive
│   ├── benchmark_generator.py  # Sector benchmark generation engine
│   ├── raw/                    # 50_Startups.csv, input_500_companies.csv
│   └── processed/              # Multi-quarter enterprise ledger series
├── models/
│   ├── artifacts/              # Model binary pickles, scalers & metadata.json
│   ├── registry.py             # Singleton model registry & consensus routing
│   └── train.py                # 10-Model tournament cross-validation trainer
├── notebooks/
│   └── profit_prediction.ipynb # Interactive EDA, tournament & SHAP notebook
├── src/
│   ├── config.py               # Constants, currencies, paths & styling tokens
│   ├── copilot.py              # Autonomous 3-Agent AI CFO deliberation engine
│   ├── data_loader.py          # Cached data loaders (@st.cache_data)
│   ├── explainer.py            # Multi-model SHAP routing & plain-language generator
│   ├── financial_engine.py     # P&L financial ledger, COGS, EBITDA & PAT math
│   ├── liquidity_engine.py     # Cash burn, runway, Rule of 40 calculator
│   ├── monte_carlo.py          # 10,000-run Monte Carlo risk simulator (VaR/CVaR)
│   ├── optimizer.py            # Inverse Goal-Seek optimizer (SLSQP & Diff Evolution)
│   ├── report_generator.py     # Executive boardroom memorandum PDF/HTML export
│   ├── sensitivity.py          # Tornado elasticity & 2D profit sweet spot
│   ├── stress_tester.py        # Macroeconomic shock engine & resilience scoring
│   └── ui/
│       ├── charts.py           # Collision-free Plotly financial charts
│       ├── components.py       # Glassmorphic KPI cards & badges
│       ├── main_view.py        # 9-tab coordinator & sidebar controls
│       ├── styles.py           # CSS design tokens & animations
│       └── tabs/               # 9 standalone modular tab implementations
├── tests/                      # 19 Unit tests covering all algorithms
├── Dockerfile                  # Production multi-stage container
├── docker-compose.yml          # Dual-service composition (Streamlit + FastAPI)
├── requirements.txt            # Production runtime dependencies
└── requirements-dev.txt        # Development & test tooling
```

---

## ⚡ Quickstart Guide

### 1. Local Environment Setup

```bash
# Clone the repository
git clone https://github.com/anujmundu/profit-predictor.git
cd profit-predictor

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Launch the Streamlit Operating System

```bash
streamlit run app.py
```
*Access the interactive platform at `http://localhost:8501`.*

### 3. Launch the FastAPI Microservice

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
*Access interactive Swagger documentation at `http://localhost:8000/docs`.*

### 4. Run via Docker Compose

```bash
docker compose up --build
```
*Launches both Streamlit (port 8501) and FastAPI (port 8000) simultaneously with shared volume mounts.*

---

## 🧪 Automated Testing

The platform includes 19 unit and integration tests verifying numerical consistency, convergence stability, and consensus bounds:

```bash
pytest tests/ -v
```

```text
============================== 19 passed in 115.77s ==============================
tests/test_engine.py::test_ledger_math PASSED
tests/test_engine.py::test_margin_bounds PASSED
tests/test_models.py::test_all_10_models_inference PASSED
tests/test_models.py::test_consensus_dispersion PASSED
tests/test_optimizer.py::test_slsqp_convergence PASSED
tests/test_optimizer.py::test_budget_cap_enforcement PASSED
tests/test_monte_carlo.py::test_var_cvar_order PASSED
tests/test_monte_carlo.py::test_loss_probability_bounds PASSED
tests/test_sensitivity.py::test_tornado_ranking PASSED
tests/test_liquidity.py::test_runway_calculation PASSED
tests/test_liquidity.py::test_rule_of_40_classification PASSED
tests/test_stress.py::test_stagflation_shock_deltas PASSED
tests/test_multi_agent.py::test_copilot_boardroom_deliberation PASSED
...
```

---

## 📄 License & Author

- **Author**: [Anuj Mundu](https://github.com/anujmundu)
- **License**: MIT License. Open for enterprise use, research, and modification.
