<p align="center">
  <img src="assets/nexus-api-banner.png"
       alt="NEXUS API Banner"
       width="100%">
</p>

<h1 align="center">⚡ NEXUS API</h1>

<h3 align="center">
  Intelligent Public API Discovery Platform
</h3>

<p align="center">
  Search • Discover • Integrate • Build
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
  <img src="https://img.shields.io/badge/API-Live_Catalog-22D3EE?style=flat-square">
  <img src="https://img.shields.io/badge/Status-LIVE-32E08C?style=flat-square">
</p>

---

# 🚀 NEXUS API

**NEXUS API** is an intelligent Public API Explorer built with
**Python and Streamlit**.

It transforms the large `public-apis/public-apis` GitHub catalog into a
modern searchable dashboard.

Instead of manually searching through thousands of API entries,
developers can quickly discover APIs based on their project needs.

🌐 **Live App**

https://nexusapipintuaryan.streamlit.app

---

# 🧠 What NEXUS API Can Do

NEXUS API provides a developer-friendly environment where you can:

- 🔎 Search APIs instantly
- 📂 Explore API categories
- 🔐 Filter APIs by authentication
- 🔒 Check HTTPS support
- 🌐 Check CORS availability
- 📊 View live API statistics
- ⚡ Fetch live GitHub catalog data
- 📖 Open official API documentation
- 🧩 Discover APIs for real-world projects
- 🛟 Use fallback API data if GitHub becomes temporarily unavailable

---

# ✨ Core Features

## 🔎 Intelligent Search

Search APIs using keywords such as:

```text
weather
python
security
finance
books
AI
machine learning
crypto
automation
```

Search works across:

```text
API Name
+
Description
+
Category
```

---

## 📂 Category Explorer

Discover APIs from many categories including:

```text
AI
Animals
Books
Business
Cryptocurrency
Development
Finance
Games
Government
Health
Jobs
Machine Learning
Music
Programming
Science
Security
Sports
Weather
```

and many more.

---

## 🔐 Authentication Detection

NEXUS API displays authentication requirements such as:

```text
No Authentication
API Key
OAuth
Custom Authentication
```

This helps developers quickly find APIs that are easy to integrate.

---

## 🔒 HTTPS Security Information

Before using an API, you can check whether it supports:

```text
HTTPS
```

This is useful when building secure applications.

---

## 🌐 CORS Information

For browser-based web applications, CORS support can be important.

NEXUS API displays the available CORS information directly in the
dashboard.

---

# 📊 Live Dashboard

The application automatically calculates:

```text
Total APIs
Total Categories
HTTPS APIs
No-Authentication APIs
Search Results
```

The values are generated dynamically from the loaded API catalog.

---

# 🖥️ Advanced User Interface

NEXUS API includes a modern developer-focused interface.

### UI Highlights

```text
Dark Futuristic Theme
Glass UI
Gradient Effects
Developer Terminal Panel
Responsive Cards
Advanced Search Area
Two-Column API Grid
Hover Effects
Live Status Indicator
Mobile Responsive Layout
```

---

# 🛠️ Technology Stack

| Technology | Usage |
|---|---|
| 🐍 Python | Main programming language |
| ⚡ Streamlit | Interactive web application |
| 🐼 Pandas | Data processing |
| 🌐 Requests | Fetch GitHub API catalog |
| 🎨 HTML | Custom UI structure |
| 💅 CSS | Advanced visual design |
| 🐙 GitHub | Source code and API data |
| ☁️ Streamlit Cloud | Live deployment |

---

# 🏗️ Application Architecture

```text
              GitHub
                │
                ▼
      public-apis/public-apis
                │
                ▼
          Requests Library
                │
                ▼
          README Parser
                │
                ▼
             Pandas
                │
        ┌───────┴────────┐
        │                │
        ▼                ▼
     Search           Filters
        │                │
        └───────┬────────┘
                ▼
           Streamlit UI
                │
                ▼
            NEXUS API
```

---

# 📂 Project Structure

```text
nexus-api-explorer/
│
├── app.py
│
├── README.md
│
├── requirements.txt
│
├── .gitignore
│
└── assets/
    │
    └── nexus-api-banner.png
```

---

# ⚙️ Installation

## Step 1 — Clone Repository

```bash
git clone https://github.com/pintuaryan8973-source/nexus-api-explorer.git
```

Enter project folder:

```bash
cd nexus-api-explorer
```

---

## Step 2 — Create Virtual Environment

```bash
python -m venv .venv
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4 — Run Application

```bash
streamlit run app.py
```

The app will normally open on:

```text
http://localhost:8501
```

---

# 🪟 Windows PowerShell

If PowerShell does not allow virtual environment activation, run:

```powershell
python -m venv .venv
```

Then:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Then:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

---

# 🌐 Live Deployment

NEXUS API is deployed using **Streamlit Community Cloud**.

### Live Application

🚀 https://nexusapipintuaryan.streamlit.app

Deployment configuration:

```text
Repository:
pintuaryan8973-source/nexus-api-explorer

Branch:
main

Main File:
app.py
```

---

# 🔄 Automatic Updates

Because the application is connected with GitHub:

```text
VS Code
   │
   ▼
Git Commit
   │
   ▼
Git Push
   │
   ▼
GitHub
   │
   ▼
Streamlit Cloud
   │
   ▼
Updated Live App
```

So future changes can be published by running:

```powershell
git add .
git commit -m "Update NEXUS API"
git push
```

Streamlit will detect the GitHub update and redeploy the application.

---

# 💡 Project Ideas Using NEXUS API

Developers can discover APIs for projects like:

```text
Weather Application
Crypto Dashboard
AI Assistant
News Application
Book Finder
Job Search Platform
Finance Dashboard
Cybersecurity Tool
Movie Application
Sports Dashboard
Automation System
Machine Learning Application
Student Projects
Portfolio Projects
```

---

# 🧪 Example API Searches

### Weather

```text
weather
```

### Cybersecurity

```text
security
```

### Artificial Intelligence

```text
AI
```

### Finance

```text
finance
```

### Programming

```text
programming
```

---

# 🧠 Future Intelligence Features

NEXUS API can be upgraded further with intelligent features.

## 🤖 AI API Recommendation Engine

User could type:

```text
I want to build a weather application
```

and NEXUS API could automatically recommend suitable APIs.

---

## 💬 AI Assistant

Future versions can include an AI assistant where users ask:

```text
Which API should I use for cryptocurrency prices?
```

and the assistant recommends APIs from the catalog.

---

## 🧪 Built-in API Tester

Future version could allow users to test API endpoints directly inside
NEXUS API.

Example:

```text
GET
https://api.example.com/data
```

and display the JSON response.

---

## 📄 JSON Viewer

API responses could be displayed in a formatted JSON viewer.

Example:

```json
{
  "status": "success",
  "data": {
    "example": true
  }
}
```

---

## ⭐ Favorite APIs

Users could save useful APIs into their own collection.

Example:

```text
My APIs
│
├── Weather API
├── GitHub API
├── Crypto API
└── Books API
```

---

## 📊 API Analytics

Future versions could display:

```text
Popular APIs
Most Used Categories
Authentication Distribution
HTTPS Percentage
API Category Statistics
```

---

# 🗺️ Future Roadmap

```text
✅ Public API Explorer
✅ Search System
✅ Category Filter
✅ Authentication Filter
✅ HTTPS Detection
✅ CORS Information
✅ Live GitHub Catalog
✅ Advanced UI
✅ GitHub Repository
✅ Streamlit Deployment

⬜ AI API Recommendations
⬜ AI Assistant
⬜ API Testing Console
⬜ JSON Response Viewer
⬜ Favorite APIs
⬜ Saved Collections
⬜ User Accounts
⬜ API Analytics
⬜ API Key Manager
⬜ Advanced Search
```

---

# 📚 Data Source

API information is sourced from the community-maintained:

```text
public-apis/public-apis
```

GitHub repository.

The individual APIs belong to their respective owners and providers.

---

# 🔗 Important Links

### 🚀 Live Application

https://nexusapipintuaryan.streamlit.app

### 🐙 GitHub Repository

https://github.com/pintuaryan8973-source/nexus-api-explorer

---

# 🤝 Contributions

Contributions are welcome.

Typical contribution workflow:

```text
Fork Repository
      ↓
Create Branch
      ↓
Make Changes
      ↓
Commit Changes
      ↓
Push Branch
      ↓
Open Pull Request
```

---

# ⭐ Support

If you find NEXUS API useful, consider giving the repository a:

## ⭐ GitHub Star

It helps the project grow and motivates future improvements.

---

<p align="center">
  <b>⚡ NEXUS API</b>
</p>

<p align="center">
  Discover Faster • Build Smarter • Ship More
</p>

<p align="center">
  Built with Python + Streamlit
</p>