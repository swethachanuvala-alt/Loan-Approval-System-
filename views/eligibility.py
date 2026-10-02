import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import art, ml
from utils.loaders import get_artifacts, get_data
from utils.theme import BAD, GOOD, h, html, page_header, style_fig, footer

df = get_data()
scaler, model, _ = get_artifacts()

page_header("Check Eligibility", "Describe the applicant — the model answers instantly and explains itself.")

lo, hi = df.min(), df.max()
left, right = st.columns([1, 1.3], gap="large")

# ------------------------------------------------------------------ input form
with left:
    with st.form("applicant_form"):
        st.markdown("#### 👤 Applicant details")
        age = st.slider("Age", int(lo["age"]), int(hi["age"]), 35)
        income = st.slider("Income", int(lo["income"]), int(hi["income"]), 30000, step=500,
                           help="Use the same currency & period as the training data (4,000 – 100,000).")
        credit = st.slider("Credit score", int(lo["credit_score"]), int(hi["credit_score"]), 650)
        dependents = st.select_slider("Number of dependents", options=[0, 1, 2, 3, 4], value=1)
        owner = st.radio("Owns a home?", ["Yes", "No"], horizontal=True)
        submitted = st.form_submit_button("Check my eligibility ✨")

    if submitted:
        applicant = dict(age=age, income=income, credit_score=credit,
                         dependents=dependents, home_owner=1 if owner == "Yes" else 0)
        prob, contrib, intercept = ml.predict_one(scaler, model, applicant)
        st.session_state["loan_result"] = dict(applicant=applicant, prob=prob, contrib=contrib, intercept=intercept)


# ------------------------------------------------------------------ helpers
def band(p: float) -> str:
    if p >= 0.85:
        return "Strong profile"
    if p >= 0.65:
        return "Good profile"
    if p >= 0.5:
        return "Borderline"
    if p >= 0.3:
        return "Needs work"
    return "High risk"


def prob_with(applicant: dict, **changes) -> float:
    return ml.predict_one(scaler, model, {**applicant, **changes})[0]


def curve(applicant: dict, feature: str, grid) -> np.ndarray:
    frame = pd.DataFrame([applicant] * len(grid))
    frame[feature] = grid
    return ml.predict_many(scaler, model, frame)


# ------------------------------------------------------------------ results
with right:
    res = st.session_state.get("loan_result")
    if not res:
        html(f"""
        <div class="card" style="text-align:center;padding:2rem 1.5rem">
          {art.img(art.house_key(), "78%")}
          <h4 style="font-size:1.4rem">Your result will appear here</h4>
          <p>Fill in the form and press <b>Check my eligibility</b>. You'll get a verdict, a probability gauge,
          a factor-by-factor explanation and personalised what-if tips.</p>
        </div>
        """)
    else:
        a, prob, contrib, intercept = res["applicant"], res["prob"], res["contrib"], res["intercept"]
        approved = prob >= 0.5
        icon = art.icon_approved() if approved else art.icon_declined()
        title = "Likely approved 🎉" if approved else "Likely declined"
        sub = (f"The model estimates a <b>{prob:.0%}</b> chance of approval."
               if approved else
               f"The model estimates only a <b>{prob:.0%}</b> chance of approval — see how to improve it below.")
        html(f"""
        <div class="verdict {'ok' if approved else 'no'}" style="display:flex;align-items:center;gap:1.2rem">
          <div style="flex:1">
            <div class="t">{title}</div>
            <div class="s">{sub}</div>
            <div style="margin-top:.8rem"><span class="pill">{band(prob)}</span><span class="pill">Decision threshold 50%</span></div>
          </div>
          <div style="width:112px">{art.img(icon, "112px")}</div>
        </div>
        """)

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            number=dict(suffix="%", font=dict(size=46, color="#F3E8FF", family="Outfit")),
            title=dict(text="Approval probability", font=dict(size=15, color="#D8B4FE")),
            gauge=dict(
                axis=dict(range=[0, 100], tickcolor="#D8B4FE"),
                bar=dict(color="#F3E8FF", thickness=0.22),
                bgcolor="rgba(0,0,0,0)",
                borderwidth=0,
                steps=[dict(range=[0, 30], color="#3B0764"), dict(range=[30, 50], color="#6B21A8"),
                       dict(range=[50, 70], color="#7E22CE"), dict(range=[70, 85], color="#A855F7"),
                       dict(range=[85, 100], color="#C084FC")],
                threshold=dict(line=dict(color="#D946EF", width=5), thickness=0.85, value=50),
            ),
        ))
        style_fig(gauge, height=260, legend=False)
        gauge.update_layout(margin=dict(l=30, r=30, t=50, b=0))
        st.plotly_chart(gauge, key="gauge_chart")

# ------------------------------------------------------------------ deep-dive tabs
res = st.session_state.get("loan_result")
if res:
    a, prob, contrib, intercept = res["applicant"], res["prob"], res["contrib"], res["intercept"]
    t1, t2, t3 = st.tabs(["🔍 Why this result", "🎛️ What-if explorer", "🚀 Boost your odds"])

    # ---- tab 1: contributions
    with t1:
        order = sorted(contrib, key=lambda k: contrib[k])
        fig = go.Figure(go.Bar(
            x=[contrib[k] for k in order],
            y=[ml.NICE_NAMES[k] for k in order],
            orientation="h",
            marker=dict(color=[GOOD if contrib[k] >= 0 else BAD for k in order],
                        line=dict(color="rgba(243,232,255,.5)", width=1)),
            text=[f"{contrib[k]:+.2f}" for k in order],
            textposition="outside",
            hovertemplate="%{y}: %{x:+.2f}<extra></extra>",
        ))
        fig.update_layout(title="How each factor moved the odds (log-odds contribution)")
        style_fig(fig, height=340, legend=False)
        fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#E9D5FF")
        st.plotly_chart(fig, key="contrib_chart")
        total = intercept + sum(contrib.values())
        st.caption(
            f"Light purple bars helped, fuchsia bars hurt — each measured against an *average* applicant in the training data. "
            f"Baseline {intercept:+.2f} + factors {sum(contrib.values()):+.2f} = log-odds {total:+.2f}, "
            f"which the logistic function turns into **{prob:.1%}**."
        )

    # ---- tab 2: what-if curves
    with t2:
        c1, c2 = st.columns(2)
        grid_c = np.arange(int(df["credit_score"].min()), int(df["credit_score"].max()) + 1, 10)
        grid_i = np.arange(int(df["income"].min()), int(df["income"].max()) + 1, 1000)
        for col, feat, grid, ttl, key in (
            (c1, "credit_score", grid_c, "Approval chance vs. credit score", "wi_credit"),
            (c2, "income", grid_i, "Approval chance vs. income", "wi_income"),
        ):
            probs = curve(a, feat, grid)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=grid, y=probs * 100, mode="lines", name="Approval %",
                                     line=dict(color="#C084FC", width=4, shape="spline"),
                                     fill="tozeroy", fillcolor="rgba(168,85,247,.22)"))
            fig.add_trace(go.Scatter(x=[a[feat]], y=[prob * 100], mode="markers", name="You",
                                     marker=dict(size=15, color="#F3E8FF", line=dict(color="#D946EF", width=4))))
            fig.add_hline(y=50, line=dict(color="#D946EF", dash="dash", width=1.5), annotation_text="50% threshold",
                          annotation_font_color="#F0ABFC")
            fig.update_layout(title=ttl, yaxis=dict(range=[0, 101], title="%"), xaxis_title=ml.NICE_NAMES[feat])
            style_fig(fig, height=340, legend=False)
            col.plotly_chart(fig, key=key)
        st.caption("Every other detail is held fixed while one factor moves — handy for seeing which lever matters most.")

    # ---- tab 3: improvement ideas
    with t3:
        ideas = []
        if a["credit_score"] < 850:
            for pts in (50, 100):
                new = min(850, a["credit_score"] + pts)
                ideas.append((f"Raise credit score by {pts} points (to {new})", prob_with(a, credit_score=new)))
        if a["income"] < 100000:
            new = min(100000, int(a["income"] * 1.25))
            ideas.append((f"Increase income by 25% (to {new:,})", prob_with(a, income=new)))
        if a["home_owner"] == 0:
            ideas.append(("Become a home owner", prob_with(a, home_owner=1)))
        if a["dependents"] > 0:
            ideas.append((f"If dependents were {a['dependents'] - 1} instead of {a['dependents']}", prob_with(a, dependents=a["dependents"] - 1)))
        ideas = [(t, p) for t, p in ideas if p - prob > 0.004]
        ideas.sort(key=lambda x: x[1], reverse=True)
        if not ideas:
            st.success("This profile is already near the top of what the model can score — nothing meaningful to improve. 🎉")
        else:
            st.markdown("**Model-based what-ifs** — each change is applied on its own to the current profile:")
            for text, p in ideas:
                html(f'<div class="tip"><b>{text}</b> → approval chance <b>{p:.0%}</b> ({(p - prob) * 100:+.1f} pts)</div>')
        st.caption("These are statistical patterns from a small demo dataset, not guarantees or financial advice.")

footer()
