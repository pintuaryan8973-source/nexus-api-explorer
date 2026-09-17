import re
from html import escape

import pandas as pd
import requests
import streamlit as st


# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="NEXUS API — Public API Explorer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

RAW_README = "https://raw.githubusercontent.com/public-apis/public-apis/master/README.md"


# =========================================================
# FALLBACK DATA
# =========================================================
FALLBACK = [
    {
        "Category": "Animals",
        "API": "Dog API",
        "Description": "Random dog images and breed data",
        "Auth": "No",
        "HTTPS": "Yes",
        "CORS": "Yes",
        "Link": "https://dog.ceo/dog-api/",
    },
    {
        "Category": "Books",
        "API": "Open Library",
        "Description": "Books, authors and editions data",
        "Auth": "No",
        "HTTPS": "Yes",
        "CORS": "Yes",
        "Link": "https://openlibrary.org/developers/api",
    },
    {
        "Category": "Development",
        "API": "GitHub",
        "Description": "GitHub repositories, users and organizations",
        "Auth": "OAuth",
        "HTTPS": "Yes",
        "CORS": "Yes",
        "Link": "https://docs.github.com/en/rest",
    },
    {
        "Category": "Programming",
        "API": "JSONPlaceholder",
        "Description": "Fake REST API for testing and prototyping",
        "Auth": "No",
        "HTTPS": "Yes",
        "CORS": "Yes",
        "Link": "https://jsonplaceholder.typicode.com/",
    },
    {
        "Category": "Weather",
        "API": "Open-Meteo",
        "Description": "Weather forecast data",
        "Auth": "No",
        "HTTPS": "Yes",
        "CORS": "Yes",
        "Link": "https://open-meteo.com/",
    },
]


# =========================================================
# DATA HELPERS
# =========================================================
def clean_md(text: str) -> str:
    text = re.sub(r"`", "", text)
    text = re.sub(r"\*\*", "", text)
    return text.strip()


def parse_api_cell(cell: str):
    match = re.search(r"\[([^\]]+)\]\((https?://[^)]+)\)", cell)
    if match:
        return clean_md(match.group(1)), match.group(2).strip()
    return clean_md(cell), ""


@st.cache_data(ttl=3600)
def load_catalog():
    try:
        response = requests.get(RAW_README, timeout=15)
        response.raise_for_status()

        current_category = None
        rows = []

        for line in response.text.splitlines():
            if line.startswith("### "):
                current_category = clean_md(line[4:])
                continue

            if not current_category or not line.startswith("|"):
                continue

            if "---" in line or "API | Description" in line or "| API |" in line:
                continue

            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) < 4:
                continue

            name, url = parse_api_cell(parts[0])
            if not name or not url:
                continue

            rows.append(
                {
                    "Category": current_category,
                    "API": name,
                    "Description": clean_md(parts[1]) if len(parts) > 1 else "",
                    "Auth": clean_md(parts[2]) if len(parts) > 2 else "Unknown",
                    "HTTPS": clean_md(parts[3]) if len(parts) > 3 else "Unknown",
                    "CORS": clean_md(parts[4]) if len(parts) > 4 else "Unknown",
                    "Link": url,
                }
            )

        if rows:
            return pd.DataFrame(rows), True

    except Exception:
        pass

    return pd.DataFrame(FALLBACK), False


df, live = load_catalog()


# =========================================================
# CSS — ADVANCED NEXUS DESIGN
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #05070d;
    --panel: rgba(14, 18, 31, .76);
    --panel2: rgba(10, 14, 24, .92);
    --line: rgba(255,255,255,.08);
    --muted: #8d98ad;
    --text: #f6f8fc;
    --cyan: #22d3ee;
    --blue: #5b7cff;
    --violet: #8b5cf6;
    --green: #32e08c;
}

html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(91,124,255,.13), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(34,211,238,.10), transparent 28%),
        radial-gradient(circle at 50% 100%, rgba(139,92,246,.08), transparent 35%),
        var(--bg);
    color: var(--text);
}

.block-container {
    max-width: 1500px;
    padding-top: 1.3rem;
    padding-bottom: 3rem;
}

[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

/* TOP BAR */
.topbar {
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:20px;
    padding:14px 18px;
    margin-bottom:18px;
    border:1px solid var(--line);
    border-radius:18px;
    background:rgba(8,11,19,.70);
    backdrop-filter: blur(18px);
    box-shadow: 0 18px 50px rgba(0,0,0,.22);
}

.brand-wrap {
    display:flex;
    align-items:center;
    gap:12px;
}

.logo-box {
    width:40px;
    height:40px;
    display:grid;
    place-items:center;
    border-radius:12px;
    background:linear-gradient(145deg, var(--blue), var(--violet));
    box-shadow:0 0 30px rgba(91,124,255,.28);
    font-weight:900;
}

.brand {
    font-family:"Space Grotesk", sans-serif;
    font-weight:700;
    letter-spacing:.4px;
}

.brand small {
    display:block;
    font-family:"Inter", sans-serif;
    color:var(--muted);
    font-size:.68rem;
    font-weight:500;
    margin-top:1px;
}

.live-pill {
    display:inline-flex;
    align-items:center;
    gap:8px;
    font-size:.78rem;
    padding:8px 12px;
    border-radius:999px;
    color:#c9ffe0;
    border:1px solid rgba(50,224,140,.18);
    background:rgba(50,224,140,.08);
}

.dot {
    width:8px;
    height:8px;
    border-radius:50%;
    background:var(--green);
    box-shadow:0 0 14px var(--green);
}

/* HERO */
.hero {
    position:relative;
    overflow:hidden;
    border:1px solid var(--line);
    border-radius:30px;
    padding:58px 52px;
    margin-bottom:24px;
    background:
        linear-gradient(135deg, rgba(17,23,42,.96), rgba(8,12,22,.92));
    box-shadow: 0 30px 90px rgba(0,0,0,.30);
}

.hero:before {
    content:"";
    position:absolute;
    width:520px;
    height:520px;
    border-radius:50%;
    right:-180px;
    top:-240px;
    background:radial-gradient(circle, rgba(34,211,238,.22), transparent 68%);
    pointer-events:none;
}

.hero:after {
    content:"";
    position:absolute;
    inset:0;
    opacity:.13;
    background-image:
      linear-gradient(rgba(255,255,255,.08) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,.08) 1px, transparent 1px);
    background-size:34px 34px;
    mask-image:linear-gradient(to right, transparent, black 25%, black 100%);
    pointer-events:none;
}

.hero-grid {
    position:relative;
    z-index:2;
    display:grid;
    grid-template-columns:1.25fr .75fr;
    gap:46px;
    align-items:center;
}

.eyebrow {
    display:inline-flex;
    align-items:center;
    gap:8px;
    padding:7px 11px;
    border:1px solid rgba(91,124,255,.26);
    border-radius:999px;
    background:rgba(91,124,255,.08);
    color:#b9c6ff;
    font-size:.75rem;
    font-weight:700;
    letter-spacing:.7px;
}

.hero h1 {
    font-family:"Space Grotesk", sans-serif;
    font-size:clamp(3rem, 6vw, 5.3rem);
    line-height:.95;
    letter-spacing:-3px;
    margin:18px 0 20px 0;
}

.gradient-text {
    background:linear-gradient(90deg, #ffffff 2%, #a9c6ff 35%, #65e6ff 68%, #b69cff);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero p {
    max-width:760px;
    color:#aab5c8;
    line-height:1.75;
    font-size:1.03rem;
    margin:0;
}

.hero-actions {
    display:flex;
    flex-wrap:wrap;
    gap:10px;
    margin-top:24px;
}

.tag {
    padding:8px 11px;
    border-radius:10px;
    border:1px solid rgba(255,255,255,.08);
    background:rgba(255,255,255,.035);
    color:#dce4f2;
    font-size:.78rem;
}

.terminal {
    border:1px solid rgba(255,255,255,.08);
    border-radius:20px;
    overflow:hidden;
    background:#080b13;
    box-shadow:0 24px 70px rgba(0,0,0,.36);
    transform:rotate(1deg);
}

.terminal-head {
    display:flex;
    align-items:center;
    gap:7px;
    padding:12px 14px;
    background:#0d111c;
    border-bottom:1px solid rgba(255,255,255,.06);
}

.tdot { width:9px; height:9px; border-radius:50%; }
.r { background:#ff6b6b; }
.y { background:#ffd166; }
.g { background:#32e08c; }

.terminal-body {
    padding:20px;
    min-height:220px;
    font-family:Consolas, monospace;
    color:#cfe9ff;
    font-size:.84rem;
    line-height:1.85;
}

.t-muted { color:#667188; }
.t-cyan { color:#5ee7ff; }
.t-green { color:#6df0a7; }
.t-violet { color:#ae94ff; }

/* KPI */
.kpi {
    padding:20px 22px;
    border:1px solid var(--line);
    border-radius:18px;
    background:linear-gradient(145deg, rgba(255,255,255,.045), rgba(255,255,255,.018));
    min-height:116px;
    box-shadow:0 14px 40px rgba(0,0,0,.12);
}

.kpi-label {
    color:var(--muted);
    font-size:.72rem;
    text-transform:uppercase;
    font-weight:700;
    letter-spacing:.9px;
}

.kpi-value {
    font-family:"Space Grotesk", sans-serif;
    font-size:2.15rem;
    font-weight:700;
    margin:5px 0 2px 0;
}

.kpi-note {
    color:#6f7a8d;
    font-size:.72rem;
}

/* SECTION */
.section-head {
    display:flex;
    justify-content:space-between;
    align-items:end;
    margin:34px 0 14px 0;
}

.section-title {
    font-family:"Space Grotesk", sans-serif;
    font-size:1.65rem;
    font-weight:700;
    letter-spacing:-.5px;
}

.section-sub {
    color:var(--muted);
    font-size:.87rem;
    margin-top:4px;
}

/* FEATURE CARDS */
.feature {
    min-height:150px;
    padding:20px;
    border-radius:18px;
    border:1px solid var(--line);
    background:rgba(255,255,255,.025);
    transition:.2s ease;
}

.feature:hover {
    transform:translateY(-3px);
    border-color:rgba(91,124,255,.30);
    background:rgba(91,124,255,.045);
}

.feature-num {
    color:#64718a;
    font-size:.70rem;
    font-weight:800;
    letter-spacing:1px;
}

.feature-title {
    margin-top:22px;
    font-family:"Space Grotesk", sans-serif;
    font-size:1.02rem;
    font-weight:700;
}

.feature-text {
    margin-top:6px;
    color:#8f9bad;
    font-size:.82rem;
    line-height:1.6;
}

/* API CARD */
.api-card {
    position:relative;
    padding:22px;
    margin:10px 0 8px 0;
    border-radius:20px;
    border:1px solid var(--line);
    background:
        linear-gradient(145deg, rgba(18,24,40,.88), rgba(9,13,23,.88));
    box-shadow:0 12px 35px rgba(0,0,0,.13);
    transition:.2s ease;
}

.api-card:hover {
    transform:translateY(-2px);
    border-color:rgba(34,211,238,.25);
    box-shadow:0 20px 45px rgba(0,0,0,.20);
}

.api-top {
    display:flex;
    justify-content:space-between;
    gap:18px;
}

.api-name {
    font-family:"Space Grotesk", sans-serif;
    font-size:1.25rem;
    font-weight:700;
    margin-bottom:7px;
}

.api-desc {
    color:#96a2b6;
    line-height:1.6;
    font-size:.88rem;
}

.badges {
    margin-top:14px;
}

.badge {
    display:inline-block;
    margin:4px 5px 0 0;
    padding:5px 9px;
    border:1px solid rgba(255,255,255,.08);
    border-radius:8px;
    background:rgba(255,255,255,.035);
    color:#c8d1df;
    font-size:.70rem;
}

.footer-box {
    margin-top:42px;
    padding:26px;
    border-top:1px solid var(--line);
    text-align:center;
    color:#687386;
    font-size:.78rem;
}

div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] > div > div {
    background:#0c111d !important;
    border-color:rgba(255,255,255,.08) !important;
    border-radius:12px !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color:rgba(34,211,238,.40) !important;
    box-shadow:0 0 0 1px rgba(34,211,238,.18) !important;
}

.stButton > button,
.stLinkButton > a {
    border-radius:11px !important;
    border:1px solid rgba(91,124,255,.28) !important;
    background:linear-gradient(135deg, rgba(91,124,255,.17), rgba(139,92,246,.14)) !important;
    color:#eef3ff !important;
    transition:.2s ease !important;
}

.stLinkButton > a:hover {
    border-color:rgba(34,211,238,.35) !important;
    transform:translateY(-1px);
}

@media (max-width: 900px) {
    .hero-grid {
        grid-template-columns:1fr;
    }

    .hero {
        padding:34px 24px;
    }

    .hero h1 {
        letter-spacing:-1.8px;
    }

    .terminal {
        transform:none;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# TOPBAR
# =========================================================
status_text = "LIVE CATALOG" if live else "FALLBACK MODE"

st.markdown(
    f"""
<div class="topbar">
    <div class="brand-wrap">
        <div class="logo-box">N</div>
        <div class="brand">
            NEXUS API
            <small>Public API Intelligence Explorer</small>
        </div>
    </div>

    <div class="live-pill">
        <span class="dot"></span>
        {status_text}
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HERO
# =========================================================
st.markdown(
    f"""
<div class="hero">
  <div class="hero-grid">

    <div>
      <div class="eyebrow">⚡ API DISCOVERY ENGINE</div>

      <h1>
        Find the API.<br>
        <span class="gradient-text">Build anything.</span>
      </h1>

      <p>
        Explore {len(df):,}+ public APIs from one intelligent dashboard.
        Search by use-case, filter by authentication, inspect HTTPS and CORS,
        then jump directly into the documentation.
      </p>

      <div class="hero-actions">
        <span class="tag">Python</span>
        <span class="tag">Web Apps</span>
        <span class="tag">AI / ML</span>
        <span class="tag">Security</span>
        <span class="tag">Automation</span>
        <span class="tag">Data Projects</span>
      </div>
    </div>

    <div class="terminal">
      <div class="terminal-head">
        <span class="tdot r"></span>
        <span class="tdot y"></span>
        <span class="tdot g"></span>
      </div>

      <div class="terminal-body">
        <div><span class="t-muted">$</span> nexus search <span class="t-cyan">weather</span></div>
        <div><span class="t-green">✓</span> catalog connected</div>
        <div><span class="t-green">✓</span> {len(df):,} APIs indexed</div>
        <div><span class="t-violet">→</span> filtering secure endpoints</div>
        <div><span class="t-muted">status:</span> ready</div>
        <br>
        <div class="t-muted"># Build faster. Search smarter.</div>
        <div><span class="t-cyan">GET</span> /discover/api</div>
        <div><span class="t-green">200 OK</span></div>
      </div>
    </div>

  </div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# KPI ROW
# =========================================================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">Total APIs</div>
            <div class="kpi-value">{len(df):,}</div>
            <div class="kpi-note">Indexed from catalog</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">Categories</div>
            <div class="kpi-value">{df["Category"].nunique()}</div>
            <div class="kpi-note">Different API domains</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k3:
    secure_count = int(
        df["HTTPS"].astype(str).str.lower().isin(["yes", "true"]).sum()
    )
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">HTTPS APIs</div>
            <div class="kpi-value">{secure_count:,}</div>
            <div class="kpi-note">Secure endpoints detected</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k4:
    no_auth_count = int(
        df["Auth"].astype(str).str.lower().isin(["no", "", "none"]).sum()
    )
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">No Auth</div>
            <div class="kpi-value">{no_auth_count:,}</div>
            <div class="kpi-note">Quick-start friendly</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# FEATURES
# =========================================================
st.markdown(
    """
<div class="section-head">
  <div>
    <div class="section-title">Built for developers</div>
    <div class="section-sub">Everything you need to discover your next integration.</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

f1, f2, f3, f4 = st.columns(4)

feature_data = [
    ("01", "Instant Discovery", "Search API names, descriptions and categories instantly."),
    ("02", "Smart Filters", "Narrow results using category and authentication requirements."),
    ("03", "Security Signals", "See HTTPS and CORS support before opening the docs."),
    ("04", "Direct Launch", "Jump straight from discovery into official API documentation."),
]

for col, item in zip((f1, f2, f3, f4), feature_data):
    num, title, text = item
    with col:
        st.markdown(
            f"""
            <div class="feature">
                <div class="feature-num">{num}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-text">{text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# SEARCH / FILTER AREA
# =========================================================
st.markdown(
    """
<div class="section-head">
  <div>
    <div class="section-title">Explore the catalog</div>
    <div class="section-sub">Search by idea, category, technology or use-case.</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns([2.4, 1.25, 1.25, .8])

with c1:
    query = st.text_input(
        "Search APIs",
        placeholder="Try: weather, AI, finance, books, security...",
    )

with c2:
    category_options = ["All"] + sorted(
        df["Category"].dropna().astype(str).unique().tolist()
    )
    category = st.selectbox("Category", category_options)

with c3:
    auth_options = ["All"] + sorted(
        df["Auth"].dropna().astype(str).unique().tolist()
    )
    auth = st.selectbox("Authentication", auth_options)

with c4:
    result_limit = st.selectbox("Show", [12, 24, 48, 96], index=1)


# =========================================================
# FILTERING
# =========================================================
filtered = df.copy()

if query:
    q = query.strip().lower()
    filtered = filtered[
        filtered["API"].astype(str).str.lower().str.contains(q, na=False, regex=False)
        | filtered["Description"].astype(str).str.lower().str.contains(q, na=False, regex=False)
        | filtered["Category"].astype(str).str.lower().str.contains(q, na=False, regex=False)
    ]

if category != "All":
    filtered = filtered[filtered["Category"] == category]

if auth != "All":
    filtered = filtered[filtered["Auth"].astype(str) == auth]


# =========================================================
# RESULTS HEADER
# =========================================================
st.markdown(
    f"""
<div class="section-head">
  <div>
    <div class="section-title">Results</div>
    <div class="section-sub">{len(filtered):,} APIs match your current filters.</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# RESULTS GRID
# =========================================================
if filtered.empty:
    st.info("No API matched your current search and filters.")

else:
    rows = filtered.head(result_limit).reset_index(drop=True)

    for start in range(0, len(rows), 2):
        left, right = st.columns(2)

        for col, idx in zip((left, right), (start, start + 1)):
            if idx >= len(rows):
                continue

            row = rows.iloc[idx]

            api_name = escape(str(row["API"]))
            desc = escape(str(row["Description"]))
            cat = escape(str(row["Category"]))
            auth_value = escape(str(row["Auth"]))
            https_value = escape(str(row["HTTPS"]))
            cors_value = escape(str(row["CORS"]))

            with col:
                st.markdown(
                    f"""
                    <div class="api-card">
                        <div class="api-name">{api_name}</div>
                        <div class="api-desc">{desc}</div>

                        <div class="badges">
                            <span class="badge">{cat}</span>
                            <span class="badge">Auth: {auth_value}</span>
                            <span class="badge">HTTPS: {https_value}</span>
                            <span class="badge">CORS: {cors_value}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.link_button(
                    f"Open {row['API']} ↗",
                    str(row["Link"]),
                    use_container_width=True,
                )


# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
<div class="footer-box">
    NEXUS API • Built with Python + Streamlit • Data powered by public-apis/public-apis
    <br><br>
    Discover faster. Build smarter. Ship more.
</div>
""",
    unsafe_allow_html=True,
)
