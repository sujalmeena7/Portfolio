import React, { useEffect, useRef } from "react";
import {
  Braces, Atom, Server, Box, Terminal, Container, Cloud, Figma,
} from "lucide-react";
import useReveal from "../../hooks/useReveal";
import { skills } from "../../data/mock";

const ICONS = { Braces, Atom, Server, Box, Terminal, Container, Cloud, Figma };

function TiltCard({ skill, index, inView }) {
  const ref = useRef(null);
  const Icon = ICONS[skill.icon] || Box;

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const onMove = (e) => {
      const r = el.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width;
      const py = (e.clientY - r.top) / r.height;
      const rx = (py - 0.5) * -14;
      const ry = (px - 0.5) * 16;
      el.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg) translateZ(0)`;
      el.style.setProperty("--mx", `${px * 100}%`);
      el.style.setProperty("--my", `${py * 100}%`);
    };
    const onLeave = () => {
      el.style.transform = "perspective(900px) rotateX(0) rotateY(0)";
    };
    el.addEventListener("mousemove", onMove);
    el.addEventListener("mouseleave", onLeave);
    return () => {
      el.removeEventListener("mousemove", onMove);
      el.removeEventListener("mouseleave", onLeave);
    };
  }, []);

  return (
    <div
      ref={ref}
      className="tilt-card"
      style={{ transitionDelay: `${index * 60}ms` }}
    >
      <div className="tilt-card__shine" aria-hidden="true" />
      <div className="tilt-card__top">
        <div className="tilt-card__icon"><Icon size={22} strokeWidth={1.6} /></div>
        <span className="tilt-card__num">{String(index + 1).padStart(2, "0")}</span>
      </div>
      <div className="tilt-card__name">{skill.name}</div>
      <div className="tilt-card__bar">
        <div
          className="tilt-card__bar-fill"
          style={{ width: inView ? `${skill.level}%` : "0%" }}
        />
      </div>
      <div className="tilt-card__level">{skill.level}%</div>
    </div>
  );
}

export default function Skills() {
  const [ref, visible] = useReveal();
  return (
    <section id="skills" className="section skills" ref={ref}>
      <div className="section__index">02</div>
      <div className="section__heading">
        <span className={`section__heading-inner ${visible ? "reveal-in" : ""}`}>SKILLS</span>
      </div>
      <p className="section__lede">
        Tools and technologies I reach for when turning ambitious ideas into shippable, fast, and memorable products.
      </p>

      <div className="skills__grid">
        {skills.map((s, i) => (
          <TiltCard key={s.name} skill={s} index={i} inView={visible} />
        ))}
      </div>
    </section>
  );
}
