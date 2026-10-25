import pandas as pd
import streamlit as st
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.config import STARTUPS_CSV_PATH, INPUT_500_CSV_PATH
from src.financial_engine import get_engine

@st.cache_data(ttl=3600)
def load_startups_data() -> pd.DataFrame:
    """Loads and caches the 50 Startups dataset."""
    if STARTUPS_CSV_PATH.exists():
        return pd.read_csv(STARTUPS_CSV_PATH)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_enterprise_series() -> pd.DataFrame:
    """Loads and caches the enterprise multi-quarter financial dataset."""
    engine = get_engine()
    return engine.load_data()

@st.cache_data(ttl=3600)
def load_sample_batch_data() -> pd.DataFrame:
    """Loads and caches the 500 companies batch evaluation dataset."""
    if INPUT_500_CSV_PATH.exists():
        return pd.read_csv(INPUT_500_CSV_PATH)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_benchmark_catalog() -> list:
    """Loads catalog of all 50+ industry benchmark sectors."""
    catalog_path = Path(__file__).resolve().parent.parent / "data" / "benchmarks" / "catalog.json"
    if catalog_path.exists():
        import json
        with open(catalog_path, "r") as f:
            return json.load(f)
    return []

@st.cache_data(ttl=3600)
def load_benchmark_dataset(sector_slug: str) -> pd.DataFrame:
    """Loads a specific industry benchmark dataset from data/benchmarks/."""
    csv_path = Path(__file__).resolve().parent.parent / "data" / "benchmarks" / f"{sector_slug}.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return pd.DataFrame()

def get_benchmarks_zip_bytes() -> bytes:
    """Returns the zip archive bytes of all 50+ benchmark datasets."""
    zip_path = Path(__file__).resolve().parent.parent / "data" / "benchmarks_50_plus_sectors.zip"
    benchmarks_dir = Path(__file__).resolve().parent.parent / "data" / "benchmarks"
    raw_dir = Path(__file__).resolve().parent.parent / "data" / "raw"
    if not zip_path.exists() or zip_path.stat().st_size == 0:
        import zipfile
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for f in benchmarks_dir.glob("*.*"):
                z.write(f, arcname=f"benchmarks/{f.name}")
            for f in raw_dir.glob("*.csv"):
                z.write(f, arcname=f"raw/{f.name}")
    with open(zip_path, "rb") as f:
        return f.read()

