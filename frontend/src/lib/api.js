import axios from "axios";
import { projects as mockProjects, skills as mockSkills, about as mockAbout } from "../data/mock";


// Use empty string in production so requests go to /api/... and Vercel proxies them.
// In development, it will fall back to localhost or the provided env var.
const DEFAULT_BACKEND_URL = process.env.NODE_ENV === 'production' ? '' : 'http://localhost:8000';
const BASE_URL = (process.env.REACT_APP_BACKEND_URL || DEFAULT_BACKEND_URL).replace(/\/$/, "");
const API = `${BASE_URL}/api`;

// Axios instance with token injection
export const http = axios.create({
  baseURL: API,
  timeout: 30000,
});

const TOKEN_KEY = "pf_admin_token";

export const setToken = (t) => {
  if (t) localStorage.setItem(TOKEN_KEY, t);
  else localStorage.removeItem(TOKEN_KEY);
};
export const getToken = () => localStorage.getItem(TOKEN_KEY);

http.interceptors.request.use((config) => {
  const t = getToken();
  if (t) config.headers.Authorization = `Bearer ${t}`;
  return config;
});

function logApiError(endpoint, error) {
  console.error(`[api] ${endpoint} failed`, error);
}

// ---------- Public API ----------
const withRetry = async (fn, retries = 3, delay = 2000) => {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === retries - 1) throw error;
      console.warn(`[api] Request failed, retrying in ${delay}ms... (${i + 1}/${retries})`);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }
};

export async function fetchAbout() {
  try {
    const { data } = await withRetry(() => http.get("/about"), 5, 3000);
    return data;
  } catch (error) {
    logApiError("GET /about", error);
    return mockAbout;
  }
}

export async function fetchProjects() {
  try {
    const { data } = await withRetry(() => http.get("/projects"), 5, 3000);
    if (!Array.isArray(data)) throw new Error("Invalid projects response shape");
    // If backend returns empty, also consider fallback
    if (data.length === 0) return mockProjects;
    return data.map(normalizeProject);
  } catch (error) {
    logApiError("GET /projects", error);
    return mockProjects;
  }
}

export async function fetchSkills() {
  try {
    const { data } = await withRetry(() => http.get("/skills"), 5, 3000);
    if (!Array.isArray(data)) throw new Error("Invalid skills response shape");
    if (data.length === 0) return mockSkills;
    return data;
  } catch (error) {
    logApiError("GET /skills", error);
    return mockSkills;
  }
}

export async function submitContact({ name, email, subject, body }) {
  const { data } = await http.post("/contact", { name, email, subject, body });
  return data;
}

// ---------- AI ----------
export async function aiChat({ sessionId, message }) {
  const { data } = await http.post("/ai/chat", { session_id: sessionId, message });
  return data;
}

export async function aiHistory(sessionId) {
  const { data } = await http.get(`/ai/history/${sessionId}`);
  return data;
}

// ---------- Analytics ----------
export async function trackEvent(type, meta = null, path = null) {
  try {
    await http.post("/analytics/event", { type, meta, path });
  } catch (_) {}
}

// ---------- Auth (admin) ----------
export async function login(email, password) {
  const { data } = await http.post("/auth/login", { email, password });
  setToken(data.access_token);
  return data;
}

export async function me() {
  const { data } = await http.get("/auth/me");
  return data;
}

export function logout() {
  setToken(null);
}

// ---------- helpers ----------
function normalizeProject(p, i) {
  // Convert backend project shape to what ProjectCard expects
  return {
    id: p.id || String(i + 1).padStart(2, "0"),
    displayId: String(i + 1).padStart(2, "0"),
    title: p.title,
    description: p.description,
    tags: p.tags || [],
    gradient: p.gradient || "linear-gradient(135deg, #7b2fff 0%, #00f5ff 100%)",
    live: p.live_url || "#",
    github: p.github_url || "#",
    image_url: p.image_url || null,
  };
}
