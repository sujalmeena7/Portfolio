import React, { useEffect } from "react";
import "./App.css";
import CustomCursor from "./components/portfolio/CustomCursor";
import FloatingParticles from "./components/portfolio/FloatingParticles";
import Navbar from "./components/portfolio/Navbar";
import Hero from "./components/portfolio/Hero";
import About from "./components/portfolio/About";
import Skills from "./components/portfolio/Skills";
import Projects from "./components/portfolio/Projects";
import Contact from "./components/portfolio/Contact";
import Footer from "./components/portfolio/Footer";
import ChatWidget from "./components/portfolio/ChatWidget";
import { Toaster } from "./components/ui/toaster";
import { trackEvent } from "./lib/api";

function App() {
  useEffect(() => {
    trackEvent("page_view", null, window.location.pathname);
  }, []);

  return (
    <div className="app">
      <div className="grain" aria-hidden="true" />
      <FloatingParticles count={50} />
      <CustomCursor />
      <Navbar />
      <main>
        <Hero />
        <About />
        <Skills />
        <Projects />
        <Contact />
      </main>
      <Footer />
      <ChatWidget />
      <Toaster />
    </div>
  );
}

export default App;
