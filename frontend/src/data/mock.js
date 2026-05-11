// Mock data for portfolio - replace with real content later

export const personal = {
  name: "Sujal Meena",
  role: "Full-Stack AI Engineer",
  tagline: "Crafting intelligent agentic workflows and high-performance digital systems.",
  email: "meenasujal60@gmail.com",
  location: "Chandigarh, India",
  available: true,
  resume: "/Sujal_Meena_Resume_Final.pdf",
};

export const socials = {
  github: "https://github.com/sujalmeena7",
  linkedin: "https://www.linkedin.com/in/sujal-meena-170418371",
};

export const stats = [
  { label: "Projects", value: "9", suffix: "+" },
  { label: "Hackathons", value: "10", suffix: "+" },
  { label: "Technologies", value: "15", suffix: "+" },
];

export const bio = [
  "I am a Computer Science student at PEC Chandigarh and a software developer specializing in AI-driven architectures. I focus on building autonomous agentic workflows and sophisticated RAG pipelines, bridging the gap between raw data and intelligent automation.",
  "My approach combines technical rigor—using stacks like Python, FastAPI, and Next.js—with a commitment to minimalist, high-end design. Whether it's legal tech compliance or performance-heavy hackathon builds, I prioritize clean code and premium user experiences.",
];

export const skills = [
  { name: "Python / FastAPI", level: 95, icon: "Terminal" },
  { name: "AI Agents / RAG", level: 92, icon: "Cpu" },
  { name: "Next.js / React", level: 85, icon: "Globe" },
  { name: "Vector DBs", level: 80, icon: "Database" },
];

export const projects = [
  {
    id: "01",
    title: "LexGuard AI",
    description: "AI-powered compliance auditor that analyzes legal documents against India's DPDP Act 2023 using tiered RAG + LLM inference. Transforms privacy policies and terms of service into actionable risk assessments with clause-level flagging and remediation suggestions.",
    tags: ["Python", "FastAPI", "Next.js", "RAG", "Gemini"],
    gradient: "linear-gradient(135deg, #7b2fff 0%, #00f5ff 100%)",
    live: "https://lexguard-ai-three.vercel.app/",
    github: "https://github.com/sujalmeena7/lexguard-ai",
  },
  {
    id: "02",
    title: "Sentinel-SRE",
    description: "AI-powered root cause analysis platform that ingests Prometheus alerts via webhook, uses RAG (LlamaIndex + Groq) to diagnose incidents, and generates actionable postmortems. Includes chaos simulation, real-time telemetry, and automated incident triage.",
    tags: ["Python", "FastAPI", "Next.js", "LlamaIndex", "Prometheus", "Docker"],
    gradient: "linear-gradient(135deg, #0ea5e9 0%, #7b2fff 100%)",
    live: "https://sentinel-sre-zeta.vercel.app",
    github: "https://github.com/sujalmeena7/sentinel-sre",
  },
  {
    id: "03",
    title: "ConnectAI",
    description: "Hyper-personalized LinkedIn outreach generator as a Chrome extension. Automates profile scraping and crafts high-conversion DMs using Claude 3.5. Features AI-powered shortening, inline message editing, and persistent bookmarking.",
    tags: ["JavaScript", "Claude 3.5", "Chrome Extension", "Manifest V3"],
    gradient: "linear-gradient(135deg, #0A66C2 0%, #0077b5 100%)",
    live: "https://chromewebstore.google.com/detail/cjfnhjpheldgcfmipcmibbmlfmpflfij?utm_source=item-share-cb",
    github: "https://github.com/sujalmeena7/Connect-AI",
  },
  {
    id: "04",
    title: "Tab Hibernator Pro",
    description: "High-performance, privacy-first Chrome extension that intelligently suspends inactive tabs to reclaim system memory. Built on Manifest V3 with a smart exclusion engine that detects audio, video, and active form inputs to ensure zero data loss while keeping the browser blazing fast.",
    tags: ["JavaScript", "Chrome Extension", "Manifest V3", "Performance"],
    gradient: "linear-gradient(135deg, #4f46e5 0%, #818cf8 100%)",
    live: "https://github.com/sujalmeena7/Tab-Hibernator-Pro",
    github: "https://github.com/sujalmeena7/Tab-Hibernator-Pro",
  },
];

export const navLinks = [
  { label: "Home", href: "#home" },
  { label: "About", href: "#about" },
  { label: "Skills", href: "#skills" },
  { label: "Work", href: "#projects" },
  { label: "Contact", href: "#contact" },
];

export const about = {
  ...personal,
  socials,
  stats,
  bio,
  resume_url: personal.resume,
};
