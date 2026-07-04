# Systems Walkthrough: AI Smart Campus Event Registration Agent Foundation

This document details the backend foundations and database layer created for the **AI Smart Campus Event Registration Agent** application.

---

## 1. Project Directory Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   └── api.py                  # Mounts router definitions
│   │   └── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                # Environment configurations loading settings
│   │   └── database.py              # Async MongoDB connector
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── db.py                    # Database injection dependencies (Depends(get_db))
│   ├── models/
│   │   ├── __init__.py
│   │   ├── chat_session.py          # Chat session history Pydantic schema
│   │   ├── event.py                 # Events parameters and vectors schema
│   │   ├── notification.py          # Notification alerts schemas
│   │   ├── pyobjectid.py            # BSON serialization utility helper
│   │   ├── registration.py          # Registrations & tickets schemas
│   │   └── user.py                  # User profiles and authentication schemas
│   ├── middleware/
│   │   └── __init__.py
│   ├── repositories/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   ├── utils/
│   │   └── __init__.py
│   ├── __init__.py
│   └── main.py                      # Application bootstrap & middleware configs
```

---

## 2. Walkthrough of Main Features

### 2.1. Lifespan Database Management
The application implements modern FastAPI lifespan management. On server start, it establishes a persistent connection pool using MongoDB Motor driver, and closes the connection pool gracefully when shutdown signals are received:
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()
```

### 2.2. Configuration & Environment Injection
Values are safely loaded from environment files (`.env`) with fail-safes. The application supports standard logging with level controls configured via setting parameters:
* Path: [config.py](file:///c:/Users/D%20E%20L%20L/Desktop/AI%20smart%20campus%20event%20registeration%20agent/backend/app/core/config.py)

### 2.3. Health Checking
A clean, lightweight monitoring route is set up at `/health`. Returning a standard status code verifies database and web sockets viability:
* Endpoint: `GET /health` -> `{"status": "healthy"}`

---

## 3. How to Run the Backend Local Instance

### Prerequisites
Install dependencies in your python environment:
```bash
pip install fastapi uvicorn motor pydantic pydantic-settings email-validator
```

### Starting the Server
Run the uvicorn development server from the project directory containing `backend`:
```bash
uvicorn backend.app.main:app --reload --port 8000
```
Once run, you can view the automated OpenAPI documentation at:
* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
