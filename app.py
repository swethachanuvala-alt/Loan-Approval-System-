"""
LoanLens — Loan Approval Predictor
Entry point:  streamlit run app.py
"""
import streamlit as st

st.set_page_config(
    page_title="LoanLens · Loan Approval Predictor",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from utils.theme import inject_css  # noqa: E402  (must come after set_page_config)

inject_css()

pages = [
    st.Page("views/home.py", title="Home", icon=":material/home:", default=True),
    st.Page("views/eligibility.py", title="Check Eligibility", icon=":material/verified_user:"),
    st.Page("views/insights.py", title="Insights", icon=":material/insights:"),
    st.Page("views/model_lab.py", title="Model Lab", icon=":material/science:"),
    st.Page("views/about.py", title="About", icon=":material/info:"),
]

try:
    nav = st.navigation(pages, position="top")   # modern top navigation bar
except TypeError:                                  # older Streamlit -> sidebar menu
    nav = st.navigation(pages)

nav.run()
