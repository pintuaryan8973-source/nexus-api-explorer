import re
import json
import socket
import time
from datetime import datetime
import ipaddress
import hashlib
from collections import Counter
from html import escape
from urllib.parse import urlparse

import pandas as pd
import requests
import streamlit as st


# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="NEXUS API — Intelligent Public API Explorer",
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



# =========================================================
# INTELLIGENT RECOMMENDER
# =========================================================
STOP_WORDS = {
    "i", "me", "my", "want", "to", "build", "make", "create", "need", "a", "an",
    "the", "for", "with", "using", "app", "application", "project", "website",
    "system", "tool", "please", "mujhe", "banana", "banani", "hai", "ka", "ki",
    "ke", "liye", "ek", "chahiye", "karna", "krna", "main", "me", "aur", "or",
}

INTENT_MAP = {
    "weather": ["weather", "forecast", "temperature", "climate", "rain", "storm"],
    "finance": ["finance", "stock", "stocks", "market", "money", "currency", "forex", "bank"],
    "cryptocurrency": ["crypto", "bitcoin", "ethereum", "coin", "blockchain"],
    "security": ["security", "cyber", "cybersecurity", "threat", "malware", "vulnerability"],
    "books": ["book", "books", "author", "library", "novel"],
    "music": ["music", "song", "songs", "artist", "spotify", "audio"],
    "movies": ["movie", "movies", "film", "cinema", "tv", "series"],
    "jobs": ["job", "jobs", "career", "hiring", "employment"],
    "news": ["news", "headlines", "article", "articles"],
    "sports": ["sport", "sports", "football", "cricket", "basketball", "tennis"],
    "animals": ["animal", "animals", "dog", "cat", "pet"],
    "food": ["food", "recipe", "recipes", "meal", "nutrition"],
    "health": ["health", "medical", "medicine", "fitness"],
    "machine learning": ["machine learning", "ml", "ai", "artificial intelligence", "model"],
    "programming": ["programming", "developer", "coding", "code", "github"],
    "science": ["science", "space", "nasa", "astronomy", "research"],
    "maps": ["map", "maps", "location", "geo", "geolocation", "places"],
}


def tokenize(text: str):
    words = re.findall(r"[a-zA-Z0-9+#.]+", text.lower())
    return [w for w in words if len(w) > 1 and w not in STOP_WORDS]


def detect_intents(text: str):
    lower = text.lower()
    detected = []
    for intent, terms in INTENT_MAP.items():
        if any(term in lower for term in terms):
            detected.append(intent)
    return detected


def recommend_apis(data: pd.DataFrame, idea: str, beginner_mode=True, top_n=8):
    tokens = tokenize(idea)
    intents = detect_intents(idea)
    if not tokens and not intents:
        return pd.DataFrame()

    token_counts = Counter(tokens)
    rows = []

    for _, row in data.iterrows():
        api = str(row["API"])
        category = str(row["Category"])
        desc = str(row["Description"])
        auth = str(row["Auth"])
        https = str(row["HTTPS"])

        score = 0.0
        reasons = []
        matched = []

        for token, count in token_counts.items():
            if token in api.lower():
                score += 5.0 * count
                matched.append(token)
            elif token in category.lower():
                score += 4.0 * count
                matched.append(token)
            elif token in desc.lower():
                score += 2.0 * count
                matched.append(token)

        if matched:
            reasons.append("matches: " + ", ".join(sorted(set(matched))[:4]))

        haystack = f"{api} {category} {desc}".lower()
        for intent in intents:
            intent_terms = [intent] + INTENT_MAP.get(intent, [])
            if any(term in category.lower() for term in intent_terms):
                score += 8.0
                reasons.append(f"{intent} category")
            elif any(term in haystack for term in intent_terms):
                score += 3.0
                reasons.append(f"{intent} related")

        if https.strip().lower() in {"yes", "true"}:
            score += 1.5
            reasons.append("HTTPS")

        if beginner_mode and auth.strip().lower() in {"no", "", "none"}:
            score += 2.5
            reasons.append("no API key")

        if 15 <= len(desc) <= 180:
            score += 0.4

        if score > 0:
            item = row.to_dict()
            item["Score"] = round(score, 2)
            item["Why"] = " • ".join(dict.fromkeys(reasons)) if reasons else "relevant match"
            rows.append(item)

    if not rows:
        return pd.DataFrame()

    return (
        pd.DataFrame(rows)
        .sort_values(["Score", "API"], ascending=[False, True])
        .head(top_n)
        .reset_index(drop=True)
    )

df, live = load_catalog()


# =========================================================
# FAVORITES + SAVED COLLECTIONS
# =========================================================
if "favorites" not in st.session_state:
    st.session_state.favorites = {}

if "collections" not in st.session_state:
    st.session_state.collections = {}

if "request_history" not in st.session_state:
    st.session_state.request_history = []


def stable_id(value: str) -> str:
    return hashlib.sha1(str(value).encode("utf-8")).hexdigest()[:12]


def api_to_record(row) -> dict:
    return {
        "Category": str(row.get("Category", "")),
        "API": str(row.get("API", "")),
        "Description": str(row.get("Description", "")),
        "Auth": str(row.get("Auth", "")),
        "HTTPS": str(row.get("HTTPS", "")),
        "CORS": str(row.get("CORS", "")),
        "Link": str(row.get("Link", "")),
    }


def add_favorite(row):
    record = api_to_record(row)
    if record["Link"]:
        st.session_state.favorites[record["Link"]] = record


def remove_favorite(link: str):
    st.session_state.favorites.pop(link, None)


def add_to_collection(collection_name: str, record: dict):
    name = collection_name.strip()
    if not name:
        return False

    if name not in st.session_state.collections:
        st.session_state.collections[name] = {}

    link = str(record.get("Link", "")).strip()
    if not link:
        return False

    st.session_state.collections[name][link] = record
    return True


def remove_from_collection(collection_name: str, link: str):
    items = st.session_state.collections.get(collection_name, {})
    items.pop(link, None)


def build_library_export() -> str:
    payload = {
        "version": 1,
        "favorites": list(st.session_state.favorites.values()),
        "collections": {
            name: list(items.values())
            for name, items in st.session_state.collections.items()
        },
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)



def safe_auth_placeholder(auth_type: str):
    if auth_type == "Bearer Token":
        return {"Authorization": "Bearer <YOUR_TOKEN>"}
    if auth_type == "X-API-Key":
        return {"X-API-Key": "<YOUR_API_KEY>"}
    if auth_type == "API Key (Authorization)":
        return {"Authorization": "<YOUR_API_KEY>"}
    return {}


def build_code_snippets(method: str, url: str, params: dict, custom_headers: dict, auth_type: str, json_body):
    method = method.upper().strip()
    safe_headers = {str(k): str(v) for k, v in custom_headers.items()}
    safe_headers.update(safe_auth_placeholder(auth_type))

    # Python requests
    py_lines = [
        "import requests",
        "",
        f'url = {url!r}',
        f"params = {repr(params)}",
        f"headers = {repr(safe_headers)}",
    ]
    if method in {"POST", "PUT", "PATCH", "DELETE"} and json_body is not None:
        py_lines.append(f"payload = {repr(json_body)}")
        py_lines.append(
            f'response = requests.request("{method}", url, params=params, headers=headers, json=payload, timeout=20)'
        )
    else:
        py_lines.append(
            f'response = requests.request("{method}", url, params=params, headers=headers, timeout=20)'
        )
    py_lines += ["", "print(response.status_code)", "print(response.text)"]
    python_code = "\n".join(py_lines)

    # JavaScript fetch
    js_headers = dict(safe_headers)
    if method in {"POST", "PUT", "PATCH", "DELETE"} and json_body is not None:
        js_headers.setdefault("Content-Type", "application/json")

    query_string = ""
    if params:
        query_string = "?" + "&".join(
            f"{k}={v}" for k, v in params.items()
        )

    js_options = [
        f'method: "{method}"',
        f"headers: {json.dumps(js_headers, ensure_ascii=False)}",
    ]
    if method in {"POST", "PUT", "PATCH", "DELETE"} and json_body is not None:
        js_options.append(
            f"body: JSON.stringify({json.dumps(json_body, ensure_ascii=False)})"
        )
    js_code = (
        f'const url = {json.dumps(url + query_string)};\n\n'
        "const response = await fetch(url, {\n  "
        + ",\n  ".join(js_options)
        + "\n});\n\n"
        "const data = await response.json();\n"
        "console.log(response.status, data);"
    )

    # cURL
    curl_parts = [f'curl -X {method} "{url}"']
    for key, value in safe_headers.items():
        curl_parts.append(f'-H "{key}: {value}"')
    for key, value in params.items():
        curl_parts.append(f'--data-urlencode "{key}={value}"')
    if method in {"POST", "PUT", "PATCH", "DELETE"} and json_body is not None:
        curl_parts.append('-H "Content-Type: application/json"')
        curl_parts.append(
            f"-d '{json.dumps(json_body, ensure_ascii=False)}'"
        )
    curl_code = " \\\n  ".join(curl_parts)

    return python_code, js_code, curl_code


def add_request_history(method: str, url: str, status, elapsed_ms, content_type: str):
    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "method": method,
        "url": url,
        "status": status,
        "time_ms": round(float(elapsed_ms), 1) if elapsed_ms is not None else None,
        "content_type": content_type or "Unknown",
    }
    st.session_state.request_history.insert(0, entry)
    st.session_state.request_history = st.session_state.request_history[:20]


def import_library_payload(payload: dict):
    imported_favorites = {}
    imported_collections = {}

    for item in payload.get("favorites", []):
        if isinstance(item, dict) and item.get("Link"):
            record = api_to_record(item)
            imported_favorites[record["Link"]] = record

    collections = payload.get("collections", {})
    if isinstance(collections, dict):
        for name, items in collections.items():
            clean_name = str(name).strip()
            if not clean_name or not isinstance(items, list):
                continue

            imported_collections[clean_name] = {}
            for item in items:
                if isinstance(item, dict) and item.get("Link"):
                    record = api_to_record(item)
                    imported_collections[clean_name][record["Link"]] = record

    st.session_state.favorites.update(imported_favorites)

    for name, items in imported_collections.items():
        if name not in st.session_state.collections:
            st.session_state.collections[name] = {}
        st.session_state.collections[name].update(items)



# =========================================================
# SAFE PUBLIC API TESTER HELPERS
# =========================================================
def validate_public_url(url: str):
    """Allow only public HTTP(S) URLs and block local/private/reserved targets."""
    try:
        parsed = urlparse(url.strip())
    except Exception:
        return False, "Invalid URL."

    if parsed.scheme not in {"http", "https"}:
        return False, "Only http:// and https:// URLs are allowed."

    if parsed.username or parsed.password:
        return False, "URLs containing embedded usernames/passwords are blocked."

    if not parsed.hostname:
        return False, "URL must include a valid hostname."

    host = parsed.hostname.lower().strip(".")
    if host in {"localhost", "localhost.localdomain"} or host.endswith(".local"):
        return False, "Local/internal hosts are blocked."

    try:
        ip_obj = ipaddress.ip_address(host)
        addresses = [ip_obj]
    except ValueError:
        try:
            infos = socket.getaddrinfo(
                host,
                parsed.port or (443 if parsed.scheme == "https" else 80),
                type=socket.SOCK_STREAM,
            )
            addresses = []
            for info in infos:
                raw_ip = info[4][0]
                try:
                    addresses.append(ipaddress.ip_address(raw_ip))
                except ValueError:
                    continue
        except socket.gaierror:
            return False, "Hostname could not be resolved."
        except Exception:
            return False, "Could not validate this hostname."

    if not addresses:
        return False, "No public IP address found for this hostname."

    for ip_obj in addresses:
        if (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_multicast
            or ip_obj.is_reserved
            or ip_obj.is_unspecified
        ):
            return False, "Private, local, reserved, and internal network targets are blocked."

    return True, "OK"


def parse_json_object(raw_text: str, label: str):
    if not raw_text.strip():
        return {}

    data = json.loads(raw_text)
    if not isinstance(data, dict):
        raise ValueError(f"{label} must be a JSON object.")
    return data


def sanitize_custom_headers(headers: dict):
    blocked = {
        "host",
        "content-length",
        "transfer-encoding",
        "connection",
        "proxy-authorization",
        "proxy-authenticate",
        "upgrade",
        "te",
    }

    clean = {}
    for key, value in headers.items():
        key = str(key).strip()
        if not key:
            continue

        if key.lower() in blocked:
            raise ValueError(f'Header "{key}" is not allowed.')

        if isinstance(value, (dict, list)):
            raise ValueError(f'Header "{key}" must have a simple string/number value.')

        clean[key] = str(value)

    return clean


def test_public_api(
    method: str,
    url: str,
    params: dict,
    custom_headers: dict,
    auth_type: str,
    auth_value: str,
    json_body: dict | None,
):
    ok, message = validate_public_url(url)
    if not ok:
        raise ValueError(message)

    method = method.upper().strip()
    allowed_methods = {"GET", "POST", "PUT", "PATCH", "DELETE"}
    if method not in allowed_methods:
        raise ValueError("Unsupported HTTP method.")

    headers = {
        "User-Agent": "NEXUS-API-Explorer/2.0",
        "Accept": "application/json, text/plain;q=0.9, */*;q=0.5",
    }
    headers.update(sanitize_custom_headers(custom_headers))

    if auth_value.strip():
        if auth_type == "Bearer Token":
            headers["Authorization"] = f"Bearer {auth_value.strip()}"
        elif auth_type == "X-API-Key":
            headers["X-API-Key"] = auth_value.strip()
        elif auth_type == "API Key (Authorization)":
            headers["Authorization"] = auth_value.strip()

    request_kwargs = {
        "params": params,
        "headers": headers,
        "timeout": (5, 20),
        "allow_redirects": False,
        "stream": True,
    }

    if method in {"POST", "PUT", "PATCH", "DELETE"} and json_body is not None:
        request_kwargs["json"] = json_body

    started = time.perf_counter()
    response = requests.request(
        method,
        url.strip(),
        **request_kwargs,
    )
    elapsed_ms = (time.perf_counter() - started) * 1000

    max_bytes = 1024 * 1024  # 1 MB preview limit
    chunks = []
    total = 0
    truncated = False

    for chunk in response.iter_content(chunk_size=16384):
        if not chunk:
            continue

        remaining = max_bytes - total
        if remaining <= 0:
            truncated = True
            break

        if len(chunk) > remaining:
            chunks.append(chunk[:remaining])
            total += remaining
            truncated = True
            break

        chunks.append(chunk)
        total += len(chunk)

    body_bytes = b"".join(chunks)
    encoding = response.encoding or "utf-8"
    body_text = body_bytes.decode(encoding, errors="replace")

    return response, body_text, truncated, elapsed_ms, len(body_bytes)


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


.ai-box {
    border:1px solid rgba(91,124,255,.24);
    background:linear-gradient(135deg, rgba(91,124,255,.09), rgba(34,211,238,.045));
    padding:22px;
    border-radius:20px;
    margin:12px 0 18px 0;
}

.ai-title {
    font-family:"Space Grotesk", sans-serif;
    font-size:1.22rem;
    font-weight:700;
}

.ai-text {
    color:#9eabc0;
    margin-top:6px;
    line-height:1.6;
    font-size:.86rem;
}

.score {
    display:inline-block;
    margin-top:12px;
    padding:5px 9px;
    border-radius:8px;
    color:#9fffd0;
    background:rgba(50,224,140,.08);
    border:1px solid rgba(50,224,140,.16);
    font-size:.72rem;
    font-weight:700;
}

.why {
    margin-top:10px;
    color:#8190a7;
    font-size:.76rem;
}

.tester-box {
    border:1px solid rgba(34,211,238,.20);
    background:linear-gradient(135deg, rgba(34,211,238,.055), rgba(91,124,255,.055));
    padding:22px;
    border-radius:20px;
    margin:12px 0 18px 0;
}

.tester-title {
    font-family:"Space Grotesk", sans-serif;
    font-size:1.22rem;
    font-weight:700;
}

.tester-text {
    color:#9eabc0;
    margin-top:6px;
    line-height:1.6;
    font-size:.86rem;
}

.response-card {
    border:1px solid rgba(255,255,255,.08);
    border-radius:18px;
    background:#080b13;
    padding:18px;
    margin-top:12px;
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
div[data-testid="stTextArea"] textarea,
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
            <small>Intelligent Public API Explorer</small>
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
      <div class="eyebrow">⚡ INTELLIGENT API DISCOVERY</div>

      <h1>
        Describe your idea.<br>
        <span class="gradient-text">Find the right API.</span>
      </h1>

      <p>
        Explore {len(df):,}+ public APIs or describe your project in normal language.
        NEXUS API can rank relevant APIs automatically, with no paid AI key required.
      </p>

      <div class="hero-actions">
        <span class="tag">Smart Recommendations</span>
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
        <div><span class="t-muted">$</span> nexus recommend</div>
        <div><span class="t-cyan">idea:</span> weather app for students</div>
        <div><span class="t-green">✓</span> intent detected</div>
        <div><span class="t-green">✓</span> secure APIs prioritized</div>
        <div><span class="t-violet">→</span> beginner-friendly matches ranked</div>
        <div><span class="t-muted">status:</span> intelligence ready</div>
        <br>
        <div><span class="t-cyan">GET</span> /recommend/api</div>
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
    ("01", "Idea Recommender", "Describe a project idea and get ranked API recommendations."),
    ("02", "Saved Collections", "Favorite useful APIs and organize them into named collections."),
    ("03", "Security Signals", "See HTTPS and CORS support before opening the docs."),
    ("04", "API Tester", "Send GET, POST, PUT, PATCH and DELETE requests safely."),
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
# INTELLIGENT RECOMMENDER
# =========================================================
st.markdown(
    """
<div class="section-head">
  <div>
    <div class="section-title">🧠 Intelligent API Recommender</div>
    <div class="section-sub">Describe what you want to build in English or Hinglish.</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="ai-box">
        <div class="ai-title">No API key required</div>
        <div class="ai-text">
            This local intelligence engine detects your project intent, matches keywords with
            API names/categories/descriptions, and boosts secure + beginner-friendly APIs.
            Example: <b>“mujhe crypto price tracker banana hai”</b>.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

idea = st.text_area(
    "Project idea",
    placeholder="Example: I want to build a weather dashboard for students with forecast data...",
    height=110,
)

r1, r2 = st.columns([1, 1])
with r1:
    beginner_mode = st.toggle("Prefer no-key / beginner APIs", value=True)
with r2:
    recommendation_count = st.selectbox("Number of recommendations", [4, 6, 8, 10, 12], index=2)

if st.button("⚡ Find Best APIs", use_container_width=True, type="primary"):
    if not idea.strip():
        st.warning("Please describe your project idea first.")
    else:
        recommendations = recommend_apis(
            df,
            idea,
            beginner_mode=beginner_mode,
            top_n=recommendation_count,
        )

        detected = detect_intents(idea)
        if detected:
            st.success("Detected intent: " + ", ".join(detected))

        if recommendations.empty:
            st.info("No strong match found. Add a few more specific words about the data you need.")
        else:
            st.markdown(
                f'<div class="section-sub"><b>{len(recommendations)}</b> recommended APIs ranked for your idea.</div>',
                unsafe_allow_html=True,
            )

            for i, row in recommendations.iterrows():
                api_name = escape(str(row["API"]))
                desc = escape(str(row["Description"]))
                cat = escape(str(row["Category"]))
                auth_value = escape(str(row["Auth"]))
                https_value = escape(str(row["HTTPS"]))
                cors_value = escape(str(row["CORS"]))
                why = escape(str(row["Why"]))
                score = row["Score"]

                st.markdown(
                    f"""
                    <div class="api-card">
                        <div class="api-name">#{i+1} — {api_name}</div>
                        <div class="api-desc">{desc}</div>

                        <div class="badges">
                            <span class="badge">{cat}</span>
                            <span class="badge">Auth: {auth_value}</span>
                            <span class="badge">HTTPS: {https_value}</span>
                            <span class="badge">CORS: {cors_value}</span>
                        </div>

                        <div class="score">Relevance score: {score}</div>
                        <div class="why">Why recommended: {why}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                rec_open, rec_save = st.columns([2.3, 1])

                with rec_open:
                    st.link_button(
                        f"Open {row['API']} documentation ↗",
                        str(row["Link"]),
                        use_container_width=True,
                    )

                with rec_save:
                    rec_key = stable_id(str(row["Link"]))
                    already_saved = str(row["Link"]) in st.session_state.favorites
                    if st.button(
                        "★ Saved" if already_saved else "☆ Save",
                        key=f"rec_save_{rec_key}_{i}",
                        use_container_width=True,
                        disabled=already_saved,
                    ):
                        add_favorite(row)
                        st.toast(f"{row['API']} added to Favorites.")
                        st.rerun()

# =========================================================
# ADVANCED BUILT-IN API TESTER
# =========================================================
st.markdown(
    """
<div class="section-head">
  <div>
    <div class="section-title">🧪 Advanced API Tester</div>
    <div class="section-sub">Test public GET, POST, PUT, PATCH and DELETE endpoints directly inside NEXUS API.</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="tester-box">
        <div class="tester-title">Multi-Method Request Console</div>
        <div class="tester-text">
            Public endpoints only. Local/private network addresses are blocked, redirects are not followed,
            requests time out automatically, and response previews are limited to 1 MB.
            Use POST/PUT/PATCH/DELETE only on APIs you own or are authorized to test.
            Never save secret API keys in GitHub.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

method_col, url_col = st.columns([0.75, 3.25])

with method_col:
    request_method = st.selectbox(
        "HTTP method",
        ["GET", "POST", "PUT", "PATCH", "DELETE"],
        key="tester_method",
    )

with url_col:
    test_url = st.text_input(
        "API endpoint URL",
        placeholder="Example: https://jsonplaceholder.typicode.com/posts",
        key="tester_url",
    )

tp1, tp2 = st.columns(2)

with tp1:
    params_text = st.text_area(
        "Query parameters (JSON)",
        value="{}",
        height=120,
        key="tester_params",
        help='Example: {"limit": 5, "page": 1}',
    )

with tp2:
    custom_headers_text = st.text_area(
        "Custom headers (JSON)",
        value="{}",
        height=120,
        key="tester_headers",
        help='Example: {"Accept-Language": "en-US"}',
    )

body_col, auth_col = st.columns([1.55, 1])

with body_col:
    if request_method == "GET":
        st.text_area(
            "JSON request body",
            value="",
            height=150,
            disabled=True,
            key="tester_body_disabled",
            help="GET requests do not use a JSON body in this tester.",
        )
        body_text = ""
    else:
        body_text = st.text_area(
            "JSON request body",
            value="{}",
            height=150,
            key="tester_body",
            help='Example: {"title": "Hello", "userId": 1}',
        )

with auth_col:
    auth_type = st.selectbox(
        "Optional authentication",
        ["None", "Bearer Token", "X-API-Key", "API Key (Authorization)"],
        key="tester_auth_type",
    )

    auth_value = st.text_input(
        "Temporary token / key",
        type="password",
        key="tester_auth_value",
        help="Used only for this request and not written to your project files.",
    )

    if request_method == "DELETE":
        st.warning("DELETE can permanently remove data on real APIs. Use only authorized test endpoints.")

if st.button(
    f"▶ Send {request_method} Request",
    use_container_width=True,
    key="run_api_test",
    type="primary",
):
    if not test_url.strip():
        st.warning("Enter a public API endpoint first.")
    else:
        try:
            params = parse_json_object(params_text, "Query parameters")
            custom_headers = parse_json_object(custom_headers_text, "Custom headers")

            json_body = None
            if request_method in {"POST", "PUT", "PATCH", "DELETE"}:
                json_body = parse_json_object(body_text, "JSON request body")

            with st.spinner(f"Sending safe {request_method} request..."):
                response, body_preview, truncated, elapsed_ms, preview_bytes = test_public_api(
                    request_method,
                    test_url,
                    params,
                    custom_headers,
                    auth_type,
                    auth_value,
                    json_body,
                )

            add_request_history(
                request_method,
                test_url.strip(),
                response.status_code,
                elapsed_ms,
                response.headers.get("Content-Type", "").split(";")[0],
            )

            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric("Status", response.status_code)
            mc2.metric(
                "Content type",
                response.headers.get("Content-Type", "Unknown").split(";")[0],
            )
            mc3.metric("Time", f"{elapsed_ms:.0f} ms")
            mc4.metric("Preview size", f"{preview_bytes / 1024:.1f} KB")

            if 200 <= response.status_code < 300:
                st.success(
                    f"{request_method} request completed successfully: HTTP {response.status_code}"
                )
            elif 300 <= response.status_code < 400:
                location = response.headers.get("Location", "Not provided")
                st.warning(
                    f"HTTP {response.status_code} redirect received. Redirects are intentionally "
                    f"not followed for safety. Location: {location}"
                )
            else:
                st.error(f"API returned HTTP {response.status_code}")

            with st.expander("Request summary"):
                st.code(
                    f"Method: {request_method}\n"
                    f"URL: {test_url.strip()}\n"
                    f"Query params: {json.dumps(params, ensure_ascii=False)}",
                    language="text",
                )

            with st.expander("Response headers"):
                safe_headers = {
                    k: v
                    for k, v in response.headers.items()
                    if k.lower() not in {"set-cookie"}
                }
                st.json(safe_headers)

            st.markdown("#### Response preview")
            content_type = response.headers.get("Content-Type", "").lower()

            if "json" in content_type:
                try:
                    parsed_json = json.loads(body_preview)
                    st.json(parsed_json, expanded=True)
                except Exception:
                    st.code(body_preview or "(empty response)", language="text")
            else:
                st.code(body_preview or "(empty response)", language="text")

            st.markdown("#### Quick-start code")
            py_code, js_code, curl_code = build_code_snippets(
                request_method,
                test_url.strip(),
                params,
                custom_headers,
                auth_type,
                json_body,
            )

            code_tab1, code_tab2, code_tab3 = st.tabs(
                ["🐍 Python", "🟨 JavaScript", "⌨️ cURL"]
            )

            with code_tab1:
                st.code(py_code, language="python")

            with code_tab2:
                st.code(js_code, language="javascript")

            with code_tab3:
                st.code(curl_code, language="bash")

            st.caption(
                "Security note: temporary credentials are never inserted into generated snippets. "
                "Placeholders are used instead."
            )

            if truncated:
                st.info("Response was larger than 1 MB, so only the first 1 MB is shown.")

        except json.JSONDecodeError as exc:
            st.error(f"Invalid JSON: {exc.msg}. Check query parameters, headers, or request body.")
        except ValueError as exc:
            st.error(str(exc))
        except requests.Timeout:
            st.error("The API request timed out.")
        except requests.RequestException as exc:
            st.error(f"Request failed: {exc}")
        except Exception as exc:
            st.error(f"Could not test this API: {exc}")


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

                result_open, result_save = st.columns([2.3, 1])

                with result_open:
                    st.link_button(
                        f"Open {row['API']} ↗",
                        str(row["Link"]),
                        use_container_width=True,
                    )

                with result_save:
                    result_key = stable_id(str(row["Link"]))
                    already_saved = str(row["Link"]) in st.session_state.favorites
                    if st.button(
                        "★ Saved" if already_saved else "☆ Save",
                        key=f"result_save_{result_key}_{idx}",
                        use_container_width=True,
                        disabled=already_saved,
                    ):
                        add_favorite(row)
                        st.toast(f"{row['API']} added to Favorites.")
                        st.rerun()




# =========================================================
# API COMPARE
# =========================================================
st.markdown(
    """
<div class="section-head">
  <div>
    <div class="section-title">⚖️ Compare APIs</div>
    <div class="section-sub">Compare up to three APIs side-by-side before choosing one for your project.</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

api_options = (
    df.assign(
        Display=df["API"].astype(str) + " — " + df["Category"].astype(str)
    )
    .drop_duplicates(subset=["Display"])
    .set_index("Display")
)

compare_choices = st.multiselect(
    "Choose APIs to compare",
    options=list(api_options.index),
    max_selections=3,
    placeholder="Select up to 3 APIs...",
    key="compare_apis",
)

if compare_choices:
    compare_rows = api_options.loc[compare_choices].reset_index()

    compare_table = compare_rows[
        ["API", "Category", "Auth", "HTTPS", "CORS", "Description", "Link"]
    ].copy()

    st.dataframe(
        compare_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Link": st.column_config.LinkColumn("Docs"),
        },
    )

    no_auth_count_compare = int(
        compare_rows["Auth"].astype(str).str.lower().isin(["no", "", "none"]).sum()
    )
    https_count_compare = int(
        compare_rows["HTTPS"].astype(str).str.lower().isin(["yes", "true"]).sum()
    )

    cp1, cp2 = st.columns(2)
    cp1.metric("No-auth choices", f"{no_auth_count_compare}/{len(compare_rows)}")
    cp2.metric("HTTPS choices", f"{https_count_compare}/{len(compare_rows)}")
else:
    st.info("Select APIs above to compare authentication, HTTPS, CORS and descriptions.")


# =========================================================
# REQUEST HISTORY
# =========================================================
st.markdown(
    """
<div class="section-head">
  <div>
    <div class="section-title">🕘 Request History</div>
    <div class="section-sub">Review your latest API tests from this Streamlit session.</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

if not st.session_state.request_history:
    st.info("No requests tested yet in this session.")
else:
    history_df = pd.DataFrame(st.session_state.request_history)

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "time": "Time",
            "method": "Method",
            "url": "URL",
            "status": "Status",
            "time_ms": st.column_config.NumberColumn("Time (ms)", format="%.1f"),
            "content_type": "Content Type",
        },
    )

    history_c1, history_c2 = st.columns([1, 3])

    with history_c1:
        if st.button("Clear History", use_container_width=True, key="clear_request_history"):
            st.session_state.request_history = []
            st.rerun()

    with history_c2:
        st.download_button(
            "⬇ Export Request History",
            data=json.dumps(st.session_state.request_history, indent=2, ensure_ascii=False),
            file_name="nexus_request_history.json",
            mime="application/json",
            use_container_width=True,
            key="export_request_history",
        )


# =========================================================
# MY API LIBRARY — FAVORITES + COLLECTIONS
# =========================================================
st.markdown(
    """
<div class="section-head">
  <div>
    <div class="section-title">⭐ My API Library</div>
    <div class="section-sub">Save useful APIs, organize collections, and export/import your library.</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="ai-box">
        <div class="ai-title">Favorites & Collections</div>
        <div class="ai-text">
            Favorites are kept in your current Streamlit session. Use <b>Export Library</b>
            to save them permanently as JSON, then import that file later on any device/session.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

lib1, lib2, lib3 = st.columns(3)
lib1.metric("Favorites", len(st.session_state.favorites))
lib2.metric("Collections", len(st.session_state.collections))
lib3.metric(
    "Saved in collections",
    sum(len(items) for items in st.session_state.collections.values()),
)

create_col, export_col = st.columns([1.6, 1])

with create_col:
    new_collection_name = st.text_input(
        "Create a collection",
        placeholder="Example: Weather Project APIs",
        key="new_collection_name",
    )
    if st.button("＋ Create Collection", use_container_width=True, key="create_collection"):
        clean_name = new_collection_name.strip()
        if not clean_name:
            st.warning("Enter a collection name.")
        elif clean_name in st.session_state.collections:
            st.info("That collection already exists.")
        else:
            st.session_state.collections[clean_name] = {}
            st.toast(f'Collection "{clean_name}" created.')
            st.rerun()

with export_col:
    st.write("")
    st.download_button(
        "⬇ Export Library JSON",
        data=build_library_export(),
        file_name="nexus_api_library.json",
        mime="application/json",
        use_container_width=True,
        key="export_library",
    )

import_file = st.file_uploader(
    "Import a previously exported NEXUS library",
    type=["json"],
    key="import_library_file",
)

if import_file is not None:
    if st.button("⬆ Import Library", use_container_width=True, key="import_library_button"):
        try:
            payload = json.loads(import_file.getvalue().decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("Library file must contain a JSON object.")
            import_library_payload(payload)
            st.success("Library imported successfully.")
            st.rerun()
        except Exception as exc:
            st.error(f"Could not import library: {exc}")

favorites_tab, collections_tab = st.tabs(["⭐ Favorites", "📁 Collections"])

with favorites_tab:
    if not st.session_state.favorites:
        st.info("No favorites yet. Use the ☆ Save button on any API card.")
    else:
        collection_names = list(st.session_state.collections.keys())

        for fav_index, (link, record) in enumerate(list(st.session_state.favorites.items())):
            fav_id = stable_id(link)

            st.markdown(
                f"""
                <div class="api-card">
                    <div class="api-name">★ {escape(record["API"])}</div>
                    <div class="api-desc">{escape(record["Description"])}</div>
                    <div class="badges">
                        <span class="badge">{escape(record["Category"])}</span>
                        <span class="badge">Auth: {escape(record["Auth"])}</span>
                        <span class="badge">HTTPS: {escape(record["HTTPS"])}</span>
                        <span class="badge">CORS: {escape(record["CORS"])}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            fav_open, fav_remove = st.columns([2.3, 1])

            with fav_open:
                st.link_button(
                    f"Open {record['API']} ↗",
                    link,
                    use_container_width=True,
                    key=f"fav_open_{fav_id}",
                )

            with fav_remove:
                if st.button(
                    "Remove Favorite",
                    key=f"remove_fav_{fav_id}",
                    use_container_width=True,
                ):
                    remove_favorite(link)
                    st.rerun()

            if collection_names:
                add_col1, add_col2 = st.columns([2, 1])
                with add_col1:
                    destination = st.selectbox(
                        "Add to collection",
                        collection_names,
                        key=f"fav_collection_select_{fav_id}",
                        label_visibility="collapsed",
                    )
                with add_col2:
                    if st.button(
                        "Add",
                        key=f"fav_add_collection_{fav_id}",
                        use_container_width=True,
                    ):
                        add_to_collection(destination, record)
                        st.toast(f"Added to {destination}.")
                        st.rerun()
            else:
                st.caption("Create a collection above to organize this favorite.")

with collections_tab:
    if not st.session_state.collections:
        st.info("No collections yet. Create your first collection above.")
    else:
        selected_collection = st.selectbox(
            "Choose collection",
            list(st.session_state.collections.keys()),
            key="selected_library_collection",
        )

        collection_items = st.session_state.collections.get(selected_collection, {})

        col_title, col_delete = st.columns([2.4, 1])
        with col_title:
            st.markdown(f"### 📁 {selected_collection}")
            st.caption(f"{len(collection_items)} saved API(s)")
        with col_delete:
            if st.button(
                "Delete Collection",
                key=f"delete_collection_{stable_id(selected_collection)}",
                use_container_width=True,
            ):
                st.session_state.collections.pop(selected_collection, None)
                st.rerun()

        if not collection_items:
            st.info("This collection is empty. Add APIs from your Favorites tab.")
        else:
            for item_index, (link, record) in enumerate(list(collection_items.items())):
                item_id = stable_id(selected_collection + link)

                st.markdown(
                    f"""
                    <div class="api-card">
                        <div class="api-name">{escape(record["API"])}</div>
                        <div class="api-desc">{escape(record["Description"])}</div>
                        <div class="badges">
                            <span class="badge">{escape(record["Category"])}</span>
                            <span class="badge">Auth: {escape(record["Auth"])}</span>
                            <span class="badge">HTTPS: {escape(record["HTTPS"])}</span>
                            <span class="badge">CORS: {escape(record["CORS"])}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                item_open, item_remove = st.columns([2.3, 1])
                with item_open:
                    st.link_button(
                        f"Open {record['API']} ↗",
                        link,
                        use_container_width=True,
                        key=f"collection_open_{item_id}",
                    )
                with item_remove:
                    if st.button(
                        "Remove",
                        key=f"collection_remove_{item_id}",
                        use_container_width=True,
                    ):
                        remove_from_collection(selected_collection, link)
                        st.rerun()


# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
<div class="footer-box">
    NEXUS API • Discovery • Testing • Code Generator • Compare • History • Collections
    <br><br>
    Describe your idea. Discover the API. Build the project.
</div>
""",
    unsafe_allow_html=True,
)
