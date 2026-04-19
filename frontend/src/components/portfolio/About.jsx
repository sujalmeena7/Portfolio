import React, { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import useReveal from "../../hooks/useReveal";
import { fetchAbout } from "../../lib/api";

export default function About() {
  const meshCanvasRef = useRef(null);
  const [revealRef, visible] = useReveal();
  const [about, setAbout] = useState(null);

  useEffect(() => {
    fetchAbout()
      .then(setAbout)
      .catch((error) => console.error("[about] Failed to load about data", error));
  }, []);

  useEffect(() => {
    const canvas = meshCanvasRef.current;
    if (!canvas) return;
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 100);
    camera.position.z = 4;

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(w, h, false);

    const geometry = new THREE.TorusKnotGeometry(1, 0.32, 160, 24);
    const material = new THREE.MeshStandardMaterial({
      color: "#00f5ff",
      emissive: "#7b2fff",
      emissiveIntensity: 0.35,
      wireframe: true,
      metalness: 0.5,
      roughness: 0.3,
    });
    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    const amb = new THREE.AmbientLight("#ffffff", 0.4);
    const p1 = new THREE.PointLight("#00f5ff", 2, 10);
    p1.position.set(3, 2, 3);
    const p2 = new THREE.PointLight("#7b2fff", 2, 10);
    p2.position.set(-3, -2, 2);
    scene.add(amb, p1, p2);

    const onResize = () => {
      const nw = canvas.clientWidth;
      const nh = canvas.clientHeight;
      camera.aspect = nw / nh;
      camera.updateProjectionMatrix();
      renderer.setSize(nw, nh, false);
    };
    window.addEventListener("resize", onResize);

    let raf;
    const clock = new THREE.Clock();
    const loop = () => {
      const t = clock.getElapsedTime();
      mesh.rotation.x = t * 0.25;
      mesh.rotation.y = t * 0.18;
      renderer.render(scene, camera);
      raf = requestAnimationFrame(loop);
    };
    loop();

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", onResize);
      geometry.dispose();
      material.dispose();
      renderer.dispose();
    };
  }, []);

  const bioLines = about?.bio || [];
  const statsList = about?.stats || [];

  return (
    <section id="about" className="section about" ref={revealRef}>
      <div className="section__index">01</div>
      <div className="section__heading">
        <span className={`section__heading-inner ${visible ? "reveal-in" : ""}`}>ABOUT</span>
      </div>

      <div className="about__grid">
        <div className="about__mesh">
          <canvas ref={meshCanvasRef} className="about__mesh-canvas" />
          <div className="about__mesh-glow" aria-hidden="true" />
        </div>

        <div className={`about__content ${visible ? "fade-up-in" : "fade-up"}`}>
          {about?.available && (
            <div className="about__badge">
              <span className="about__badge-dot" />
              <span>Currently available for work</span>
            </div>
          )}

          {bioLines.map((p, i) => (
            <p key={i} className="about__p">{p}</p>
          ))}

          <div className="about__stats">
            {statsList.map((s) => (
              <div key={s.label} className="stat-card">
                <div className="stat-card__value">
                  {s.value}<span className="stat-card__suffix">{s.suffix}</span>
                </div>
                <div className="stat-card__label">{s.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
