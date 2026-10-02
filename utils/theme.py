"""Purple design system: palette, global CSS, small HTML helpers, Plotly styling."""
from __future__ import annotations

import streamlit as st

# Every shade of purple used across the app (light -> dark)
PALETTE = {
    "Lavender":   "#F3E8FF",
    "Lilac":      "#E9D5FF",
    "Orchid":     "#D8B4FE",
    "Mauve":      "#B794D6",
    "Wisteria":   "#C084FC",
    "Periwinkle": "#8B7CF6",
    "Amethyst":   "#A855F7",
    "Fuchsia":    "#D946EF",
    "Violet":     "#9333EA",
    "Indigo":     "#6D28D9",
    "Grape":      "#7E22CE",
    "Royal":      "#6B21A8",
    "Plum":       "#581C87",
    "Aubergine":  "#3B0764",
    "Midnight":   "#1E0B3A",
    "Ink":        "#140826",
}
SEQ = ["#E9D5FF", "#D8B4FE", "#C084FC", "#A855F7", "#9333EA", "#7E22CE", "#6B21A8", "#581C87"]
GOOD = "#C084FC"   # approved / positive
BAD = "#D946EF"    # declined / negative (fuchsia keeps us in the purple family)


def html(markup: str) -> None:
    """Render raw HTML. Blank lines / indentation would break Markdown's HTML blocks, so strip them."""
    clean = "\n".join(line.strip() for line in markup.splitlines() if line.strip())
    st.markdown(clean, unsafe_allow_html=True)


def h(markup: str) -> str:
    """Same clean-up but returns the string (for composing)."""
    return "\n".join(line.strip() for line in markup.splitlines() if line.strip())


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

:root{
  --lav:#F3E8FF; --lilac:#E9D5FF; --orchid:#D8B4FE; --wist:#C084FC; --ame:#A855F7;
  --vio:#9333EA; --grape:#7E22CE; --royal:#6B21A8; --plum:#581C87; --aub:#3B0764;
  --mid:#1E0B3A; --ink:#140826; --fuchsia:#D946EF; --peri:#8B7CF6;
}
html, body, [class*="css"], .stApp { font-family:'Inter',sans-serif; }
h1,h2,h3,h4,.display{ font-family:'Outfit',sans-serif !important; letter-spacing:-0.02em; }

/* ---------- page background ---------- */
.stApp{
  background:
    radial-gradient(1000px 520px at 85% -8%, rgba(168,85,247,.35), transparent 60%),
    radial-gradient(800px 480px at -8% 12%, rgba(109,40,217,.38), transparent 60%),
    radial-gradient(900px 600px at 50% 115%, rgba(217,70,239,.20), transparent 60%),
    linear-gradient(180deg,#140826 0%,#1E0B3A 55%,#2A1250 100%);
  background-attachment: fixed;
}
[data-testid="stHeader"]{ background:rgba(20,8,38,.55); backdrop-filter:blur(14px); }
#MainMenu, footer{ visibility:hidden; }
.block-container{ padding-top:3.2rem; padding-bottom:3rem; max-width:1180px; }
::-webkit-scrollbar{ width:10px; } ::-webkit-scrollbar-thumb{ background:linear-gradient(#7E22CE,#A855F7); border-radius:8px; }

/* ---------- hero ---------- */
.hero-badge{ display:inline-flex; gap:.5rem; align-items:center; padding:.38rem .9rem; border-radius:999px;
  background:rgba(168,85,247,.16); border:1px solid rgba(216,180,254,.35); color:#E9D5FF; font-size:.82rem; font-weight:600; }
.hero-title{ font-family:'Outfit',sans-serif; font-weight:800; font-size:3.55rem; line-height:1.04; margin:1rem 0 .9rem; color:#F3E8FF; }
.grad{ background:linear-gradient(90deg,#E9D5FF 0%,#C084FC 35%,#D946EF 65%,#8B7CF6 100%); background-size:220% auto;
  -webkit-background-clip:text; background-clip:text; color:transparent; animation:shine 6s linear infinite; }
@keyframes shine{ to{ background-position:220% center; } }
.hero-sub{ color:#D8B4FE; font-size:1.12rem; line-height:1.65; max-width:34rem; }
.float{ animation:floaty 5s ease-in-out infinite; }
@keyframes floaty{ 0%,100%{ transform:translateY(0);} 50%{ transform:translateY(-12px);} }

/* ---------- cards ---------- */
.card{ background:linear-gradient(145deg,rgba(88,28,135,.55),rgba(42,18,80,.65)); border:1px solid rgba(216,180,254,.18);
  border-radius:22px; padding:1.4rem 1.5rem; box-shadow:0 18px 50px rgba(20,8,38,.55), inset 0 1px 0 rgba(255,255,255,.06);
  backdrop-filter:blur(8px); transition:transform .25s ease, border-color .25s ease, box-shadow .25s ease; height:100%; }
.card:hover{ transform:translateY(-5px); border-color:rgba(192,132,252,.6); box-shadow:0 24px 60px rgba(147,51,234,.35); }
.card h4{ margin:.6rem 0 .35rem; color:#F3E8FF; font-size:1.18rem; }
.card p{ color:#D8B4FE; font-size:.95rem; line-height:1.55; margin:0; }
.step-no{ font-family:'Outfit'; font-weight:800; font-size:.8rem; letter-spacing:.14em; color:#C084FC; }

.kpi{ background:linear-gradient(145deg,rgba(126,34,206,.45),rgba(59,7,100,.7)); border:1px solid rgba(216,180,254,.2);
  border-radius:20px; padding:1.15rem 1.3rem; position:relative; overflow:hidden; }
.kpi::after{ content:""; position:absolute; right:-30px; top:-30px; width:110px; height:110px; border-radius:50%;
  background:radial-gradient(circle,rgba(217,70,239,.35),transparent 70%); }
.kpi .v{ font-family:'Outfit'; font-weight:800; font-size:2.15rem; color:#F3E8FF; line-height:1.1; }
.kpi .l{ color:#D8B4FE; font-size:.85rem; letter-spacing:.04em; margin-top:.2rem; }

.section-title{ font-family:'Outfit'; font-weight:700; font-size:1.9rem; color:#F3E8FF; margin:2.4rem 0 .3rem; }
.section-sub{ color:#C9A9F0; margin-bottom:1.1rem; }
.page-title{ font-family:'Outfit'; font-weight:800; font-size:2.5rem; color:#F3E8FF; margin:0; }
.page-sub{ color:#D8B4FE; font-size:1.05rem; margin:.3rem 0 1.4rem; }

/* ---------- verdict ---------- */
.verdict{ border-radius:24px; padding:1.5rem 1.7rem; text-align:left; position:relative; overflow:hidden; }
.verdict.ok{ background:linear-gradient(135deg,#7E22CE 0%,#A855F7 55%,#C084FC 100%); box-shadow:0 20px 60px rgba(168,85,247,.45); }
.verdict.no{ background:linear-gradient(135deg,#3B0764 0%,#6B21A8 50%,#A21CAF 100%); box-shadow:0 20px 60px rgba(162,28,175,.35); }
.verdict .t{ font-family:'Outfit'; font-weight:800; font-size:2.1rem; color:#fff; line-height:1.1; }
.verdict .s{ color:#F3E8FF; opacity:.92; margin-top:.4rem; font-size:1rem; }

.pill{ display:inline-block; padding:.28rem .8rem; border-radius:999px; font-size:.8rem; font-weight:600;
  background:rgba(255,255,255,.16); color:#fff; margin-right:.4rem; }
.tip{ background:rgba(168,85,247,.12); border-left:4px solid #A855F7; border-radius:12px; padding:.8rem 1rem; margin:.5rem 0;
  color:#EBDDFB; font-size:.95rem; }
.tip b{ color:#fff; }

/* ---------- bars (home) ---------- */
.bar-row{ display:flex; align-items:center; gap:.9rem; margin:.7rem 0; }
.bar-label{ width:130px; color:#E9D5FF; font-weight:500; font-size:.95rem; }
.bar-track{ flex:1; height:14px; border-radius:99px; background:rgba(255,255,255,.07); overflow:hidden; }
.bar-fill{ height:100%; border-radius:99px; background:linear-gradient(90deg,#6D28D9,#A855F7,#E9D5FF); }
.bar-val{ width:54px; text-align:right; color:#D8B4FE; font-variant-numeric:tabular-nums; font-size:.9rem; }

/* ---------- palette strip ---------- */
.swatches{ display:flex; border-radius:18px; overflow:hidden; box-shadow:0 14px 40px rgba(20,8,38,.6); }
.sw{ flex:1; padding:1.9rem .3rem .6rem; text-align:center; font-size:.68rem; font-weight:600; letter-spacing:.03em; transition:flex .3s ease; }
.sw:hover{ flex:2.2; }

/* ---------- timeline (about) ---------- */
.tl{ border-left:3px solid rgba(192,132,252,.5); margin-left:.6rem; padding-left:1.4rem; }
.tl-item{ position:relative; margin-bottom:1.25rem; }
.tl-item::before{ content:""; position:absolute; left:-1.95rem; top:.3rem; width:14px; height:14px; border-radius:50%;
  background:linear-gradient(135deg,#E9D5FF,#A855F7); box-shadow:0 0 0 4px rgba(168,85,247,.25); }
.tl-item b{ color:#F3E8FF; font-family:'Outfit'; font-size:1.05rem; }
.tl-item span{ display:block; color:#D8B4FE; font-size:.93rem; }

.footer{ text-align:center; color:#9F7ACB; font-size:.85rem; margin-top:3.2rem; padding-top:1.4rem; border-top:1px solid rgba(216,180,254,.15); }

/* ---------- Streamlit widgets ---------- */
.stButton>button, .stFormSubmitButton>button, .stDownloadButton>button{
  background:linear-gradient(90deg,#7E22CE,#A855F7,#D946EF); color:#fff; border:0; border-radius:14px; font-weight:700;
  padding:.7rem 1.4rem; box-shadow:0 10px 30px rgba(168,85,247,.45); transition:transform .2s ease, box-shadow .2s ease; }
.stButton>button:hover, .stFormSubmitButton>button:hover{ transform:translateY(-2px) scale(1.01); box-shadow:0 16px 40px rgba(217,70,239,.55); color:#fff; border:0; }
.stFormSubmitButton>button{ width:100%; }
[data-testid="stForm"]{ background:linear-gradient(145deg,rgba(88,28,135,.5),rgba(42,18,80,.6)); border:1px solid rgba(216,180,254,.2);
  border-radius:22px; padding:1.4rem; }
[data-testid="stPageLink-NavLink"]{ background:rgba(168,85,247,.18); border:1px solid rgba(216,180,254,.35); border-radius:14px; padding:.55rem 1rem; }
[data-testid="stPageLink-NavLink"]:hover{ background:rgba(168,85,247,.38); }
.chip{ display:inline-block; margin:.25rem .3rem .25rem 0; padding:.35rem .85rem; border-radius:999px; background:rgba(168,85,247,.18); border:1px solid rgba(216,180,254,.3); color:#E9D5FF; font-size:.85rem; font-weight:600; }
.dtable{ width:100%; border-collapse:separate; border-spacing:0; border-radius:16px; overflow:hidden; border:1px solid rgba(216,180,254,.2); }
.dtable th{ background:rgba(126,34,206,.55); color:#F3E8FF; text-align:left; padding:.7rem 1rem; font-family:Outfit; font-weight:600; }
.dtable td{ padding:.65rem 1rem; color:#E9D5FF; border-top:1px solid rgba(216,180,254,.12); background:rgba(42,18,80,.45); font-size:.93rem; }
.dtable tr:hover td{ background:rgba(88,28,135,.55); }
.dtable tr.best td{ background:rgba(168,85,247,.28); font-weight:600; }
.stTabs [data-baseweb="tab-list"]{ gap:.4rem; }
.stTabs [data-baseweb="tab"]{ background:rgba(168,85,247,.12); border-radius:12px 12px 0 0; padding:.5rem 1.1rem; }
.stTabs [aria-selected="true"]{ background:rgba(168,85,247,.35); }
[data-testid="stMetric"]{ background:linear-gradient(145deg,rgba(126,34,206,.4),rgba(59,7,100,.65)); border:1px solid rgba(216,180,254,.2);
  border-radius:18px; padding:.9rem 1.1rem; }
[data-testid="stDataFrame"]{ border-radius:14px; overflow:hidden; }
@media (max-width:760px){ .hero-title{ font-size:2.5rem; } .page-title{ font-size:2rem; } }
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------- html building blocks
def page_header(title: str, subtitle: str) -> None:
    html(f"""
    <div class="page-title"><span class="grad">{title}</span></div>
    <div class="page-sub">{subtitle}</div>
    """)


def section(title: str, subtitle: str = "") -> None:
    sub = f'<div class="section-sub">{subtitle}</div>' if subtitle else ""
    html(f'<div class="section-title">{title}</div>{sub}')


def kpi(value: str, label: str) -> str:
    return f'<div class="kpi"><div class="v">{value}</div><div class="l">{label}</div></div>'


def card(icon_html: str, title: str, text: str, step: str = "") -> str:
    step_html = f'<div class="step-no">{step}</div>' if step else ""
    return h(f'<div class="card">{icon_html}{step_html}<h4>{title}</h4><p>{text}</p></div>')


def footer() -> None:
    html('<div class="footer">💜 LoanLens · Logistic Regression loan-approval model · Built with Streamlit · '
         'For learning &amp; demonstration only — not financial advice.</div>')


# ---------------------------------------------------------------- plotly styling
def style_fig(fig, height: int = 380, legend: bool = True):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#E9D5FF", size=13),
        margin=dict(l=10, r=10, t=50, b=10),
        colorway=["#C084FC", "#D946EF", "#8B7CF6", "#E9D5FF", "#7E22CE", "#A855F7"],
        title=dict(font=dict(family="Outfit, sans-serif", size=18, color="#F3E8FF")),
        showlegend=legend,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#3B0764", font=dict(color="#F3E8FF")),
    )
    fig.update_xaxes(gridcolor="rgba(216,180,254,.12)", zerolinecolor="rgba(216,180,254,.2)", linecolor="rgba(216,180,254,.25)")
    fig.update_yaxes(gridcolor="rgba(216,180,254,.12)", zerolinecolor="rgba(216,180,254,.2)", linecolor="rgba(216,180,254,.25)")
    return fig
