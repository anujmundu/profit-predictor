import streamlit as st

def inject_custom_styles():
    """Injects modern 2026 CSS design system with glassmorphism, responsive cards, and glowing badges."""
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Global Dark Background with Ambient Gradients */
    .stApp {
        background-color: #0B0F19 !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(6, 182, 212, 0.10) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(15, 23, 42, 0.6) 0px, transparent 50%) !important;
        color: #F8FAFC !important;
    }

    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #0d1117 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1350px;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.4rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 12px 40px 0 rgba(79, 70, 229, 0.15);
    }

    /* KPI Metric Cards */
    .kpi-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 16px;
        padding: 1.25rem 1.4rem;
        position: relative;
        overflow: hidden;
        transition: all 0.25s ease-in-out;
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6366F1, #06B6D4);
        opacity: 0.8;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.35);
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.2);
    }

    .kpi-title {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94A3B8;
        margin-bottom: 0.4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }

    .kpi-meta {
        margin-top: 0.6rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.78rem;
    }

    /* Trend Badges */
    .trend-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        padding: 0.2rem 0.55rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .trend-up {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(52, 211, 153, 0.3);
    }

    .trend-down {
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(248, 113, 113, 0.3);
    }

    .ci-pill {
        background: rgba(99, 102, 241, 0.15);
        color: #A5B4FC;
        border: 1px solid rgba(165, 180, 252, 0.3);
        padding: 0.2rem 0.5rem;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
    }

    /* AI Executive Narrative Banner */
    .narrative-box {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.12) 0%, rgba(6, 182, 212, 0.08) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-left: 4px solid #6366F1;
        border-radius: 12px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 1.5rem;
        color: #E2E8F0;
        font-size: 0.92rem;
        line-height: 1.6;
    }

    /* Styled Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px;
        color: #94A3B8;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 0 1.2rem;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.25) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(99, 102, 241, 0.4) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0B1120;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Clean Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        border-color: #6366F1;
        box-shadow: 0 0 16px rgba(99, 102, 241, 0.4);
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
