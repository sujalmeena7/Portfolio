# Sujal Meena - Full Stack Developer Portfolio

<div align="center">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind" />
  <img src="https://img.shields.io/badge/ThreeJs-black?style=for-the-badge&logo=three.js&logoColor=white" alt="Three.js" />
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI" />
</div>

## 🚀 Overview
Welcome to the source code for my professional portfolio. Designed and engineered to be more than just a static site, this platform serves as a **dynamic full-stack application** that highlights my expertise in modern web engineering, API design, and AI integration.

The architecture separates the presentation layer from business logic, utilizing a **React + Tailwind** frontend driven by a scalable **FastAPI + MongoDB** backend.

## ✨ Key Technical Features

- **AI-Powered RAG Chatbot:** Integrated an LLM-powered assistant (OpenAI `gpt-4o-mini`) that utilizes Retrieval-Augmented Generation (RAG) to dynamically answer recruiter questions based on the live database of my projects, skills, and bio.
- **Custom Headless CMS:** Built a secured, JWT-authenticated Admin Dashboard to perform CRUD operations on portfolio content (Projects, Skills, About section) without requiring codebase modifications.
- **High-Performance UI:** Implemented responsive, accessible, and interactive interfaces using **shadcn/ui** and **Radix UI** components. Leveraged **Three.js** for custom 3D web graphics.
- **Robust API Engineering:** Engineered a RESTful backend with **FastAPI**, incorporating dependency injection, Pydantic data validation (v2), async MongoDB operations (Motor), and route-level rate limiting (`slowapi`).
- **Production-Ready Security:** Implemented role-based access control (RBAC), bcrypt password hashing, path traversal guards for local file uploads, and global CORS policies.

## 🏗️ Architecture & Tech Stack

### Frontend (`/frontend`)
- **Framework:** React 19
- **Styling:** Tailwind CSS, `clsx`, `tailwind-merge`
- **UI Components:** shadcn/ui, Radix UI Primitives, Lucide Icons, Embla Carousel
- **Graphics/Animation:** Three.js
- **State/Routing:** React Router v7, React Hook Form (with Zod validation)
- **API Client:** Axios (with auth interceptors)

### Backend (`/backend`)
- **Framework:** FastAPI (Python 3.11+)
- **Database:** MongoDB (Motor async driver)
- **Authentication:** JWT (JSON Web Tokens), Passlib (bcrypt)
- **AI Integration:** OpenAI `gpt-4o-mini` (via custom RAG pipeline)
- **Utilities:** `slowapi` (Rate Limiting)

*(For detailed backend documentation, refer to the [Backend Integration & Deployment Guide](./BACKEND_GUIDE.md))*

## 🛠️ Local Development Setup

### Prerequisites
- Node.js (v18+)
- Python (v3.11+)
- MongoDB (running locally on port `27017` or Atlas URI)

### 1. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create a .env file based on environment variables found in BACKEND_GUIDE.md
# Ensure MongoDB is running locally or provide a valid URI

# Seed the database with the initial admin user and sample data
python scripts/seed.py

# Run the FastAPI development server
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```
*The backend API will be available at `http://localhost:8001/api` and Swagger Docs at `http://localhost:8001/docs`.*

### 2. Frontend Setup

```bash
# Navigate to the frontend directory
cd frontend

# Install Node modules
yarn install

# Start the development server
yarn start
```
*The React app will be available at `http://localhost:3000`.*

## 📈 Analytics & Monitoring
Built-in lightweight event tracking endpoint `/api/analytics/event` to monitor page views, project clicks, and resume downloads, securely accessible only via the Admin panel.

## 🤝 Let's Connect
Feel free to explore the code! If you're a recruiter or hiring manager looking for a detail-oriented full-stack engineer who builds scalable, user-centric products—I'd love to chat.
Reach out via the contact form on my portfolio or find me on [LinkedIn](#).

---
*Designed & Built by Sujal Meena*
