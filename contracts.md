# API Contracts & Integration Plan

## Stack
- **Backend:** FastAPI + Motor (async MongoDB) + JWT + slowapi rate-limit + emergentintegrations for AI
- **DB:** MongoDB (local via `MONGO_URL`)
- **AI:** Emergent Universal LLM key → OpenAI `gpt-4o-mini` by default (configurable via `AI_MODEL` env)
- **Email:** console log only (dev mode)
- **File upload:** local disk at `/app/backend/uploads`, served via `/api/uploads/<filename>`

All routes prefixed with `/api` (Kubernetes ingress rule).

## Environment (`backend/.env`)
`MONGO_URL`, `DB_NAME`, `JWT_SECRET`, `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES`, `SEED_ADMIN_EMAIL`, `SEED_ADMIN_PASSWORD`, `UPLOAD_DIR`, `PUBLIC_UPLOAD_BASE`, `EMERGENT_LLM_KEY`, `AI_PROVIDER`, `AI_MODEL`

## MongoDB Collections
- `users` — `{id, email, password_hash, role, created_at}`
- `projects` — `{id, title, description, tags[], image_url, live_url, github_url, gradient, order, created_at}`
- `skills` — `{id, name, level (0-100), icon, order, created_at}`
- `about` — singleton `{id, name, role, tagline, bio[], location, email, available, stats[], socials{}, updated_at}`
- `messages` — contact submissions `{id, name, email, subject, body, read, created_at}`
- `chat_sessions` — `{session_id, history[{role, content, ts}], created_at, updated_at}`
- `analytics_events` — `{id, type, meta, path, ua, created_at}`

## REST Endpoints (all prefixed `/api`)

### Auth
- `POST /auth/login` — body `{email, password}` → `{access_token, token_type, user}`
- `GET /auth/me` — (JWT) → current user

### Projects
- `GET /projects` — public list
- `GET /projects/{id}` — public
- `POST /projects` — admin, body project shape
- `PUT /projects/{id}` — admin
- `DELETE /projects/{id}` — admin

### Skills
- `GET /skills` — public
- `POST /skills` — admin
- `PUT /skills/{id}` — admin
- `DELETE /skills/{id}` — admin

### About
- `GET /about` — public singleton
- `PUT /about` — admin (upsert)

### Contact + Messages
- `POST /contact` — public (rate-limited 5/min/IP) → store + console email
- `GET /messages` — admin list
- `PATCH /messages/{id}/read` — admin mark read
- `DELETE /messages/{id}` — admin

### Uploads
- `POST /uploads` — admin, multipart `file` → `{url, filename}`
- `GET /uploads/{filename}` — public static

### AI
- `POST /ai/chat` — public (rate-limited 20/min/IP), body `{session_id, message}` → `{reply, session_id}`
  RAG context: pulls current projects + skills + about from MongoDB on each call.
- `GET /ai/history/{session_id}` — public, chat history for a session

### Analytics
- `POST /analytics/event` — public, body `{type, meta?, path?}`
- `GET /analytics` — admin summary + recent events

## Frontend Integration Mapping
Current `mock.js` → live API:
- `personal`, `bio`, `stats`, `socials` → `GET /about`
- `skills` → `GET /skills`
- `projects` → `GET /projects`
- `navLinks` → stays static (client-side)
- Contact copy-email button stays, **add** a visible form later → `POST /contact`
- Floating chatbot widget (new) → `POST /ai/chat`

I'll create `frontend/src/lib/api.js` (axios instance + typed methods) and swap imports in components from `../../data/mock` to `../../lib/api` via React state fetched on mount. Added a lightweight chat widget component and keep graceful fallback to mock data if API fails (so the portfolio never appears broken).

## Security
- bcrypt via passlib
- JWT HS256
- slowapi: `/api/contact` 5/min, `/api/ai/chat` 20/min, default 120/min
- Pydantic v2 validation on every route
- CORS open (`*`) per env default

## Seed Script
`python /app/backend/scripts/seed.py` — creates admin user + copies current mock content (projects, skills, about) into DB so frontend integration is immediate.
