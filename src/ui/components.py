import streamlit as st

def render_kpi_card(
    title: str,
    value: str,
    delta_str: str = "",
    is_positive: bool = True,
    subtitle: str = "",
    ci_str: str = "",
    icon: str = "📈"
):
    """Renders a sleek, modern KPI metric card with trend badges and uncertainty indicators."""
    trend_html = ""
    if delta_str:
        trend_class = "trend-up" if is_positive else "trend-down"
        arrow = "↑" if is_positive else "↓"
        trend_html = f'<span class="trend-pill {trend_class}">{arrow} {delta_str}</span>'

    ci_html = f'<span class="ci-pill">{ci_str}</span>' if ci_str else ""
    subtitle_html = f'<span style="color: #64748B; margin-left: auto; font-size: 0.76rem;">{subtitle}</span>' if subtitle else ""

    meta_elements = [el for el in [trend_html, ci_html, subtitle_html] if el]
    meta_html = f'<div class="kpi-meta">{" ".join(meta_elements)}</div>' if meta_elements else ""

    card_html = (
        f'<div class="kpi-card">'
        f'<div class="kpi-title"><span>{title}</span><span>{icon}</span></div>'
        f'<div class="kpi-value">{value}</div>'
        f'{meta_html}'
        f'</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

def render_narrative_box(text: str):
    """Renders the AI Executive Insight banner with pristine typography and clear readable paragraphs."""
    import re
    # Strip any stray markdown asterisks completely
    clean_text = text.replace("**", "").strip()

    # Split into paragraphs if separated by newlines
    paragraphs = [p.strip() for p in clean_text.split("\n\n") if p.strip()]
    if not paragraphs:
        paragraphs = [clean_text]

    formatted_paras = []
    for p in paragraphs:
        if p.startswith("Executive Outlook"):
            p = re.sub(r"^(Executive Outlook[^:]*:)", r'<strong style="color: #F8FAFC; font-weight: 700;">\1</strong>', p)
        elif p.startswith("Strategic Guidance:"):
            p = re.sub(r"^(Strategic Guidance:)", r'<strong style="color: #34D399; font-weight: 700;">💡 Strategic Guidance:</strong>', p)
        elif p.startswith("Risk Mitigation:"):
            p = re.sub(r"^(Risk Mitigation:)", r'<strong style="color: #F87171; font-weight: 700;">⚠️ Risk Mitigation:</strong>', p)
        formatted_paras.append(f'<p style="margin: 0 0 10px 0; line-height: 1.65; color: #CBD5E1; font-size: 0.94rem;">{p}</p>')

    body_html = "".join(formatted_paras)

    html = (
        f'<div class="narrative-box" style="padding: 1.25rem 1.4rem; border-radius: 12px; background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(99, 102, 241, 0.25); margin-bottom: 1.25rem;">'
        f'<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px; font-weight: 700; color: #818CF8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">'
        f'<span>🤖</span><span>AI Executive Brief & Decision Synthesis</span>'
        f'</div>'
        f'{body_html}'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def render_header(title: str, subtitle: str, badge: str = "Enterprise AI"):
    """Renders the application executive header."""
    html = (
        f'<div style="margin-bottom: 1.6rem; display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 1rem;">'
        f'<div>'
        f'<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">'
        f'<h1 style="font-size: 2.2rem; font-weight: 800; letter-spacing: -0.03em; margin: 0; background: linear-gradient(90deg, #FFFFFF 0%, #CBD5E1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</h1>'
        f'<span style="background: rgba(99,102,241,0.2); border: 1px solid rgba(99,102,241,0.4); color: #A5B4FC; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 999px; text-transform: uppercase;">{badge}</span>'
        f'</div>'
        f'<p style="color: #94A3B8; font-size: 0.95rem; margin: 0;">{subtitle}</p>'
        f'</div>'
        f'<div style="display: flex; gap: 8px;">'
        f'<span style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #34D399; font-size: 0.75rem; padding: 4px 10px; border-radius: 6px; font-weight: 600;">● Live Model Active</span>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

