/**
 * SEO Configuration Module
 *
 * Central configuration for all SEO-related constants used across the portfolio site.
 * Includes meta tag values, Open Graph data, Twitter Card settings,
 * and JSON-LD structured data for Person and WebSite schemas.
 */

const SEO_CONFIG = {
  title: "Sujal Meena — Full-Stack AI Engineer",
  description:
    "Full-Stack AI Engineer specializing in agentic workflows, RAG pipelines, and high-performance web applications. View projects, skills, and get in touch.",
  canonicalUrl: "https://sujalmeena.xyz",
  ogImage: "https://sujalmeena.xyz/og-image.png",
  ogType: "website",
  twitterCard: "summary_large_image",
  person: {
    name: "Sujal Meena",
    jobTitle: "Full-Stack AI Engineer",
    url: "https://sujalmeena.xyz",
    sameAs: [
      "https://github.com/sujalmeena7",
      "https://www.linkedin.com/in/sujal-meena-170418371",
    ],
  },
  website: {
    name: "Sujal Meena Portfolio",
    url: "https://sujalmeena.xyz",
    description:
      "Portfolio of Sujal Meena, a Full-Stack AI Engineer building intelligent agentic workflows and high-performance digital systems.",
  },
};

export default SEO_CONFIG;
