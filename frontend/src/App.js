import React from "react";
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
import { Toaster } from "./components/ui/toaster";

function App() {
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
      <Toaster />
    </div>
  );
}

export default App;
