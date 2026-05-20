import React, { useEffect, Suspense } from "react";
import "./App.css";
import CustomCursor from "./components/portfolio/CustomCursor";
import Navbar from "./components/portfolio/Navbar";
import Hero from "./components/portfolio/Hero";
import About from "./components/portfolio/About";
import Skills from "./components/portfolio/Skills";
import Projects from "./components/portfolio/Projects";
import Contact from "./components/portfolio/Contact";
import Footer from "./components/portfolio/Footer";
import { Toaster } from "./components/ui/toaster";
import { trackEvent } from "./lib/api";

const FloatingParticles = React.lazy(() => import('./components/portfolio/FloatingParticles'));
const ChatWidget = React.lazy(() => import('./components/portfolio/ChatWidget'));

function App() {
  useEffect(() => {
    trackEvent("page_view", null, window.location.pathname);
  }, []);

  return (
    <div className="app">
      <div className="grain" aria-hidden="true" />
      <Suspense fallback={null}>
        <FloatingParticles count={50} />
      </Suspense>
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
      <Suspense fallback={null}>
        <ChatWidget />
      </Suspense>
      <Toaster />
    </div>
  );
}

export default App;
