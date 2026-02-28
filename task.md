# SprintSync – Full Build Task List

## Phase 0: Setup & Estimation
- [ ] Initialize Git repo with proper `.gitignore`
- [ ] Create `estimates.csv` (first commit)
- [ ] Create project scaffold (FastAPI + folder structure)

## Phase 1: Database & Models
- [ ] Set up PostgreSQL config with SQLAlchemy/SQLModel
- [ ] Define User model (id, username, email, hashed_password, isAdmin)
- [ ] Define Task model (id, title, description, status, totalMinutes, assignee FK)
- [ ] Create migration/schema files + seed data script

## Phase 2: Auth System
- [ ] Implement password hashing (bcrypt)
- [ ] Implement JWT token creation & validation
- [ ] Create auth endpoints: POST `/auth/register`, POST `/auth/login`, GET `/auth/me`
- [ ] Add auth dependency for protected routes

## Phase 3: CRUD Endpoints
- [ ] User CRUD: GET list, GET by id, PUT, DELETE (admin only)
- [ ] Task CRUD: GET list (with filters), GET by id, POST, PUT, DELETE
- [ ] Task status transitions endpoint (PATCH `/tasks/{id}/status`)

## Phase 4: AI Assist
- [ ] Implement `/ai/suggest` endpoint
- [ ] Live LLM call (OpenAI/Gemini) for draft task description from title
- [ ] Deterministic stub JSON for tests/CI (env-based toggle)
- [ ] Graceful degradation on LLM failure

## Phase 5: Observability
- [ ] Structured request logging middleware (method, path, userId, latency)
- [ ] Stack traces on errors
- [ ] `/metrics` endpoint (Prometheus-style JSON)

## Phase 6: Testing
- [ ] ≥ 2 unit tests (happy paths – auth, task CRUD)
- [ ] 1 integration test hitting `/ai/suggest` stub
- [ ] pytest configuration

## Phase 7: DevOps & Deploy
- [ ] Create Dockerfile (multi-stage)
- [ ] Create docker-compose.yml (app + PostgreSQL)
- [ ] Deploy to free cloud (Render / Railway)

## Phase 8: Frontend SPA (Stretch)
- [ ] React SPA: task list, create/edit task, AI suggest button
- [ ] Auth login UI
- [ ] Integrate with backend API

## Phase 9: Stretch Goals
- [ ] `/stats/top-users` aggregate endpoint
- [ ] CI pipeline (GitHub Actions: lint → test → Docker build)

## Phase 10: Documentation & Polish
- [ ] Comprehensive README.md
- [ ] API docs (Swagger/Redoc auto-generated)
- [ ] Update `estimates.csv` with actuals
- [ ] Final commit tags
