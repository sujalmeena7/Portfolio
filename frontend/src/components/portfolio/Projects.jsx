import React, { useEffect, useState } from "react";
import { ExternalLink, Github, ArrowUpRight } from "lucide-react";
import useReveal from "../../hooks/useReveal";
import { fetchProjects } from "../../lib/api";

function ProjectCard({ project, index }) {
  const [ref, visible] = useReveal();
  const displayId = project.displayId || String(index + 1).padStart(2, "0");
  const hasLive = project.live && project.live !== "#";
  const hasGithub = project.github && project.github !== "#";

  return (
    <article
      ref={ref}
      className={`project-card ${visible ? "fade-up-in" : "fade-up"}`}
      style={{ transitionDelay: `${index * 90}ms` }}
    >
      <div className="project-card__media" style={{ background: project.gradient }}>
        {project.image_url && (
          <img src={project.image_url} alt={project.title} className="project-card__img" />
        )}
        <div className="project-card__media-grid" aria-hidden="true" />
        <div className="project-card__media-id">{displayId}</div>
        <div className="project-card__media-label">
          <span>CASE STUDY</span>
          <ArrowUpRight size={18} />
        </div>
      </div>

      <div className="project-card__body">
        <div className="project-card__tags">
          {(project.tags || []).map((t) => (
            <span key={t} className="project-card__tag">{t}</span>
          ))}
        </div>
        <h3 className="project-card__title">{project.title}</h3>
        <p className="project-card__desc">{project.description}</p>

        <div className="project-card__actions">
          <a
            href={project.live || "#"}
            target={hasLive ? "_blank" : undefined}
            rel="noreferrer"
            onClick={(e) => { if (!hasLive) e.preventDefault(); }}
            className="btn btn--primary btn--sm"
          >
            <ExternalLink size={14} /> View Live
          </a>
          <a
            href={project.github || "#"}
            target={hasGithub ? "_blank" : undefined}
            rel="noreferrer"
            onClick={(e) => { if (!hasGithub) e.preventDefault(); }}
            className="btn btn--ghost btn--sm"
          >
            <Github size={14} /> GitHub
          </a>
        </div>
      </div>
    </article>
  );
}

export default function Projects() {
  const [ref, visible] = useReveal();
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    fetchProjects()
      .then(setProjects)
      .catch((error) => console.error("[projects] Failed to load projects", error));
  }, []);

  return (
    <section id="projects" className="section projects" ref={ref}>
      <div className="section__index">03</div>
      <div className="section__heading">
        <span className={`section__heading-inner ${visible ? "reveal-in" : ""}`}>SELECTED WORK</span>
      </div>
      <p className="section__lede">
        A small set of recent builds spanning commerce, tooling, and creative coding. Each shipped, each measurable.
      </p>

      <div className="projects__grid">
        {projects.map((p, i) => (
          <ProjectCard key={p.id || i} project={p} index={i} />
        ))}
      </div>
    </section>
  );
}
