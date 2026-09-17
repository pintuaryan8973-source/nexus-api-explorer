git add README.md<p align="center">
  <img src="assets/nexus-api-banner.png" alt="NEXUS API Banner" width="100%">
</p>

<h1 align="center">⚡ NEXUS API</h1>

<h3 align="center">Intelligent Public API Discovery & Advanced Testing Platform</h3>

<p align="center">
  Search • Discover • Test • Integrate • Build
</p>

<p align="center">
  <a href="https://nexusapipintuaryan.streamlit.app">
    <img src="https://img.shields.io/badge/🚀_LIVE_DEMO-OPEN_APP-00D4FF?style=for-the-badge">
  </a>
  <a href="https://github.com/pintuaryan8973-source/nexus-api-explorer">
    <img src="https://img.shields.io/badge/GITHUB-SOURCE_CODE-181717?style=for-the-badge&logo=github">
  </a>
</p>

🚀 About NEXUS API

NEXUS API is a modern Public API Explorer and advanced API testing platform built with Python + Streamlit.

It loads the public-apis/public-apis catalog from GitHub and turns it into an interactive dashboard where developers and students can discover APIs, inspect authentication requirements, check HTTPS/CORS support, open documentation and test endpoints directly.

🌐 Live Application

https://nexusapipintuaryan.streamlit.app

✨ Main Features

🔎 Smart API search

📂 Category filtering

🔐 Authentication filtering

🔒 HTTPS information

🌐 CORS information

📊 Live API statistics

⚡ GitHub-powered catalog

📖 Direct documentation links

🧪 Built-in API tester

📄 JSON response viewer

⏱️ Response timing

📦 Response size preview

🔑 Temporary Bearer/API-key testing

🛡️ Private/local network blocking

📱 Responsive developer-focused UI

🧪 Advanced API Tester

Supported methods:

GET
POST
PUT
PATCH
DELETE

Tester features:

Query parameters

Custom headers

JSON request body

Bearer Token authentication

X-API-Key authentication

HTTP status code

Content type

Response timing

Response size

Response headers

JSON/text response preview

1 MB preview limit

Private/local network protection

Redirect protection

Use POST, PUT, PATCH and DELETE only on APIs you own or are authorized to test.

🧪 GET Example

GET
https://jsonplaceholder.typicode.com/todos/1

Expected response:

{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}

🧪 POST Example

POST
https://jsonplaceholder.typicode.com/posts

{
  "title": "NEXUS API",
  "body": "Testing POST request",
  "userId": 1
}

🧪 PUT Example

PUT
https://jsonplaceholder.typicode.com/posts/1

{
  "id": 1,
  "title": "NEXUS API Updated",
  "body": "Testing PUT request",
  "userId": 1
}

🧪 PATCH Example

PATCH
https://jsonplaceholder.typicode.com/posts/1

{
  "title": "Only Title Updated"
}

🧪 DELETE Example

DELETE
https://jsonplaceholder.typicode.com/posts/1

Typical test response:

{}

JSONPlaceholder simulates write operations; changes are not permanently stored.

🛠️ Tech Stack

Technology

Purpose

Python

Main programming language

Streamlit

Interactive web UI

Pandas

Data processing/filtering

Requests

HTTP requests

HTML/CSS

Custom interface design

GitHub

Source + public API catalog

Streamlit Cloud

Live deployment

📂 Project Structure

nexus-api-explorer/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── assets/
    └── nexus-api-banner.png

⚙️ Installation

git clone https://github.com/pintuaryan8973-source/nexus-api-explorer.git
cd nexus-api-explorer
python -m venv .venv
pip install -r requirements.txt
streamlit run app.py

Local URL:

http://localhost:8501

🪟 Windows PowerShell

python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py

🌐 Deployment

Repository:

pintuaryan8973-source/nexus-api-explorer

Branch:

main

Main file:

app.py

Live app:

https://nexusapipintuaryan.streamlit.app

🔄 Update Workflow

VS Code
   ↓
git add .
   ↓
git commit
   ↓
git push
   ↓
GitHub
   ↓
Streamlit Cloud
   ↓
Live App Updated

🗺️ Roadmap

✅ Public API Explorer
✅ Smart Search
✅ Category Filter
✅ Authentication Filter
✅ HTTPS Detection
✅ CORS Information
✅ Live GitHub Catalog
✅ Advanced UI
✅ Streamlit Deployment
✅ GET Tester
✅ POST Tester
✅ PUT Tester
✅ PATCH Tester
✅ DELETE Tester
✅ Query Parameters
✅ Custom Headers
✅ JSON Body
✅ Bearer Token Support
✅ API-Key Support
✅ JSON Response Viewer
✅ Response Timing
✅ Response Size Preview

⬜ Favorite APIs
⬜ Saved Collections
⬜ User Accounts
⬜ API Analytics
⬜ AI Recommendation Assistant
⬜ Export API Collections

📚 Data Source

API catalog data is sourced from:

public-apis/public-apis

Individual APIs belong to their respective owners/providers.

🔗 Links

🚀 Live App

https://nexusapipintuaryan.streamlit.app

🐙 GitHub Repository

https://github.com/pintuaryan8973-source/nexus-api-explorer

⭐ Support

If you find NEXUS API useful, consider giving the repository a GitHub Star ⭐.

<p align="center">
  <b>⚡ NEXUS API</b>
</p>

<p align="center">
  Search • Discover • Test • Build
</p>

<p align="center">
  <b>Discover Faster • Build Smarter • Ship More</b>
</p>