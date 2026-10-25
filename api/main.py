import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from api.schemas import SinglePredictionRequest, SinglePredictionResponse, ModelInfoResponse
from models.registry import get_registry

app = FastAPI(
    title="Profit Prediction & Decision-Support API",
    description="High-performance machine learning backend for corporate profit forecasting and uncertainty quantification.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "Profit Prediction API",
        "version": "2.0.0",
    }

@app.get("/model-info", response_model=ModelInfoResponse, tags=["Model"])
def get_model_info():
    registry = get_registry()
    meta = registry.metadata
    return ModelInfoResponse(
        model_type=meta.get("model_type", "RandomForestRegressor"),
        training_samples=meta.get("training_samples", 50),
        trained_at=meta.get("trained_at", "N/A"),
        best_model_metrics=meta.get("best_model_metrics", {}),
        feature_importances=meta.get("feature_importances", None),
    )

@app.post("/predict", response_model=SinglePredictionResponse, tags=["Inference"])
def predict(request: SinglePredictionRequest):
    try:
        registry = get_registry()
        result = registry.predict_single(
            rnd=request.rnd,
            admin=request.admin,
            marketing=request.marketing,
            confidence_level=request.confidence_level,
        )
        return SinglePredictionResponse(
            predicted_profit=result["predicted_profit"],
            lower_bound=result["lower_bound"],
            upper_bound=result["upper_bound"],
            margin_error=result["margin_error"],
            confidence_level=result["confidence_level"],
            currency="INR",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
