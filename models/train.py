import json
import logging
from datetime import datetime
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    ExtraTreesRegressor,
    VotingRegressor,
)
from sklearn.linear_model import Ridge, Lasso, ElasticNet, BayesianRidge
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import KFold, cross_validate
from sklearn.preprocessing import StandardScaler

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.config import (
    ARTIFACTS_DIR,
    CORE_FEATURES,
    METADATA_JSON_PATH,
    MODEL_PKL_PATH,
    SCALER_PKL_PATH,
    STARTUPS_CSV_PATH,
    TARGET_FEATURE,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_10_model_zoo():
    """Returns the dictionary of 10 candidate machine learning models."""
    rf = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=6)
    gbm = GradientBoostingRegressor(n_estimators=100, random_state=42, learning_rate=0.08)
    ridge = Ridge(alpha=1.0)
    extra_trees = ExtraTreesRegressor(n_estimators=100, random_state=42, max_depth=6)
    lasso = Lasso(alpha=50.0, random_state=42)
    elastic_net = ElasticNet(alpha=0.5, l1_ratio=0.5, random_state=42)
    svr = SVR(kernel="rbf", C=1000.0, epsilon=0.1)
    knn = KNeighborsRegressor(n_neighbors=5, weights="distance")
    bayes_ridge = BayesianRidge()

    # 10. Voting / Stacking Meta-Ensemble
    ensemble = VotingRegressor(
        estimators=[
            ("rf", rf),
            ("gbm", gbm),
            ("ridge", ridge),
            ("extra_trees", extra_trees),
        ]
    )

    return {
        "Ensemble (Voting Meta-Model)": ensemble,
        "Gradient Boosting (GBM)": gbm,
        "Random Forest Regressor": rf,
        "Extra Trees Regressor": extra_trees,
        "Ridge Regression (L2)": ridge,
        "Bayesian Ridge Regressor": bayes_ridge,
        "Lasso Regression (L1)": lasso,
        "ElasticNet Regression": elastic_net,
        "Support Vector Regression (SVR)": svr,
        "K-Nearest Neighbors (KNN)": knn,
    }

def train_and_save(data_path: Path = STARTUPS_CSV_PATH) -> dict:
    """Trains all 10 candidate models on dataset, computes CV tournament metrics, and saves model suite."""
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found at {data_path}")

    df = pd.read_csv(data_path)
    X = df[CORE_FEATURES]
    y = df[TARGET_FEATURE]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    models = get_10_model_zoo()
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    eval_results = {}
    fitted_models = {}

    for name, model in models.items():
        cv = cross_validate(
            model,
            X_scaled,
            y,
            cv=kf,
            scoring=["r2", "neg_mean_absolute_error", "neg_root_mean_squared_error"],
        )
        r2_m = float(np.mean(cv["test_r2"]))
        mae_m = float(-np.mean(cv["test_neg_mean_absolute_error"]))
        rmse_m = float(-np.mean(cv["test_neg_root_mean_squared_error"]))

        eval_results[name] = {
            "r2_mean": round(r2_m, 4),
            "r2_std": round(float(np.std(cv["test_r2"])), 4),
            "mae_mean": round(mae_m, 2),
            "rmse_mean": round(rmse_m, 2),
        }
        # Fit on all data
        model.fit(X_scaled, y)
        fitted_models[name] = model

    # Rank models by R2 score
    sorted_ranks = sorted(eval_results.items(), key=lambda x: x[1]["r2_mean"], reverse=True)
    leaderboard = []
    for rank_idx, (m_name, m_metrics) in enumerate(sorted_ranks):
        medal = "🥇 " if rank_idx == 0 else ("🥈 " if rank_idx == 1 else ("🥉 " if rank_idx == 2 else f"#{rank_idx+1} "))
        leaderboard.append({
            "rank": medal,
            "name": m_name,
            "r2": m_metrics["r2_mean"],
            "mae": m_metrics["mae_mean"],
            "rmse": m_metrics["rmse_mean"],
        })

    best_model_name = sorted_ranks[0][0]
    best_model = fitted_models[best_model_name]

    # Save artifacts
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    # Save the whole suite of fitted models so user can switch between any of them
    model_suite_payload = {
        "best_model_name": best_model_name,
        "default_model": best_model,
        "models": fitted_models,
    }
    joblib.dump(model_suite_payload, MODEL_PKL_PATH)
    joblib.dump(scaler, SCALER_PKL_PATH)

    # Feature importances from best tree model
    rf_model = fitted_models["Random Forest Regressor"]
    feature_importances = dict(zip(CORE_FEATURES, [float(v) for v in rf_model.feature_importances_]))

    metadata = {
        "model_type": f"{best_model_name} (Best of 10 Tournament)",
        "models_count": len(models),
        "features": CORE_FEATURES,
        "target": TARGET_FEATURE,
        "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "training_samples": len(df),
        "best_model_metrics": eval_results[best_model_name],
        "all_model_benchmarks": eval_results,
        "leaderboard": leaderboard,
        "feature_importances": feature_importances,
    }

    with open(METADATA_JSON_PATH, "w") as f:
        json.dump(metadata, f, indent=2)

    logging.info(f"Trained 10 models. Tournament Winner: {best_model_name} (R² = {eval_results[best_model_name]['r2_mean']:.4f})")
    return metadata

if __name__ == "__main__":
    train_and_save()
