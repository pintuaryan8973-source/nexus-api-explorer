<p align="center">
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

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat-square&logo=streamlit&logoColor=white">
  <img src="https://img.shields.io/badge/Pandas-Data-150458?style=flat-square&logo=pandas">
  <img src="https://img.shields.io/badge/API-Explorer-22D3EE?style=flat-square">
  <img src="https://img.shields.io/badge/API-Tester-8B5CF6?style=flat-square">
  <img src="https://img.shields.io/badge/Status-LIVE-32E08C?style=flat-square">
  <img src="https://img.shields.io/github/v/release/pintuaryan8973-source/nexus-api-explorer?style=flat-square&label=Release">
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

⭐ Favorites

📁 Saved API collections

🔄 Import / Export library

🕘 Request history

⚖️ API comparison

❤️ API health checker

🧩 JSON response toolkit

🐍 Python code generator

🟨 JavaScript code generator

⌨️ cURL code generator

🧪 Advanced API Tester

NEXUS API includes a built-in multi-method request console.

Supported HTTP Methods

GET
POST
PUT
PATCH
DELETE

Tester Features

Public endpoint testing

Query parameters

Custom headers

JSON request body

Bearer Token authentication

X-API-Key authentication

Authorization API-key support

HTTP status code

Content type

Response timing

Response size

Response headers

JSON response preview

Text response preview

1 MB response preview limit

Private/local network protection

Redirect protection

Use write methods such as POST, PUT, PATCH and DELETE only on APIs you own or are authorized to test.

🧪 GET Example

Method

GET

URL

https://jsonplaceholder.typicode.com/todos/1

Expected response:

{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}

🧪 POST Example

Method

POST

URL

https://jsonplaceholder.typicode.com/posts

JSON Body

{
  "title": "NEXUS API",
  "body": "Testing POST request",
  "userId": 1
}

Typical response:

{
  "id": 101
}

🧪 PUT Example

Method

PUT

URL

https://jsonplaceholder.typicode.com/posts/1

JSON Body

{
  "id": 1,
  "title": "NEXUS API Updated",
  "body": "Testing PUT request",
  "userId": 1
}

🧪 PATCH Example

Method

PATCH

URL

https://jsonplaceholder.typicode.com/posts/1

JSON Body

{
  "title": "Only Title Updated"
}

🧪 DELETE Example

Method

DELETE

URL

https://jsonplaceholder.typicode.com/posts/1

Typical response:

{}

JSONPlaceholder simulates write operations; changes are not permanently stored.

🧩 JSON Response Toolkit

The JSON Toolkit can:

Inspect JSON structure

Show field types

Pretty-print JSON

Convert tabular JSON to CSV

Export JSON

Export CSV

Generate Python parsing examples

❤️ API Health Checker

Check multiple public API endpoints and view:

HTTP status

Response time

Content type

Healthy / redirect / timeout / error status

Exportable health report CSV

⚖️ Compare APIs

Compare up to 3 APIs side-by-side using:

Authentication

HTTPS support

CORS support

Description

Documentation link

⭐ Favorites & Collections

Users can:

Save favorite APIs

Create named collections

Add favorites into collections

Remove saved APIs

Export library as JSON

Import library later

🕘 Request History

NEXUS API stores recent requests in the current session and shows:

Method

URL

Status

Response time

Content type

Request history can also be exported.

💻 Code Generator

After testing an endpoint, NEXUS API can generate starter code for:

Python

import requests

JavaScript

fetch(...)

cURL

curl ...

Secret tokens are replaced with safe placeholders instead of being inserted into generated snippets.

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

Clone:

git clone https://github.com/pintuaryan8973-source/nexus-api-explorer.git
cd nexus-api-explorer

Create virtual environment:

python -m venv .venv

Install dependencies:

pip install -r requirements.txt

Run:

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

Typical commands:

git add .
git commit -m "Update NEXUS API"
git push

🗺️ Roadmap

✅ Public API Explorer
✅ Smart Search
✅ Category Filter
✅ Authentication Filter
✅ HTTPS Detection
✅ CORS Information
✅ Live GitHub Catalog
✅ Advanced UI
✅ GitHub Repository
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
✅ Favorites
✅ Saved Collections
✅ Request History
✅ API Compare
✅ API Health Checker
✅ JSON Toolkit
✅ Code Generator
✅ Release v1.0.0

⬜ User Accounts
⬜ Cloud Database
⬜ Persistent Favorites
⬜ AI Recommendation Assistant
⬜ API Analytics Dashboard
⬜ Team Workspaces

📦 Latest Release

Current Stable Release: v1.0.0

Release page:

https://github.com/pintuaryan8973-source/nexus-api-explorer/releases/tag/v1.0.0

📚 Data Source

API catalog data is sourced from:

public-apis/public-apis

Individual APIs belong to their respective owners/providers.

🔗 Important Links

🚀 Live App

https://nexusapipintuaryan.streamlit.app

🐙 GitHub Repository

https://github.com/pintuaryan8973-source/nexus-api-explorer

📦 Latest Release

https://github.com/pintuaryan8973-source/nexus-api-explorer/releases/tag/v1.0.0

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