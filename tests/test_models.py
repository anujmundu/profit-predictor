import pytest
import pandas as pd
from models.registry import ModelRegistry
from src.config import CORE_FEATURES

def test_model_registry_single_prediction():
    registry = ModelRegistry()
    res = registry.predict_single(rnd=160000, admin=130000, marketing=300000, confidence_level=0.80)

    assert "predicted_profit" in res
    assert "lower_bound" in res
    assert "upper_bound" in res
    assert res["lower_bound"] <= res["predicted_profit"] <= res["upper_bound"]

def test_model_registry_batch_prediction():
    registry = ModelRegistry()
    sample_df = pd.DataFrame([
        {"R&D Spend": 160000, "Administration": 120000, "Marketing Spend": 300000},
        {"R&D Spend": 100000, "Administration": 110000, "Marketing Spend": 200000},
    ])

    result_df = registry.predict_batch(sample_df)
    assert "Predicted Profit" in result_df.columns
    assert "CI Lower" in result_df.columns
    assert "CI Upper" in result_df.columns
    assert len(result_df) == 2

def test_model_registry_missing_feature_error():
    registry = ModelRegistry()
    invalid_df = pd.DataFrame([{"R&D Spend": 160000}])
    with pytest.raises(ValueError):
        registry.predict_batch(invalid_df)

def test_10_models_consensus():
    registry = ModelRegistry()
    models = registry.get_available_models()
    assert len(models) >= 10

    consensus = registry.predict_all_models(rnd=160000, admin=130000, marketing=300000)
    assert len(consensus) == len(models)
    for c in consensus:
        assert "model_name" in c
        assert "predicted_profit" in c
        assert isinstance(c["predicted_profit"], float)

def test_benchmark_datasets_catalog():
    from src.data_loader import load_benchmark_catalog, load_benchmark_dataset
    catalog = load_benchmark_catalog()
    assert len(catalog) >= 50

    # Test loading a sample sector dataset
    first_sector = catalog[0]["slug"]
    df = load_benchmark_dataset(first_sector)
    assert not df.empty
    assert "Profit" in df.columns
    assert "Revenue" in df.columns
    assert "R&D Spend" in df.columns
