import axios from "axios";
import { personal, bio, stats, socials, skills as mockSkills, projects as mockProjects } from "../data/mock";

const BASE_URL = process.env.REACT_APP_BACKEND_URL;
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

// ---------- Public API ----------
export async function fetchAbout() {
  try {
    const { data } = await http.get("/about");
    return data;
  } catch (e) {
    return {
      name: personal.name,
      role: personal.role,
      tagline: personal.tagline,
      bio,
      location: personal.location,
      email: personal.email,
      available: personal.available,
      stats,
      socials,
    };
  }
}

export async function fetchProjects() {
  try {
    const { data } = await http.get("/projects");
    if (Array.isArray(data) && data.length) return data.map(normalizeProject);
    return mockProjects;
  } catch (e) {
    return mockProjects;
  }
}

export async function fetchSkills() {
  try {
    const { data } = await http.get("/skills");
    if (Array.isArray(data) && data.length) return data;
    return mockSkills;
  } catch (e) {
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
