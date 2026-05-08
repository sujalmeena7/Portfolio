<div align="center">
  <img src="https://img.icons8.com/fluency/96/portfolio.png" alt="Portfolio Logo" width="80" />
  <h1>Sujal Meena Portfolio</h1>
  <p><b>Dynamic Full-Stack Developer Platform & AI Concierge</b></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.11" />
    <img src="https://img.shields.io/badge/FastAPI-0.115-005571?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React 19" />
    <img src="https://img.shields.io/badge/MongoDB-Motor-47A248?style=flat-square&logo=mongodb&logoColor=white" alt="MongoDB" />
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="License MIT" />
  </p>

  <p>A high-performance, AI-integrated portfolio ecosystem. Features a custom RAG-powered chatbot, a secured headless CMS, and real-time analytics, all engineered for production scalability.</p>
</div>

---

## Table of Contents

- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [Deployment](#deployment)
- [AI Capabilities](#ai-capabilities)
- [Let's Connect](#lets-connect)

---

## Architecture

The system follows a modern decoupled architecture:
- **Frontend:** A responsive Single Page Application (SPA) built with React 19 and Tailwind CSS, focused on performance and accessibility.
- **Backend:** A RESTful API built with FastAPI, utilizing asynchronous patterns for MongoDB interactions and AI processing.
- **AI Layer:** A Retrieval-Augmented Generation (RAG) pipeline that injects live portfolio data into LLM prompts for context-aware interactions.

---

## Project Structure

```bash
/c:/project/Portfolio
├── backend/                # FastAPI application
│   ├── core/               # Configuration, database, and security
│   ├── models/             # Pydantic schemas
│   ├── routers/            # API endpoints (Auth, Projects, Skills, AI, etc.)
│   ├── services/           # Business logic (AI service, Email)
│   └── server.py           # Application entry point
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # UI components (shadcn/ui)
│   │   ├── lib/            # API client and utilities
│   │   └── pages/          # Portfolio sections
├── .github/                # CI/CD workflows (AWS EC2 deployment)
└── README.md               # You are here
```

---

## Tech Stack

| Component | Technologies |
| :--- | :--- |
| **Frontend** | React 19, Tailwind CSS, shadcn/ui, Three.js, Framer Motion |
| **Backend** | FastAPI, Python 3.11, Pydantic v2, Motor (Async MongoDB) |
| **Database** | MongoDB Atlas |
| **AI/LLM** | Gemini 1.5 Flash, LiteLLM, RAG Pipeline |
| **Auth** | JWT (JSON Web Tokens), Bcrypt hashing |
| **Infrastructure** | AWS EC2, GitHub Actions, PM2, Vercel |

---

## Quick Start

### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install -r requirements.txt
python scripts/seed.py    # Initialize admin user
uvicorn server:app --reload --port 8001
```

### 2. Frontend Setup
```bash
cd frontend
yarn install
yarn start
```

---

## Environment Variables

| Variable | Description |
| :--- | :--- |
| `MONGO_URL` | MongoDB connection string |
| `JWT_SECRET` | Secret key for token signing |
| `GEMINI_API_KEY` | Google AI Studio API key |
| `AI_PROVIDER` | Set to `gemini` |
| `AI_MODEL` | `gemini/gemini-pro` or `gemini/gemini-1.5-flash` |

---

## Deployment

The project is configured for automated deployment:
- **Backend:** Deployed to **AWS EC2** via GitHub Actions. Process management handled by **PM2**.
- **Frontend:** Optimized for **Vercel** or any static hosting platform.

---

## AI Capabilities

The "AI Concierge" is the centerpiece of the portfolio:
- **RAG Implementation:** Automatically fetches your latest projects and skills from the database to answer recruiter questions accurately.
- **Provider Agnostic:** Built with LiteLLM, allowing seamless switching between Gemini, OpenAI, and other providers.
- **Context Persistence:** Maintains session-based chat history in MongoDB for natural, multi-turn conversations.

---

## Let's Connect

Feel free to explore the code! If you're a recruiter or hiring manager looking for a detail-oriented full-stack engineer:
- **Portfolio:** [Visit Live Site](#)
- **LinkedIn:** [Sujal Meena](#)
- **Email:** [meenasujal60@gmail.com](mailto:meenasujal60@gmail.com)

---
<div align="center">
  <i>Designed & Engineered by Sujal Meena</i>
</div>
