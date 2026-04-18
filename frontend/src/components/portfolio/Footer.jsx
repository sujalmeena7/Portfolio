import React from "react";
import { personal } from "../../data/mock";

export default function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="footer">
      <div className="footer__inner">
        <span className="footer__left">© {year} {personal.name} · Crafted with Three.js &amp; care</span>
        <span className="footer__right">v1.0 · {personal.location}</span>
      </div>
    </footer>
  );
}
