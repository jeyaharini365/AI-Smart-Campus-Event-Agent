# AI Smart Campus Event Registration Agent

The **AI Smart Campus Event Registration Agent** is an intelligent, conversational system designed to streamline event discovery, registrations, query responses, and check-in verifications on a college campus. 

Rather than utilizing traditional forms, this project implements a **Stateful AI Agent (LangGraph)** powered by the **Google Gemini API** to run multi-turn conversational workflows. Students can discover events, check event availability, ask FAQs, register, or cancel tickets using natural language. Organizers can upload schedules, review check-ins, and analyze event metrics on a dashboard.

---

## 🚀 Technology Stack

* **Frontend:** React, Tailwind CSS
* **Backend:** Python, FastAPI, Motor (Async MongoDB Driver)
* **Database:** MongoDB Atlas (supporting Semantic Vector Search indexes)
* **AI Engine:** Google Gemini API (`gemini-1.5-flash`, `text-embedding-004`)
* **Agent Framework:** LangGraph (Stateful multi-turn workflows)
* **Hosting:** Vercel (Frontend), Render (Backend), MongoDB Atlas (Database)

---

## 📁 Repository Directory Structure

```
ai-smart-campus-event-registration-agent/
│
├── backend/
│   └── app/
│       ├── api/
│       │   └── v1/
│       │       ├── __init__.py
│       │       └── api.py              # Modular endpoints registry
│       │   └── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py            # Environment validation & loading
│       │   └── database.py          # Asynchronous Motor client pool helper
│       ├── dependencies/
│       │   ├── __init__.py
│       │   └── db.py                # Depends(get_db) dependency injections
│       ├── models/
│       │   ├── __init__.py
│       │   ├── chat_session.py      # Stateful chat threads schema
│       │   ├── event.py             # Event structures, FAQs, dynamic questions & vector embeddings
│       │   ├── notification.py      # System alerts schemas
│       │   ├── pyobjectid.py        # Serialized ObjectId Pydantic v2 validator
│       │   ├── registration.py      # Sign-ups and QR ticket tracking schemas
│       │   └── user.py              # Accounts, profiles, and credential structures
│       ├── middleware/
│       ├── repositories/
│       ├── services/
│       ├── utils/
│       ├── __init__.py
│       └── main.py                  # Lifespan events hook, CORS settings & initialization
│
├── .env.example                     # Environment template file
├── .gitignore                       # Git exclusions parameters
├── requirements.txt                 # Backend pip dependency configurations
└── README.md                        # Documentation and project manual
```

---

## 🛠️ Installation & Setup

Follow these steps to run the backend engine locally:

### 1. Prerequisite Installations
Ensure you have Python 3.10+ installed on your system.

### 2. Configure Environment Settings
1. Create a `.env` file in the root directory by copying the template:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your credentials:
   * Add your **MongoDB Atlas connection URI**.
   * Add your **Google Gemini API Key** (from Google AI Studio).
   * Customize your JWT keys, SMTP mail host configurations, etc.

### 3. Initialize Virtual Environment & Install Dependencies
Run the following commands inside the root workspace folder:
```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install required Python modules
pip install -r requirements.txt
```

### 4. Boot the FastAPI Server
Launch the local Uvicorn development server:
```bash
uvicorn backend.app.main:app --reload --port 8000
```

### 5. Access Interactive APIs
You can verify and test routes by browsing to:
* **Interactive swagger GUI:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Alternative redoc interface:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
* **Health Check Probe:** [http://localhost:8000/health](http://localhost:8000/health) returning `{"status": "healthy"}`
