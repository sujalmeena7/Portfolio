# Portfolio Backend — Integration & Deployment Guide

> **Stack:** FastAPI · Motor (async MongoDB) · JWT · slowapi · Emergent Universal LLM (OpenAI `gpt-4o-mini`) · local-disk uploads · console-logged email (dev)

---

## 1. Folder Structure

```
/app/backend
├── server.py               # FastAPI app, routers, startup
├── .env                    # MONGO_URL, JWT_SECRET, EMERGENT_LLM_KEY, ...
├── requirements.txt
├── uploads/                # served at /api/uploads/<filename>
├── core/
│   ├── config.py           # settings loader
│   ├── database.py         # motor client + db
│   ├── security.py         # JWT + bcrypt + require_admin dep
│   └── rate_limit.py       # slowapi limiter
├── models/
│   └── schemas.py          # pydantic models for every resource
├── routers/
│   ├── auth.py             # /api/auth/*
│   ├── projects.py         # /api/projects/*
│   ├── skills.py           # /api/skills/*
│   ├── about.py            # /api/about
│   ├── contact.py          # /api/contact, /api/messages/*
│   ├── uploads.py          # /api/uploads/*
│   ├── ai.py               # /api/ai/*
│   └── analytics.py        # /api/analytics/*
├── services/
│   ├── ai_service.py       # RAG loop with emergentintegrations
│   └── email_service.py    # console-log notifier
└── scripts/
    └── seed.py             # admin + sample data
```

---

## 2. Environment (`/app/backend/.env`)

```bash
MONGO_URL="mongodb://localhost:27017"
DB_NAME="test_database"
CORS_ORIGINS="*"

# Auth
JWT_SECRET="replace-with-long-random-string"
JWT_ALGORITHM="HS256"
JWT_EXPIRE_MINUTES=720

# Admin seed
SEED_ADMIN_EMAIL="admin@portfolio.dev"
SEED_ADMIN_PASSWORD="Admin@123"

# Uploads
UPLOAD_DIR="/app/backend/uploads"
PUBLIC_UPLOAD_BASE="/api/uploads"

# AI (Emergent Universal key)
EMERGENT_LLM_KEY="sk-emergent-..."
AI_PROVIDER="openai"
AI_MODEL="gpt-4o-mini"
```

---

## 3. Developer Setup

```bash
# one-time (deps already installed in this env)
cd /app/backend
pip install -r requirements.txt

# seed admin + sample data
python scripts/seed.py

# supervisor already runs the server; restart after env changes
sudo supervisorctl restart backend

# tail logs
tail -f /var/log/supervisor/backend.*.log

# swagger docs (auto-generated)
open http://localhost:8001/docs
```

Admin login (from seed):
- `admin@portfolio.dev` / `Admin@123`

---

## 4. API Reference (all routes prefixed `/api`)

### Auth
| Method | Path | Auth | Body | Returns |
|---|---|---|---|---|
| POST | `/auth/login` | public | `{email, password}` | `{access_token, token_type, user}` |
| GET | `/auth/me` | Bearer | — | `UserPublic` |

### Projects
| Method | Path | Auth |
|---|---|---|
| GET | `/projects` | public |
| GET | `/projects/{id}` | public |
| POST | `/projects` | admin |
| PUT | `/projects/{id}` | admin |
| DELETE | `/projects/{id}` | admin |

`ProjectInput`: `{title, description, tags[], image_url?, live_url?, github_url?, gradient?, order?}`

### Skills
Same CRUD pattern. `SkillInput`: `{name, level (0-100), icon, order}`.

### About (singleton)
| Method | Path | Auth |
|---|---|---|
| GET | `/about` | public |
| PUT | `/about` | admin (upsert) |

`AboutInput`: `{name, role, tagline, bio[], location, email, available, stats[{label,value,suffix}], socials{github,linkedin,twitter,...}}`

### Contact + Messages
| Method | Path | Auth | Notes |
|---|---|---|---|
| POST | `/contact` | public | **Rate-limited 5/min/IP** — stores message + console-logs email |
| GET | `/messages` | admin | |
| PATCH | `/messages/{id}/read` | admin | |
| DELETE | `/messages/{id}` | admin | |

### Uploads (local disk)
| Method | Path | Auth |
|---|---|---|
| POST | `/uploads` | admin — multipart `file` |
| GET | `/uploads/{filename}` | public |

Returns `{filename, url, size, content_type}`. Allowed: png, jpg, jpeg, webp, gif, svg, pdf (≤ 10 MB).

### AI Chat (RAG)
| Method | Path | Auth | Notes |
|---|---|---|---|
| POST | `/ai/chat` | public | **Rate-limited 20/min/IP**. Body `{session_id, message}`. Fresh portfolio context (projects/skills/about) is pulled from DB on every call and injected into the system prompt. |
| GET | `/ai/history/{session_id}` | public | Returns full turn list. |

### Analytics
| Method | Path | Auth |
|---|---|---|
| POST | `/analytics/event` | public — `{type, meta?, path?}` |
| GET | `/analytics` | admin — summary `{total_events, by_type, last_7_days, recent[]}` |

---

## 5. Example Requests / Responses

### Login
```bash
POST /api/auth/login
{"email":"admin@portfolio.dev","password":"Admin@123"}

→ 200
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": { "id":"...", "email":"admin@portfolio.dev", "role":"admin", "created_at":"..." }
}
```

### Create Project (admin)
```bash
POST /api/projects
Authorization: Bearer <token>
{
  "title": "Synth Atlas",
  "description": "Interactive sound-design dictionary.",
  "tags": ["React","Web Audio"],
  "live_url": "https://synth.example.com",
  "github_url": "https://github.com/acme/synth",
  "order": 4
}
```

### AI Chat (multi-turn)
```bash
POST /api/ai/chat
{"session_id":"visitor-42","message":"Which projects use Three.js?"}

→ 200
{
  "session_id": "visitor-42",
  "reply": "Two projects lean heavily on Three.js: **Nebula Commerce** (React + GSAP + Shopify) and **Signal Garden** (Web Audio + GLSL + Canvas). Want more detail on either?"
}
```

### Contact Form
```bash
POST /api/contact
{"name":"Mara","email":"mara@studio.co","subject":"Website rebuild","body":"Hi Alex, can we chat?"}

→ 201
{"id":"...","name":"Mara","email":"mara@studio.co","read":false,"created_at":"..."}
```

Backend console also logs:
```
===== NEW CONTACT MESSAGE =====
To:      admin@portfolio.dev
From:    Mara <mara@studio.co>
Subject: Website rebuild
Body:    Hi Alex, can we chat?
================================
```

---

## 6. React Integration — How Your Frontend Uses This

**Already wired** in this project:

### Axios client — `/app/frontend/src/lib/api.js`
```js
import axios from "axios";
const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export const http = axios.create({ baseURL: API, timeout: 30000 });
http.interceptors.request.use((cfg) => {
  const t = localStorage.getItem("pf_admin_token");
  if (t) cfg.headers.Authorization = `Bearer ${t}`;
  return cfg;
});

export const fetchProjects = () => http.get("/projects").then((r) => r.data);
export const fetchSkills   = () => http.get("/skills").then((r) => r.data);
export const fetchAbout    = () => http.get("/about").then((r) => r.data);
export const submitContact = (b) => http.post("/contact", b).then((r) => r.data);
export const aiChat = ({ sessionId, message }) =>
  http.post("/ai/chat", { session_id: sessionId, message }).then((r) => r.data);
export const trackEvent = (type, meta=null, path=null) =>
  http.post("/analytics/event", { type, meta, path }).catch(() => {});
```

### Component pattern (React 19, hooks — no Redux needed)
```jsx
import { useEffect, useState } from "react";
import { fetchProjects } from "../lib/api";

function Projects() {
  const [projects, setProjects] = useState([]);
  useEffect(() => { fetchProjects().then(setProjects); }, []);
  return <>{projects.map(p => <Card key={p.id} project={p} />)}</>;
}
```

### Rules already followed
1. **Never hardcode URLs** — always `process.env.REACT_APP_BACKEND_URL`.
2. **Every backend route is `/api`-prefixed** (Kubernetes ingress maps `/api/*` → port 8001).
3. **JWT token** stored in `localStorage` under `pf_admin_token`, injected automatically by the axios interceptor.
4. **Graceful fallback**: if API is unreachable, `fetchProjects/Skills/About` return the `mock.js` data so the site never appears broken.
5. **Chat widget** (`ChatWidget.jsx`) persists a random `session_id` in `localStorage` so multi-turn context survives refreshes.

### Admin login flow (for when you build `/admin` later)
```jsx
import { login, me, logout } from "../lib/api";

async function handleLogin(email, password) {
  await login(email, password);      // stores JWT
  const user = await me();            // verify, get profile
  navigate("/admin");
}
```

---

## 7. Security Notes

- **Passwords**: bcrypt via passlib (cost 12 default).
- **JWT**: HS256, 12-hour expiry. Rotate `JWT_SECRET` in prod.
- **Rate limits**: `/api/contact` 5/min, `/api/ai/chat` 20/min, global 120/min (per IP).
- **Upload safety**: extension allowlist + 10 MB max + random UUID filenames + path traversal guard.
- **CORS**: defaults to `*`; tighten via `CORS_ORIGINS` env on prod.
- **Validation**: every endpoint uses Pydantic v2 — invalid payloads return 422 with field-level errors automatically.

---

## 8. Deployment

### Option A — Render (recommended, free tier works)
1. **MongoDB**: spin up a free [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) cluster, copy the SRV connection string.
2. Push `/app/backend` to a GitHub repo (or add this subfolder to your main repo).
3. In Render → New → **Web Service** → connect repo.
   - Runtime: **Python 3.11**
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - Environment: copy every variable from `.env`, but set `MONGO_URL` to your Atlas URI and regenerate `JWT_SECRET`.
4. Add a **Persistent Disk** (1 GB is plenty) mounted at `/app/backend/uploads` so uploads survive redeploys.
5. After first deploy, open the Render Shell and run: `python scripts/seed.py`.
6. Point your frontend's `REACT_APP_BACKEND_URL` to the Render URL (e.g. `https://portfolio-api.onrender.com`).

### Option B — Railway
Same recipe; Railway detects FastAPI automatically. Use their Volume feature for `/app/backend/uploads`.

### Production checklist
- [ ] Rotate `JWT_SECRET` and `SEED_ADMIN_PASSWORD`
- [ ] Restrict `CORS_ORIGINS` to your domain(s)
- [ ] Use a managed MongoDB (Atlas) with IP allowlist
- [ ] Enable HTTPS (Render/Railway do this automatically)
- [ ] Consider adding Sentry or Logtail for logs
- [ ] Swap `/services/email_service.py` to SendGrid / Resend when you want real emails (1 file change)

---

## 9. Next Steps You Can Ship in ~30 min each

- **Admin dashboard** at `/admin` — login form → CRUD tables for projects/skills/about + messages inbox. All endpoints exist; just needs a React page.
- **Image upload in project editor** — wire the existing `POST /api/uploads` into a drag-drop zone, store the returned URL as `image_url` on the project.
- **Real email** — replace `email_service.py` body with a SendGrid `Mail` call. Contract stays the same.
- **Chat streaming** — the `emergentintegrations` library supports streamed responses; convert `/ai/chat` to SSE and pipe tokens to the widget.
- **Vector RAG** — current RAG is keyword-lite (full portfolio context injected every turn). For larger content, add `openai-embeddings` + a `chunks` collection with cosine search.

---

*API is live now at your `REACT_APP_BACKEND_URL + /api`. Swagger interactive docs at `/docs`.*
