import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import art, ml
from utils.loaders import get_data
from utils.theme import BAD, GOOD, footer, html, kpi, page_header, section, style_fig

df = get_data().copy()
page_header("Data Insights", "What 1,000 past loan applications reveal about who gets approved.")
html(f'<div style="margin:-.4rem 0 1.2rem">{art.img(art.skyline(), "100%", alt="Skyline")}</div>')

# ------------------------------------------------------------------ filters
with st.expander("🎚️ Filter the applicants", expanded=False):
    f1, f2 = st.columns(2)
    credit_rng = f1.slider("Credit score range", int(df.credit_score.min()), int(df.credit_score.max()),
                           (int(df.credit_score.min()), int(df.credit_score.max())))
    age_rng = f2.slider("Age range", int(df.age.min()), int(df.age.max()), (int(df.age.min()), int(df.age.max())))
    f3, f4 = st.columns(2)
    owners = f3.multiselect("Home ownership", ["Owner", "Non-owner"], default=["Owner", "Non-owner"])
    deps = f4.multiselect("Dependents", [0, 1, 2, 3, 4], default=[0, 1, 2, 3, 4])

owner_codes = [1 if o == "Owner" else 0 for o in owners]
view = df[
    df.credit_score.between(*credit_rng)
    & df.age.between(*age_rng)
    & df.home_owner.isin(owner_codes)
    & df.dependents.isin(deps)
]
if view.empty:
    st.warning("No applicants match these filters — widen them a little.")
    footer()
    st.stop()

# ------------------------------------------------------------------ KPIs
k1, k2, k3, k4 = st.columns(4)
k1.markdown(kpi(f"{len(view):,}", "Applicants in view"), unsafe_allow_html=True)
k2.markdown(kpi(f"{view.loan_approved.mean():.1%}", "Approval rate"), unsafe_allow_html=True)
k3.markdown(kpi(f"{view.credit_score.mean():.0f}", "Average credit score"), unsafe_allow_html=True)
k4.markdown(kpi(f"{view.income.median():,.0f}", "Median income"), unsafe_allow_html=True)

# ------------------------------------------------------------------ row 1
section("Who gets approved?")
c1, c2 = st.columns(2)

bands = pd.cut(view.credit_score, [299, 400, 500, 600, 700, 850],
               labels=["300–400", "401–500", "501–600", "601–700", "701–850"])
by_band = view.groupby(bands, observed=True).loan_approved.agg(["mean", "count"]).reset_index()
fig = go.Figure(go.Bar(
    x=by_band["credit_score"].astype(str), y=by_band["mean"] * 100,
    marker=dict(color=by_band["mean"], colorscale=[[0, "#581C87"], [0.5, "#A855F7"], [1, "#E9D5FF"]], line=dict(width=0)),
    text=[f"{v:.0%}" for v in by_band["mean"]], textposition="outside",
    customdata=by_band["count"], hovertemplate="%{x}: %{y:.1f}% approved (%{customdata} applicants)<extra></extra>",
))
fig.update_layout(title="Approval rate by credit-score band", yaxis=dict(title="% approved", range=[0, 112]))
c1.plotly_chart(style_fig(fig, legend=False), key="ins_band")

by_dep = view.groupby("dependents").loan_approved.agg(["mean", "count"]).reset_index()
fig = go.Figure(go.Bar(
    x=by_dep["dependents"].astype(str), y=by_dep["mean"] * 100,
    marker=dict(color=by_dep["mean"], colorscale=[[0, "#581C87"], [0.5, "#A855F7"], [1, "#E9D5FF"]], line=dict(width=0)),
    text=[f"{v:.0%}" for v in by_dep["mean"]], textposition="outside",
    customdata=by_dep["count"], hovertemplate="%{x} dependents: %{y:.1f}% approved (%{customdata} applicants)<extra></extra>",
))
fig.update_layout(title="Approval rate by number of dependents", xaxis_title="Dependents", yaxis=dict(title="% approved", range=[0, 112]))
c2.plotly_chart(style_fig(fig, legend=False), key="ins_dep")

# ------------------------------------------------------------------ row 2
c3, c4 = st.columns([1.4, 1])
fig = go.Figure()
for flag, name, colr in ((1, "Approved", GOOD), (0, "Declined", BAD)):
    fig.add_trace(go.Histogram(x=view.loc[view.loan_approved == flag, "income"], name=name,
                               marker_color=colr, opacity=0.72, nbinsx=30))
fig.update_layout(barmode="overlay", title="Income distribution by outcome", xaxis_title="Income", yaxis_title="Applicants")
c3.plotly_chart(style_fig(fig), key="ins_income")

owner_tbl = view.groupby("home_owner").loan_approved.mean().reindex([1, 0]).dropna()
fig = go.Figure(go.Pie(
    labels=["Owner" if i == 1 else "Non-owner" for i in owner_tbl.index], values=owner_tbl.values * 100,
    hole=0.62, marker=dict(colors=["#C084FC", "#6B21A8"], line=dict(color="#140826", width=3)),
    texttemplate="%{label}<br>%{value:.0f}%", textfont=dict(color="#fff"),
))
fig.update_layout(title="Approval rate: owners vs non-owners")
c4.plotly_chart(style_fig(fig, legend=False), key="ins_owner")

# ------------------------------------------------------------------ row 3
section("Digging deeper")
c5, c6 = st.columns([1.3, 1])
fig = go.Figure()
for flag, name, colr in ((1, "Approved", GOOD), (0, "Declined", BAD)):
    sub = view[view.loan_approved == flag]
    fig.add_trace(go.Scatter(x=sub.credit_score, y=sub.income, mode="markers", name=name,
                             marker=dict(size=7, color=colr, opacity=0.65, line=dict(width=0))))
fig.update_layout(title="Credit score vs. income", xaxis_title="Credit score", yaxis_title="Income")
c5.plotly_chart(style_fig(fig), key="ins_scatter")

corr = view.corr()
labels = [ml.NICE_NAMES.get(c, "Loan approved") for c in corr.columns]
fig = go.Figure(go.Heatmap(
    z=corr.values, x=labels, y=labels, zmin=-1, zmax=1,
    colorscale=[[0, "#1E0B3A"], [0.35, "#581C87"], [0.65, "#A855F7"], [1, "#F3E8FF"]],
    text=np.round(corr.values, 2), texttemplate="%{text}", textfont=dict(size=11),
    hovertemplate="%{y} × %{x}: %{z:.2f}<extra></extra>",
))
fig.update_layout(title="Correlation heat-map")
fig.update_yaxes(autorange="reversed")
c6.plotly_chart(style_fig(fig, legend=False), key="ins_corr")

# ------------------------------------------------------------------ raw data
with st.expander("📄 View & download the filtered data"):
    st.dataframe(view.reset_index(drop=True), hide_index=True)
    st.download_button("Download CSV", view.to_csv(index=False).encode("utf-8"), "filtered_loans.csv", "text/csv")

footer()
