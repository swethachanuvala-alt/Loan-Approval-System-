import plotly.graph_objects as go
import streamlit as st

from utils import ml
from utils.loaders import get_artifacts, get_metrics
from utils.theme import BAD, GOOD, footer, h, html, kpi, page_header, section, style_fig

scaler, model, source = get_artifacts()
m = get_metrics()

page_header("Model Lab", "A transparent look under the hood of the Logistic Regression model.")
if source == "retrained":
    st.info("The saved .pkl files weren't compatible with this environment, so the model was re-trained "
            "from the CSV using the same pipeline as the notebook.")

# ------------------------------------------------------------------ headline metrics
cols = st.columns(5)
for col, (label, key) in zip(cols, [("Accuracy", "accuracy"), ("Precision", "precision"), ("Recall", "recall"),
                                    ("F1 score", "f1"), ("ROC-AUC", "roc_auc")]):
    col.markdown(kpi(f"{m[key]:.3f}", label), unsafe_allow_html=True)
st.caption(f"Scored live on the {m['n_test']} hold-out applicants (20 % stratified split, random_state=42).")

# ------------------------------------------------------------------ confusion matrix + ROC
section("How well does it separate approvals from declines?")
c1, c2 = st.columns(2)
cm = m["cm"]
fig = go.Figure(go.Heatmap(
    z=cm, x=["Predicted declined", "Predicted approved"], y=["Actually declined", "Actually approved"],
    colorscale=[[0, "#2A1250"], [0.5, "#7E22CE"], [1, "#E9D5FF"]], showscale=False,
    text=cm, texttemplate="<b>%{text}</b>", textfont=dict(size=26, color="#fff"),
    hovertemplate="%{y} / %{x}: %{z}<extra></extra>",
))
fig.update_layout(title="Confusion matrix")
fig.update_yaxes(autorange="reversed")
c1.plotly_chart(style_fig(fig, legend=False), key="lab_cm")

fig = go.Figure()
fig.add_trace(go.Scatter(x=m["fpr"], y=m["tpr"], mode="lines", name=f"Model (AUC {m['roc_auc']:.3f})",
                         line=dict(color="#C084FC", width=4), fill="tozeroy", fillcolor="rgba(168,85,247,.25)"))
fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Random guess",
                         line=dict(color="#D946EF", dash="dash", width=2)))
fig.update_layout(title="ROC curve", xaxis_title="False-positive rate", yaxis_title="True-positive rate")
c2.plotly_chart(style_fig(fig), key="lab_roc")

# ------------------------------------------------------------------ coefficients
section("What the model learned", "Standardised coefficients — positive values push towards approval.")
coef = ml.coefficient_table(model).sort_values("coef")
fig = go.Figure(go.Bar(
    x=coef["coef"], y=coef["label"], orientation="h",
    marker=dict(color=[GOOD if v >= 0 else BAD for v in coef["coef"]], line=dict(color="rgba(243,232,255,.5)", width=1)),
    text=[f"{v:+.2f}" for v in coef["coef"]], textposition="outside",
))
fig.update_layout(title="Logistic Regression coefficients")
fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#E9D5FF")
st.plotly_chart(style_fig(fig, height=330, legend=False), key="lab_coef")

# ------------------------------------------------------------------ model comparison (from the notebook)
section("Why Logistic Regression?", "Six algorithms were tuned in the notebook — here is how they compared.")
comparison = [  # model, tuned test accuracy, 5-fold CV accuracy  (values from GGST_7.ipynb)
    ("Logistic Regression", 0.865, 0.91000),
    ("Random Forest", 0.850, 0.90750),
    ("SVM", 0.855, 0.90500),
    ("XGBoost", 0.855, 0.90375),
    ("KNN", 0.845, 0.90125),
    ("Decision Tree", 0.820, 0.89250),
]
fig = go.Figure()
fig.add_trace(go.Bar(name="Test accuracy", x=[r[0] for r in comparison], y=[r[1] * 100 for r in comparison], marker_color="#C084FC"))
fig.add_trace(go.Bar(name="5-fold CV accuracy", x=[r[0] for r in comparison], y=[r[2] * 100 for r in comparison], marker_color="#7E22CE"))
fig.update_layout(barmode="group", title="Tuned models — accuracy (%)", yaxis=dict(range=[75, 95]))
st.plotly_chart(style_fig(fig), key="lab_compare")

rows = "".join(
    f'<tr class="{"best" if i == 0 else ""}"><td>{n}</td><td>{t:.3f}</td><td>{c:.3f}</td></tr>'
    for i, (n, t, c) in enumerate(comparison)
)
html(f'<table class="dtable"><tr><th>Model</th><th>Test accuracy</th><th>CV accuracy</th></tr>{rows}</table>')
st.caption("Logistic Regression won on cross-validated accuracy and also posted the best untuned ROC-AUC — "
           "while staying simple enough to explain to an applicant.")

# ------------------------------------------------------------------ recipe
section("The training recipe")
html("""
<div class="card">
<span class="chip">80 / 20 stratified split</span><span class="chip">StandardScaler</span><span class="chip">SMOTE (train only)</span>
<span class="chip">Logistic Regression</span><span class="chip">C = 0.1</span><span class="chip">solver = newton-cg</span>
<span class="chip">max_iter = 2000</span><span class="chip">RandomizedSearchCV · 20 iters · 5-fold</span>
</div>
""")

footer()
