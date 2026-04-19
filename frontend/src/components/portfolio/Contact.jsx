import React, { useEffect, useState } from "react";
import { Copy, Check, Github, Linkedin, Twitter, Mail, Send, Loader2 } from "lucide-react";
import useReveal from "../../hooks/useReveal";
import { useToast } from "../../hooks/use-toast";
import { fetchAbout, submitContact, trackEvent } from "../../lib/api";

export default function Contact() {
  const [ref, visible] = useReveal();
  const [copied, setCopied] = useState(false);
  const [about, setAbout] = useState(null);
  const [form, setForm] = useState({ name: "", email: "", subject: "", body: "" });
  const [sending, setSending] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    fetchAbout().then(setAbout);
  }, []);

  const email = about?.email || "hello@alexvantage.dev";
  const socials = about?.socials || {};

  const copyEmail = async () => {
    try {
      await navigator.clipboard.writeText(email);
      setCopied(true);
      toast({ title: "Email copied", description: email });
      setTimeout(() => setCopied(false), 1800);
    } catch (_) {
      toast({ title: "Copy failed", description: "Select and copy manually." });
    }
  };

  const update = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  const submit = async (e) => {
    e.preventDefault();
    if (sending) return;
    if (!form.name.trim() || !form.email.trim() || !form.body.trim()) {
      toast({ title: "Please fill name, email and message." });
      return;
    }
    setSending(true);
    try {
      await submitContact(form);
      trackEvent("contact_submit");
      toast({ title: "Message sent", description: "I'll get back to you shortly." });
      setForm({ name: "", email: "", subject: "", body: "" });
    } catch (err) {
      const detail = err?.response?.data?.detail || "Couldn't send — please try again.";
      toast({ title: "Send failed", description: String(detail) });
    } finally {
      setSending(false);
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
          <span>{email}</span>
          <span className="contact__email-copy">
            {copied ? <Check size={16} /> : <Copy size={16} />}
          </span>
        </button>

        <form className="contact__form" onSubmit={submit}>
          <div className="contact__form-row">
            <input
              className="contact__input"
              placeholder="Your name"
              value={form.name}
              onChange={update("name")}
              maxLength={120}
              required
            />
            <input
              className="contact__input"
              placeholder="Your email"
              type="email"
              value={form.email}
              onChange={update("email")}
              required
            />
          </div>
          <input
            className="contact__input"
            placeholder="Subject (optional)"
            value={form.subject}
            onChange={update("subject")}
            maxLength={200}
          />
          <textarea
            className="contact__input contact__textarea"
            placeholder="Tell me about the project…"
            value={form.body}
            onChange={update("body")}
            rows={5}
            maxLength={5000}
            required
          />
          <button type="submit" className="btn btn--primary contact__submit" disabled={sending}>
            {sending ? <Loader2 size={14} className="chat-spin" /> : <Send size={14} />}
            <span>{sending ? "Sending…" : "Send Message"}</span>
          </button>
        </form>

        <div className="contact__socials">
          {socials.github && (
            <a href={socials.github} target="_blank" rel="noreferrer" className="contact__social" aria-label="GitHub"><Github size={18} /></a>
          )}
          {socials.linkedin && (
            <a href={socials.linkedin} target="_blank" rel="noreferrer" className="contact__social" aria-label="LinkedIn"><Linkedin size={18} /></a>
          )}
          {socials.twitter && (
            <a href={socials.twitter} target="_blank" rel="noreferrer" className="contact__social" aria-label="Twitter"><Twitter size={18} /></a>
          )}
        </div>
      </div>
    </section>
  );
}
