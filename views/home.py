import streamlit as st

from utils import art, ml
from utils.loaders import get_artifacts, get_data, get_metrics
from utils.theme import PALETTE, card, footer, h, html, kpi, section

df = get_data()
scaler, model, _ = get_artifacts()
m = get_metrics()
approval_rate = df[ml.TARGET].mean()

# ------------------------------------------------------------------ hero
left, right = st.columns([1.1, 1], gap="large", vertical_alignment="center")
with left:
    html(f"""
    <div class="hero-badge">✨ AI-powered · Logistic Regression · {m['roc_auc']:.0%} ROC-AUC</div>
    <div class="hero-title">Your loan verdict,<br><span class="grad">in a few seconds.</span></div>
    <div class="hero-sub">LoanLens reads an applicant's age, income, credit score, dependents and home
    ownership, then tells you how likely a bank is to say <b>yes</b> — and exactly <i>why</i>.</div>
    <br>
    """)
    b1, b2, _ = st.columns([1, 1, 0.4])
    with b1:
        st.page_link("views/eligibility.py", label="Check eligibility", icon=":material/rocket_launch:")
    with b2:
        st.page_link("views/insights.py", label="Explore the data", icon=":material/insights:")
with right:
    html(f'<div class="float">{art.img(art.bank_hero(), "100%", alt="Purple bank illustration")}</div>')

# ------------------------------------------------------------------ KPIs
st.write("")
k1, k2, k3, k4 = st.columns(4)
k1.markdown(kpi(f"{len(df):,}", "Applicants analysed"), unsafe_allow_html=True)
k2.markdown(kpi(f"{approval_rate:.1%}", "Historical approval rate"), unsafe_allow_html=True)
k3.markdown(kpi(f"{m['accuracy']:.1%}", "Hold-out accuracy"), unsafe_allow_html=True)
k4.markdown(kpi(f"{m['roc_auc']:.3f}", "ROC-AUC score"), unsafe_allow_html=True)

# ------------------------------------------------------------------ how it works
section("How it works", "Three quick steps from details to decision.")
c1, c2, c3 = st.columns(3, gap="large")
c1.markdown(card(art.img(art.icon_form(), "84px"), "Enter the details",
                 "Five simple inputs — age, income, credit score, dependents and whether the applicant owns a home.",
                 "STEP 01"), unsafe_allow_html=True)
c2.markdown(card(art.img(art.icon_model(), "84px"), "The model thinks",
                 "A tuned Logistic Regression, trained on 1,000 past applicants and balanced with SMOTE, scores the profile.",
                 "STEP 02"), unsafe_allow_html=True)
c3.markdown(card(art.img(art.icon_approved(), "84px"), "Get a clear answer",
                 "See the approval probability, which factors helped or hurt, and what-if tips to boost your odds.",
                 "STEP 03"), unsafe_allow_html=True)

# ------------------------------------------------------------------ what drives a decision
section("What drives a decision?", "Relative weight of each factor inside the trained model.")
coef = ml.coefficient_table(model)
total = coef["abs"].sum()
rows = ""
for _, r in coef.iterrows():
    share = r["abs"] / total
    arrow = "↑" if r["coef"] > 0 else "↓"
    rows += (f'<div class="bar-row"><div class="bar-label">{r["label"]}</div>'
             f'<div class="bar-track"><div class="bar-fill" style="width:{share * 100:.0f}%"></div></div>'
             f'<div class="bar-val">{arrow} {share:.0%}</div></div>')
l2, r2 = st.columns([1.3, 1], gap="large", vertical_alignment="center")
with l2:
    html(f'<div class="card">{rows}<p style="margin-top:.9rem">↑ raises the chance of approval · ↓ lowers it. '
         f'Credit score matters most; every extra dependent pulls the odds down.</p></div>')
with r2:
    html(f'<div class="float">{art.img(art.house_key(), "100%", alt="House and key illustration")}</div>')

# ------------------------------------------------------------------ skyline + palette
html(f'<div style="margin-top:2.2rem">{art.img(art.skyline(), "100%", alt="City skyline")}</div>')


def _is_light(hex_color: str) -> bool:
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return (0.299 * r + 0.587 * g + 0.114 * b) > 150


section("A little purple, everywhere", "Every shade used across LoanLens — hover to stretch a swatch.")
sw = "".join(
    f'<div class="sw" style="background:{c};color:{"#3B0764" if _is_light(c) else "#F3E8FF"}">{n}<br>{c}</div>'
    for n, c in PALETTE.items()
)
html(f'<div class="swatches">{sw}</div>')

footer()
