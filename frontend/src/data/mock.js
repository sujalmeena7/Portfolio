// Mock data for portfolio - replace with real content later

export const personal = {
  name: "ALEX VANTAGE",
  role: "Creative Developer",
  tagline: "Crafting immersive digital experiences at the intersection of code, design, and motion.",
  email: "hello@alexvantage.dev",
  location: "Berlin, DE",
  available: true,
};

export const socials = {
  github: "https://github.com",
  linkedin: "https://linkedin.com",
  twitter: "https://twitter.com",
};

export const stats = [
  { label: "Projects", value: "72", suffix: "+" },
  { label: "Years Exp.", value: "08", suffix: "" },
  { label: "Clients", value: "40", suffix: "+" },
];

export const bio = [
  "I'm a creative developer with 8+ years building production-grade web experiences. I specialise in WebGL, interactive 3D, and performance-obsessed frontends that feel alive.",
  "Previously at agencies and in-house teams across Europe, now freelancing on cinematic brand sites, product interfaces, and creative coding experiments.",
];

export const skills = [
  { name: "JavaScript", level: 95, icon: "Braces" },
  { name: "React", level: 92, icon: "Atom" },
  { name: "Node.js", level: 85, icon: "Server" },
  { name: "Three.js", level: 88, icon: "Box" },
  { name: "Python", level: 78, icon: "Terminal" },
  { name: "Docker", level: 72, icon: "Container" },
  { name: "AWS", level: 70, icon: "Cloud" },
  { name: "Figma", level: 82, icon: "Figma" },
];

export const projects = [
  {
    id: "01",
    title: "Nebula Commerce",
    description: "A WebGL-powered storefront for a luxury audio brand. Product configurator with real-time material shaders and a physics-based cart interaction.",
    tags: ["Three.js", "React", "GSAP", "Shopify"],
    gradient: "linear-gradient(135deg, #7b2fff 0%, #00f5ff 100%)",
    live: "#",
    github: "#",
  },
  {
    id: "02",
    title: "Cartograph OS",
    description: "Internal tool for a satellite imagery company. Real-time map rendering, terabyte-scale tile streaming, and collaborative annotation layers.",
    tags: ["WebGL", "TypeScript", "WebSockets", "Rust"],
    gradient: "linear-gradient(135deg, #0ea5e9 0%, #7b2fff 100%)",
    live: "#",
    github: "#",
  },
  {
    id: "03",
    title: "Signal Garden",
    description: "Generative art platform that turns live audio input into evolving 3D landscapes. Shipped as an installation and a web toy.",
    tags: ["Three.js", "Web Audio", "GLSL", "Canvas"],
    gradient: "linear-gradient(135deg, #ec4899 0%, #7b2fff 60%, #00f5ff 100%)",
    live: "#",
    github: "#",
  },
];

export const navLinks = [
  { label: "Home", href: "#home" },
  { label: "About", href: "#about" },
  { label: "Skills", href: "#skills" },
  { label: "Work", href: "#projects" },
  { label: "Contact", href: "#contact" },
];
