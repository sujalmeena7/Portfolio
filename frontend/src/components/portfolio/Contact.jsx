import React, { useState } from "react";
import { Copy, Check, Github, Linkedin, Twitter, Mail } from "lucide-react";
import useReveal from "../../hooks/useReveal";
import { personal, socials } from "../../data/mock";
import { useToast } from "../../hooks/use-toast";

export default function Contact() {
  const [ref, visible] = useReveal();
  const [copied, setCopied] = useState(false);
  const { toast } = useToast();

  const copyEmail = async () => {
    try {
      await navigator.clipboard.writeText(personal.email);
      setCopied(true);
      toast({ title: "Email copied", description: personal.email });
      setTimeout(() => setCopied(false), 1800);
    } catch (_) {
      toast({ title: "Copy failed", description: "Select and copy manually." });
    }
  };

  return (
    <section id="contact" className="section contact" ref={ref}>
      <div className="contact__mesh" aria-hidden="true" />
      <div className="section__index">04</div>
      <div className="section__heading section__heading--center">
        <span className={`section__heading-inner ${visible ? "reveal-in" : ""}`}>LET'S BUILD</span>
      </div>

      <div className={`contact__inner ${visible ? "fade-up-in" : "fade-up"}`}>
        <h2 className="contact__headline">
          Have a project <span className="contact__headline-accent">in orbit?</span>
          <br />Let's make it land.
        </h2>
        <p className="contact__sub">
          Open to freelance collaborations, creative coding commissions, and full-time creative developer roles.
        </p>

        <button className="contact__email" onClick={copyEmail} aria-label="Copy email">
          <Mail size={18} />
          <span>{personal.email}</span>
          <span className="contact__email-copy">
            {copied ? <Check size={16} /> : <Copy size={16} />}
          </span>
        </button>

        <div className="contact__socials">
          <a href={socials.github} target="_blank" rel="noreferrer" className="contact__social" aria-label="GitHub"><Github size={18} /></a>
          <a href={socials.linkedin} target="_blank" rel="noreferrer" className="contact__social" aria-label="LinkedIn"><Linkedin size={18} /></a>
          <a href={socials.twitter} target="_blank" rel="noreferrer" className="contact__social" aria-label="Twitter"><Twitter size={18} /></a>
        </div>
      </div>
    </section>
  );
}
