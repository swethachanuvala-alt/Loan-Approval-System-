import streamlit as st

from utils import art, ml
from utils.loaders import get_data
from utils.theme import footer, html, page_header, section

df = get_data()
page_header("About LoanLens", "From a Jupyter notebook to a deployed, purple-powered web app.")

left, right = st.columns([1.2, 1], gap="large", vertical_alignment="center")
with left:
    section("The project", "A machine-learning loan-approval predictor.")
    html("""
    <div class="tl">
      <div class="tl-item"><b>1 · Data</b><span>1,000 applicants · 5 features · no missing values · 78 % approved.</span></div>
      <div class="tl-item"><b>2 · Preparation</b><span>Stratified 80/20 split, standard scaling, SMOTE to balance the training classes.</span></div>
      <div class="tl-item"><b>3 · Modelling</b><span>Logistic Regression, Decision Tree, Random Forest, XGBoost, KNN &amp; SVM — all tuned with cross-validation.</span></div>
      <div class="tl-item"><b>4 · Selection</b><span>Logistic Regression won on CV accuracy and ROC-AUC, and is easy to explain.</span></div>
      <div class="tl-item"><b>5 · Deployment</b><span>Saved with joblib and served through this multipage Streamlit app.</span></div>
    </div>
    """)
with right:
    html(f'<div class="float">{art.img(art.coins_stack(), "100%", alt="Coins")}</div>')

section("Dataset dictionary")
desc = {
    "age": "Applicant age in years", "income": "Applicant income (4,000 – 100,000)",
    "credit_score": "Credit score (300 – 850)", "dependents": "Number of dependents (0 – 4)",
    "home_owner": "1 = owns a home, 0 = does not", "loan_approved": "Target — 1 = approved, 0 = declined",
}
rows = "".join(
    f"<tr><td><b>{c}</b></td><td>{df[c].dtype}</td><td>{df[c].min():,.0f} – {df[c].max():,.0f}</td><td>{d}</td></tr>"
    for c, d in desc.items()
)
html(f'<table class="dtable"><tr><th>Column</th><th>Type</th><th>Range</th><th>Meaning</th></tr>{rows}</table>')

section("Built with")
html("".join(f'<span class="chip">{t}</span>' for t in
             ["Python", "Streamlit", "scikit-learn", "imbalanced-learn", "pandas", "NumPy", "Plotly", "joblib", "Custom SVG art"]))

section("Good to know")
html("""
<div class="card">
<p>LoanLens is a learning project built on a small dataset. Its predictions describe statistical patterns in that data and are
<b>not</b> a real credit decision or financial advice. Real lenders weigh many more factors and must follow lending regulations.</p>
</div>
""")
html(f'<div style="margin-top:2rem">{art.img(art.skyline(), "100%", alt="Skyline")}</div>')
footer()
