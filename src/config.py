from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"
MODELS_DIR = BASE_DIR / "models"
ARTIFACTS_DIR = MODELS_DIR / "artifacts"

STARTUPS_CSV_PATH = DATA_RAW_DIR / "50_Startups.csv"
INPUT_500_CSV_PATH = DATA_RAW_DIR / "input_500_companies.csv"
ENTERPRISE_DATA_PATH = DATA_PROCESSED_DIR / "enterprise_series.csv"

# Model Artifacts
MODEL_PKL_PATH = ARTIFACTS_DIR / "profit_prediction_model.pkl"
SCALER_PKL_PATH = ARTIFACTS_DIR / "profit_scaler.pkl"
METADATA_JSON_PATH = ARTIFACTS_DIR / "metadata.json"

# Core Features
CORE_FEATURES = ["R&D Spend", "Administration", "Marketing Spend"]
TARGET_FEATURE = "Profit"

# Currency & Formatting
CURRENCY_SYMBOL = "₹"

def format_currency(val: float, compact: bool = True) -> str:
    """Formats values in Indian Rupee format (Lakhs / Crores) or standard."""
    if compact:
        abs_val = abs(val)
        sign = "-" if val < 0 else ""
        if abs_val >= 1e7:
            return f"{sign}{CURRENCY_SYMBOL}{abs_val / 1e7:.2f} Cr"
        elif abs_val >= 1e5:
            return f"{sign}{CURRENCY_SYMBOL}{abs_val / 1e5:.2f} L"
        elif abs_val >= 1e3:
            return f"{sign}{CURRENCY_SYMBOL}{abs_val / 1e3:.1f} K"
        return f"{sign}{CURRENCY_SYMBOL}{abs_val:,.2f}"
    return f"{CURRENCY_SYMBOL}{val:,.2f}"

# UI Theme Tokens
PALETTE = {
    "primary": "#6366F1",     # Indigo
    "secondary": "#06B6D4",   # Cyan
    "accent": "#10B981",      # Emerald
    "warning": "#F59E0B",     # Amber
    "danger": "#EF4444",      # Rose
    "background": "#0F172A",  # Slate 900
    "card_bg": "rgba(30, 41, 59, 0.75)",
    "border": "rgba(148, 163, 184, 0.15)",
    "text": "#F8FAFC",
    "text_muted": "#94A3B8",
}
