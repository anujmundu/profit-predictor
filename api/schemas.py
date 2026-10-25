from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class SinglePredictionRequest(BaseModel):
    rnd: float = Field(..., description="R&D Spend in INR", ge=0)
    admin: float = Field(..., description="Administration Overhead in INR", ge=0)
    marketing: float = Field(..., description="Marketing Spend in INR", ge=0)
    confidence_level: float = Field(default=0.80, ge=0.50, le=0.99, description="Confidence interval coverage (0.50 - 0.99)")

class SinglePredictionResponse(BaseModel):
    predicted_profit: float
    lower_bound: float
    upper_bound: float
    margin_error: float
    confidence_level: int
    currency: str = "INR"

class ModelInfoResponse(BaseModel):
    model_type: str
    training_samples: int
    trained_at: Optional[str]
    best_model_metrics: Dict[str, Any]
    feature_importances: Optional[Dict[str, float]]
