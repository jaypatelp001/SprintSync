# ⚡ SprintSync

**AI-Powered Sprint Management Tool** — A lean internal tool for AI consultancies where engineers log work, track time, and leverage LLM-powered planning assistance.

🔗 **Live Frontend**: https://selfless-serenity-production-a6b0.up.railway.app  
🔗 **Live API**: https://sprintsync-production-0bd2.up.railway.app  
📺 **Video Walkthrough**: [Loom Walkthrough](https://www.loom.com/share/6f39de545521498b94176d1d497cfb19)  
📖 **API Docs**: https://sprintsync-production-0bd2.up.railway.app/docs

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────────────────────────────┐
│   React SPA     │────▶│           FastAPI Backend                │
│   (Vite)        │     │                                          │
│  • Login/Auth   │     │  ┌────────┐ ┌──────┐ ┌──────┐ ┌──────┐ │
│  • Dashboard    │     │  │  Auth  │ │ CRUD │ │  AI  │ │Stats │ │
│  • Task CRUD    │     │  │ (JWT)  │ │Users/│ │Assist│ │Metrics│ │
│  • AI Suggest   │     │  │bcrypt  │ │Tasks │ │ LLM+ │ │Prom. │ │
│                 │     │  └────────┘ └──────┘ │ Stub │ └──────┘ │
└─────────────────┘     │                      └──────┘          │
                        │  ┌──────────────────────────────┐      │
                        │  │  Middleware: Structured       │      │
                        │  │  Request Logging (JSON)       │      │
                        │  └──────────────────────────────┘      │
                        └────────────────┬─────────────────────────┘
                                         │
                        ┌────────────────▼─────────────────┐
                        │      PostgreSQL / SQLite         │
                        │  Users • Tasks (with statuses)   │
                        └──────────────────────────────────┘
```

### Tech Stack

| Layer          | Technology                                     |
|----------------|-------------------------------------------------|
| **Backend**    | Python 3.11, FastAPI, SQLAlchemy, Alembic       |
| **Frontend**   | React 19, Vite 7, Vanilla CSS (dark theme)      |
| **Database**   | PostgreSQL 15 (prod) / SQLite (dev/test)        |
| **Auth**       | JWT (python-jose) + bcrypt (passlib)            |
| **AI**         | Google Gemini 2.5 Flash + deterministic stub    |
| **DevOps**     | Docker, docker-compose, GitHub Actions CI       |
| **Testing**    | pytest, httpx, 16 tests                        |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & docker-compose (optional)

### Option 1: Docker (Recommended)

```bash
# Clone and start
git clone <repo-url>
cd CodeStartLab
docker-compose up --build

# Seed demo data
docker-compose exec api python seed.py
```

API: http://localhost:8000/docs  
Frontend: http://localhost:5173 (auto-started by docker-compose)

### Option 2: Local Development

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
cp .env.example .env      # Edit as needed

# Seed database & run
python seed.py
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Demo Credentials
| User    | Password    | Role   |
|---------|-------------|--------|
| admin   | admin123    | Admin  |
| alice   | alice123    | User   |
| bob     | bob123      | User   |

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint          | Description           |
|--------|-------------------|-----------------------|
| POST   | `/auth/register`  | Register new user     |
| POST   | `/auth/login`     | Login, get JWT        |
| GET    | `/auth/me`        | Current user profile  |

### Tasks
| Method | Endpoint                  | Description                    |
|--------|---------------------------|--------------------------------|
| GET    | `/tasks/`                 | List tasks (filter by status)  |
| POST   | `/tasks/`                 | Create task                    |
| GET    | `/tasks/{id}`             | Get task by ID                 |
| PUT    | `/tasks/{id}`             | Update task                    |
| DELETE | `/tasks/{id}`             | Delete task                    |
| PATCH  | `/tasks/{id}/status`      | Transition status              |
| POST   | `/tasks/{id}/log-time`    | Log time to task               |

### AI Assist
| Method | Endpoint        | Description                              |
|--------|-----------------|------------------------------------------|
| POST   | `/ai/suggest`   | Generate description or daily plan       |

### Users (Admin)
| Method | Endpoint          | Description           |
|--------|-------------------|-----------------------|
| GET    | `/users/`         | List all users        |
| GET    | `/users/{id}`     | Get user by ID        |
| PUT    | `/users/{id}`     | Update user           |
| DELETE | `/users/{id}`     | Delete user           |

### Observability & Stats
| Method | Endpoint              | Description                    |
|--------|-----------------------|--------------------------------|
| GET    | `/metrics`            | Prometheus-style JSON metrics  |
| GET    | `/stats/top-users`    | Top users by logged minutes    |
| GET    | `/stats/cycle-time`   | Avg cycle time per status      |

---

## 🧪 Testing

```bash
cd backend
AI_STUB_MODE=true python -m pytest tests/ -v
```

**16 tests covering:**
- ✅ Auth: register, login, session validation, duplicate handling
- ✅ Tasks: CRUD, status transitions (valid + invalid), filtering
- ✅ AI: stub description, daily plan, error handling, auth guard

---

## 🤖 AI Assist Design

The `/ai/suggest` endpoint supports two modes:

1. **Description mode**: Given a short task title, generates a full task description
2. **Daily plan mode**: Analyzes the user's current tasks and creates a prioritized plan

**Dual-mode architecture:**
- **Live LLM**: Calls Google Gemini 2.5 Flash when `AI_STUB_MODE=false` and `GOOGLE_API_KEY` is set
- **Deterministic stub**: Returns predictable JSON for tests and CI (`AI_STUB_MODE=true`)
- **Graceful degradation**: If the LLM call fails, automatically falls back to stub with a warning

---

## 📊 Observability

- **Structured Logging**: Every request logs JSON with `method`, `path`, `userId`, `latency_ms`, `status_code`
- **Error Stack Traces**: 5xx errors include full Python stack traces
- **Metrics Endpoint**: `/metrics` returns Prometheus-style JSON with request counters, latency histograms, and app gauges

---

## 🔄 Status Transitions

Tasks follow a defined state machine:
```
TODO → IN_PROGRESS → REVIEW → DONE
  ↑          ↓          ↓       ↓
  └──────────┘          └───────┘
       (back to TODO for reopen)
```

Invalid transitions are rejected with a descriptive error message.

---

## 📋 Commit History

| Tag    | Description                                         |
|--------|-----------------------------------------------------|
| v0.1   | Project init with estimates and folder structure    |
| v0.2   | Database models, config, and seed data              |
| v0.3   | JWT authentication system                           |
| v0.4   | CRUD endpoints for users and tasks                  |
| v0.5   | AI assist with LLM + stub fallback                  |
| v0.7   | Unit and integration tests — 16 tests passing       |
| v0.8   | Docker, docker-compose, stats endpoints, CI pipeline|
| v0.9   | React frontend SPA                                  |
| v1.0   | Documentation and polish                            |

---

## 📝 Design Decisions & Trade-offs

1. **SQLite for dev/test, PostgreSQL for prod** — Zero-setup local dev while maintaining production readiness
2. **Sync SQLAlchemy over async** — Simpler code, easier debugging; the API is I/O-bound on DB, not CPU
3. **In-memory metrics** — Acceptable for MVP; production would use Prometheus client
4. **JWT over sessions** — Stateless auth scales better and simplifies the frontend
5. **Deterministic AI stub** — Ensures CI never flakes due to LLM API instability

---

## 📄 License

MIT
