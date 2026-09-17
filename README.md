<p align="center">
  <img src="assets/nexus-api-banner.png"
       alt="NEXUS API Banner"
       width="100%">
</p>

<h1 align="center">⚡ NEXUS API</h1>

<h3 align="center">
  Intelligent Public API Discovery & Testing Platform
</h3>

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
  <img src="https://img.shields.io/badge/API-Live_Catalog-22D3EE?style=flat-square">
  <img src="https://img.shields.io/badge/Status-LIVE-32E08C?style=flat-square">
</p>

---

# 🚀 About NEXUS API

**NEXUS API** is a modern and intelligent **Public API Explorer and Testing Platform** built using **Python + Streamlit**.

It converts the huge `public-apis/public-apis` GitHub catalog into an easy-to-use interactive dashboard.

Developers and students can discover useful APIs, search categories, inspect authentication requirements, check HTTPS/CORS support and even test public API endpoints directly inside NEXUS API.

🌐 **Live Application**

https://nexusapipintuaryan.streamlit.app

---

# 🧠 What NEXUS API Can Do

NEXUS API allows users to:

- 🔎 Search APIs instantly
- 📂 Explore API categories
- 🔐 Check authentication requirements
- 🔒 Check HTTPS support
- 🌐 Check CORS availability
- 📊 View live API statistics
- ⚡ Fetch live GitHub API catalog data
- 📖 Open official API documentation
- 🧩 Discover APIs for real projects
- 🧪 Test public GET API endpoints
- 📄 View JSON responses
- 🛰️ View HTTP status codes
- 🔑 Test temporary Bearer Token authentication
- 🛟 Use fallback data if GitHub is unavailable

---

# ✨ Main Features

## 🔎 Smart API Search

Search APIs using:

```text
API Name
Category
Description
Technology
Project Idea
```

Example searches:

```text
weather
finance
security
books
machine learning
crypto
programming
```

---

## 📂 Category Explorer

NEXUS API contains many categories such as:

```text
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

# 🔐 Authentication Information

NEXUS API displays whether an API uses:

```text
No Authentication
API Key
OAuth
Custom Authentication
```

This helps developers understand an API before integrating it into a project.

---

# 🔒 HTTPS Detection

NEXUS API shows whether an API supports secure HTTPS communication.

Example:

```text
HTTPS: Yes
```

---

# 🌐 CORS Information

CORS information is useful for frontend developers building browser-based applications.

NEXUS API displays:

```text
CORS: Yes
CORS: No
CORS: Unknown
```

depending on the API.

---

# 🧪 Built-in API Tester

NEXUS API contains a built-in **Safe GET Request Console**.

Users can test public APIs without leaving the application.

### API Tester Features

- Test public GET endpoints
- Add query parameters
- Use optional Bearer Token authentication
- View HTTP status code
- View response content type
- View response headers
- Preview JSON responses
- Preview text responses
- Response size protection
- Local/private network protection

---

## 🧪 Example API Test

Test endpoint:

```text
https://jsonplaceholder.typicode.com/todos/1
```

Authentication:

```text
None
```

Query parameters:

```json
{}
```

Successful response:

```text
HTTP 200 OK
```

JSON response:

```json
{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
```

---

# 📊 Live Dashboard Statistics

NEXUS API dynamically displays:

```text
Total APIs
Total Categories
HTTPS APIs
No-Authentication APIs
Current Search Results
```

The statistics are generated from the live API catalog.

---

# 🖥️ Advanced Interface

NEXUS API includes a futuristic developer-focused interface.

### UI Features

```text
Dark Futuristic Theme
Glass UI
Gradient Effects
Developer Terminal Panel
Live Status Indicator
Responsive API Cards
Two-Column Result Grid
Advanced Filters
Modern Buttons
Hover Effects
Mobile Responsive Design
```

---

# 🛠️ Technology Stack

| Technology | Usage |
|---|---|
| 🐍 Python | Main programming language |
| ⚡ Streamlit | Web application |
| 🐼 Pandas | Data filtering and processing |
| 🌐 Requests | API and GitHub requests |
| 🎨 HTML | Custom UI structure |
| 💅 CSS | Advanced styling |
| 🐙 GitHub | Source code and API catalog |
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
      ┌────────┴────────┐
      │                 │
      ▼                 ▼
   Search             Filters
      │                 │
      └────────┬────────┘
               ▼
          Streamlit UI
               │
     ┌─────────┴─────────┐
     │                   │
     ▼                   ▼
API Explorer        API Tester
     │                   │
     └─────────┬─────────┘
               ▼
           NEXUS API
```

---

# 📂 Project Structure

```text
nexus-api-explorer/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── assets/
    └── nexus-api-banner.png
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/pintuaryan8973-source/nexus-api-explorer.git
```

Enter the project directory:

```bash
cd nexus-api-explorer
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run NEXUS API

```bash
streamlit run app.py
```

The application will normally open at:

```text
http://localhost:8501
```

---

# 🪟 Windows PowerShell Setup

If PowerShell does not allow virtual environment activation:

```powershell
python -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the application:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

---

# 🌐 Live Deployment

NEXUS API is deployed using **Streamlit Community Cloud**.

### 🚀 Live App

https://nexusapipintuaryan.streamlit.app

### Deployment Configuration

```text
Repository:
pintuaryan8973-source/nexus-api-explorer

Branch:
main

Main File:
app.py
```

---

# 🔄 Automatic Deployment Updates

The project follows this workflow:

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

Whenever code changes are ready:

```powershell
git add .
git commit -m "Update NEXUS API"
git push
```

Streamlit Cloud can then redeploy the latest GitHub version.

---

# 💡 Projects You Can Build

NEXUS API can help discover APIs for:

```text
Weather Application
Crypto Price Tracker
AI Assistant
Finance Dashboard
Cybersecurity Tool
Book Finder
Movie Application
News Website
Sports Dashboard
Job Search Platform
Automation System
Machine Learning Project
Student Projects
Portfolio Projects
```

---

# 🧪 Example Search Ideas

### Weather

```text
weather
```

### Cybersecurity

```text
security
```

### Finance

```text
finance
```

### Artificial Intelligence

```text
AI
```

### Books

```text
books
```

### Programming

```text
programming
```

---

# 🌟 Why NEXUS API?

Normally developers need to:

```text
Search Google
↓
Find API website
↓
Read documentation
↓
Check authentication
↓
Check HTTPS
↓
Test endpoint
```

NEXUS API simplifies this workflow:

```text
Search
+
Explore
+
Filter
+
Inspect
+
Test
```

inside one platform.

---

# 🧠 Future Intelligence Features

Future versions of NEXUS API can include:

## 🤖 AI API Recommendation Engine

A user could write:

```text
I want to build a weather application
```

and NEXUS API could recommend suitable APIs automatically.

---

## 💬 AI Assistant

Users could ask:

```text
Which API should I use for cryptocurrency prices?
```

and NEXUS API could suggest relevant APIs.

---

## 🧪 Advanced API Testing

Future API Tester upgrades can support:

```text
GET
POST
PUT
PATCH
DELETE
```

along with:

```text
Request Headers
JSON Body
Authentication
Response Timing
Response Size
```

---

## 📄 Advanced JSON Viewer

API responses can be displayed in a formatted expandable JSON viewer.

---

## ⭐ Favorite APIs

Users could save useful APIs into personal collections.

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

Future versions could include:

```text
Most Popular Categories
Authentication Distribution
HTTPS Percentage
API Statistics
API Response Performance
```

---

# 🗺️ Project Roadmap

```text
✅ Public API Explorer
✅ Search System
✅ Category Filters
✅ Authentication Filter
✅ HTTPS Detection
✅ CORS Information
✅ Live GitHub Catalog
✅ Advanced UI
✅ GitHub Repository
✅ Streamlit Deployment
✅ Built-in GET API Tester
✅ JSON Response Viewer
✅ Bearer Token Testing

⬜ POST Requests
⬜ PUT Requests
⬜ PATCH Requests
⬜ DELETE Requests
⬜ AI API Recommendations
⬜ AI Assistant
⬜ Favorite APIs
⬜ Saved Collections
⬜ User Accounts
⬜ API Analytics
⬜ API Key Manager
```

---

# 📚 Data Source

API information is sourced from the community-maintained:

```text
public-apis/public-apis
```

GitHub repository.

Individual APIs and services belong to their respective providers.

---

# 🔗 Important Links

## 🚀 Live Application

https://nexusapipintuaryan.streamlit.app

## 🐙 GitHub Repository

https://github.com/pintuaryan8973-source/nexus-api-explorer

---

# 🤝 Contributions

Contributions are welcome.

Contribution workflow:

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

# ⭐ Support NEXUS API

If you find this project useful, consider giving the repository a:

## ⭐ GitHub Star

It helps support future improvements.

---

<p align="center">
  <b>⚡ NEXUS API</b>
</p>

<p align="center">
  Search • Discover • Test • Build
</p>

<p align="center">
  <b>Discover Faster • Build Smarter • Ship More</b>
</p>

<p align="center">
  Built with Python + Streamlit
</p>