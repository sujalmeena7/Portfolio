# Deploy Backend to Render

## 1) Create MongoDB URL
Use MongoDB Atlas (recommended) and copy the connection string.

## 2) Deploy from Blueprint (recommended)
1. Push this repository to GitHub.
2. In Render: New + -> Blueprint.
3. Select the repository.
4. Render will read render.yaml from repo root.

## 3) Set environment variables
In the Render service settings, ensure these are set:

Required:
- MONGO_URL
- DB_NAME
- JWT_SECRET
- CORS_ORIGINS

Required only for AI routes (/api/ai/*):
- OPENAI_API_KEY

Optional:
- AI_PROVIDER (default: openai)
- AI_MODEL (default: gpt-4o-mini)
- JWT_ALGORITHM (default: HS256)
- JWT_EXPIRE_MINUTES (default: 720)
- SEED_ADMIN_EMAIL
- SEED_ADMIN_PASSWORD
- UPLOAD_DIR
- PUBLIC_UPLOAD_BASE

## 4) Verify deployment
After deploy, open:
- /api/
- /api/health

Expected /api/health response:
{"status":"ok","db":true}

If db=false, check MONGO_URL and Atlas IP access list.
