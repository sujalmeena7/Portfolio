import React, { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { ArrowDown, Download, Play } from "lucide-react";
import { personal } from "../../data/mock";

// Hero: 3D particle galaxy + glitch/scramble typography + magnetic CTAs.
export default function Hero() {
  const canvasRef = useRef(null);
  const heroRef = useRef(null);
  const [title1, setTitle1] = useState("I BUILD");
  const [title2, setTitle2] = useState("DIGITAL WORLDS");

  // Three.js particle galaxy
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);

    const PARTICLES = 6000;
    const positions = new Float32Array(PARTICLES * 3);
    const colors = new Float32Array(PARTICLES * 3);
    const cyan = new THREE.Color("#00f5ff");
    const violet = new THREE.Color("#7b2fff");

    for (let i = 0; i < PARTICLES; i++) {
      const arm = Math.floor(Math.random() * 3);
      const angle = (arm / 3) * Math.PI * 2 + Math.random() * 1.2;
      const radius = Math.pow(Math.random(), 0.7) * 4;
      const spin = radius * 0.9;
      const x = Math.cos(angle + spin) * radius + (Math.random() - 0.5) * 0.4;
      const y = (Math.random() - 0.5) * 0.6 * (1 - radius / 5);
      const z = Math.sin(angle + spin) * radius + (Math.random() - 0.5) * 0.4;
      positions.set([x, y, z], i * 3);
      const mix = Math.random();
      const c = cyan.clone().lerp(violet, mix);
      colors.set([c.r, c.g, c.b], i * 3);
    }

    const geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    geo.setAttribute("color", new THREE.BufferAttribute(colors, 3));

    const mat = new THREE.PointsMaterial({
      size: 0.022,
      vertexColors: true,
      transparent: true,
      opacity: 0.9,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const points = new THREE.Points(geo, mat);
    scene.add(points);

    // subtle core glow sphere
    const core = new THREE.Mesh(
      new THREE.SphereGeometry(0.18, 32, 32),
      new THREE.MeshBasicMaterial({ color: "#00f5ff", transparent: true, opacity: 0.35 })
    );
    scene.add(core);

    const mouse = { x: 0, y: 0, tx: 0, ty: 0 };
    const onMove = (e) => {
      mouse.tx = (e.clientX / window.innerWidth - 0.5) * 2;
      mouse.ty = (e.clientY / window.innerHeight - 0.5) * 2;
    };
    window.addEventListener("mousemove", onMove);

    const onResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };
    window.addEventListener("resize", onResize);

    let raf;
    const clock = new THREE.Clock();
    const animate = () => {
      const t = clock.getElapsedTime();
      mouse.x += (mouse.tx - mouse.x) * 0.05;
      mouse.y += (mouse.ty - mouse.y) * 0.05;
      points.rotation.y = t * 0.08 + mouse.x * 0.4;
      points.rotation.x = Math.sin(t * 0.1) * 0.1 + mouse.y * 0.25;
      core.scale.setScalar(1 + Math.sin(t * 2) * 0.08);
      renderer.render(scene, camera);
      raf = requestAnimationFrame(animate);
    };
    animate();

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("resize", onResize);
      geo.dispose();
      mat.dispose();
      renderer.dispose();
    };
  }, []);

  // Scramble text effect on mount
  useEffect(() => {
    const CHARS = "!<>-_\\/[]{}—=+*^?#_∙·◦ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    const scramble = (finalText, setter, duration = 1200) => {
      const start = performance.now();
      const tick = (now) => {
        const p = Math.min(1, (now - start) / duration);
        const reveal = Math.floor(p * finalText.length);
        let out = "";
        for (let i = 0; i < finalText.length; i++) {
          if (i < reveal || finalText[i] === " ") out += finalText[i];
          else out += CHARS[Math.floor(Math.random() * CHARS.length)];
        }
        setter(out);
        if (p < 1) requestAnimationFrame(tick);
        else setter(finalText);
      };
      requestAnimationFrame(tick);
    };
    scramble("I BUILD", setTitle1, 900);
    setTimeout(() => scramble("DIGITAL WORLDS", setTitle2, 1400), 350);
  }, []);

  // Magnetic CTA effect
  useEffect(() => {
    const btns = heroRef.current?.querySelectorAll(".magnetic");
    if (!btns) return;
    const handlers = [];
    btns.forEach((btn) => {
      const onMove = (e) => {
        const r = btn.getBoundingClientRect();
        const dx = e.clientX - (r.left + r.width / 2);
        const dy = e.clientY - (r.top + r.height / 2);
        btn.style.transform = `translate(${dx * 0.18}px, ${dy * 0.25}px)`;
      };
      const onLeave = () => { btn.style.transform = "translate(0,0)"; };
      btn.addEventListener("mousemove", onMove);
      btn.addEventListener("mouseleave", onLeave);
      handlers.push({ btn, onMove, onLeave });
    });
    return () => handlers.forEach(({ btn, onMove, onLeave }) => {
      btn.removeEventListener("mousemove", onMove);
      btn.removeEventListener("mouseleave", onLeave);
    });
  }, []);

  return (
    <section id="home" className="hero" ref={heroRef}>
      <canvas ref={canvasRef} className="hero__canvas" />
      <div className="hero__vignette" aria-hidden="true" />

      <div className="hero__content">
        <div className="hero__eyebrow">
          <span className="hero__eyebrow-line" />
          <span>{personal.role.toUpperCase()} · {personal.location.toUpperCase()}</span>
        </div>

        <h1 className="hero__title">
          <span className="hero__title-row hero__title-row--thin">{title1}</span>
          <span className="hero__title-row hero__title-row--bold">{title2}</span>
        </h1>

        <p className="hero__subtitle">{personal.tagline}</p>

        <div className="hero__ctas">
          <a
            href="#projects"
            onClick={(e) => {
              e.preventDefault();
              document.querySelector("#projects")?.scrollIntoView({ behavior: "smooth" });
            }}
            className="btn btn--primary magnetic"
          >
            <Play size={16} />
            <span>View Work</span>
          </a>
          <a href="#" onClick={(e) => e.preventDefault()} className="btn btn--ghost magnetic">
            <Download size={16} />
            <span>Download CV</span>
          </a>
        </div>
      </div>

      <a
        href="#about"
        onClick={(e) => {
          e.preventDefault();
          document.querySelector("#about")?.scrollIntoView({ behavior: "smooth" });
        }}
        className="hero__scroll"
        aria-label="Scroll to about"
      >
        <span>SCROLL</span>
        <ArrowDown size={14} className="hero__scroll-icon" />
      </a>
    </section>
  );
}
