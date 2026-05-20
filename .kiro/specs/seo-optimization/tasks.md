# Implementation Plan: SEO Optimization

## Overview

Comprehensive SEO optimization for the portfolio website (React SPA with CRA+CRACO and FastAPI backend on EC2). Implementation covers meta tags, structured data, sitemap/robots.txt generation, semantic HTML restructuring, image optimization, Core Web Vitals performance, pre-rendering for crawlers, mobile-friendliness, and URL/link optimization. The approach uses build-time pre-rendering (react-snap) to serve static HTML to crawlers while keeping the existing SPA architecture intact.

## Tasks

- [x] 1. Set up SEO configuration and meta tags
  - [x] 1.1 Create SEO configuration module
    - Create `frontend/src/config/seo.js` with all SEO constants (title, description, canonical URL, OG image URL, person schema data, website schema data)
    - Export `SEO_CONFIG` object matching the data model in the design document
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2_

  - [x] 1.2 Update index.html with comprehensive meta tags
    - Add Open Graph tags (og:title, og:description, og:image, og:url, og:type)
    - Add Twitter Card tags (twitter:card, twitter:title, twitter:description, twitter:image)
    - Add canonical URL link element
    - Verify title is 30-60 characters, description is 150-160 characters
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

  - [x] 1.3 Add JSON-LD structured data to index.html
    - Add Person schema JSON-LD script with name, jobTitle, url, sameAs properties
    - Add WebSite schema JSON-LD script with name, url, description (max 160 chars)
    - Place in `<head>` so it's available without JavaScript execution
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [x] 1.4 Create OG image asset
    - Create or place `og-image.png` (minimum 1200x630 pixels) in `frontend/public/`
    - Ensure file size is under 500 KB
    - _Requirements: 1.3, 1.6, 6.6_

- [x] 2. Implement sitemap and robots.txt generation
  - [x] 2.1 Create sitemap generator script
    - Create `frontend/scripts/generate-sitemap.js` Node.js script
    - Generate XML conforming to Sitemaps.org protocol 0.9 schema
    - Include homepage URL with lastmod (build date in YYYY-MM-DD), changefreq "monthly", priority "1.0"
    - Output to `frontend/build/sitemap.xml`
    - Exit with non-zero code and error message on failure
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [x] 2.2 Create robots.txt generator script
    - Create `frontend/scripts/generate-robots.js` Node.js script
    - Include `User-agent: *`, `Allow: /`, `Disallow: /api/`
    - Include `Sitemap: https://sujalmeena.dev/sitemap.xml` directive
    - Output to `frontend/build/robots.txt`
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 2.3 Integrate generators into build pipeline
    - Add `postbuild` script to `package.json` that runs sitemap and robots.txt generators
    - Ensure build fails if sitemap generation fails
    - _Requirements: 3.4, 3.5, 4.4_

  - [ ]* 2.4 Write property test for sitemap XML schema conformance
    - **Property 2: Sitemap XML Schema Conformance**
    - **Validates: Requirements 3.1**
    - Install `fast-check` as dev dependency
    - Test that for any valid URL and date, the generator produces valid XML with correct structure

- [x] 3. Checkpoint - Verify meta tags and build scripts
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Implement semantic HTML and heading hierarchy
  - [x] 4.1 Restructure App.js with semantic landmarks
    - Wrap Navbar in `<header>` element with appropriate aria-label
    - Ensure `<main>` wraps primary content sections
    - Verify `<footer>` element is used for Footer component
    - Add aria-label to header landmark
    - _Requirements: 5.4, 5.5_

  - [x] 4.2 Update Hero.jsx with proper h1 and section semantics
    - Ensure exactly one `<h1>` element exists containing the primary headline
    - Wrap in `<section>` with id="home" and aria-labelledby referencing the h1's id
    - _Requirements: 5.1, 5.4, 5.6_

  - [x] 4.3 Update About.jsx with h2 and section semantics
    - Change section heading to `<h2>` element
    - Add id to the heading, add aria-labelledby to the section
    - Ensure any sub-headings use h3 (no skipped levels)
    - _Requirements: 5.2, 5.3, 5.6_

  - [x] 4.4 Update Skills.jsx with h2 and section semantics
    - Change section heading to `<h2>` element
    - Add id to the heading, add aria-labelledby to the section
    - _Requirements: 5.2, 5.3, 5.6_

  - [x] 4.5 Update Projects.jsx with h2, article elements, and section semantics
    - Change section heading to `<h2>` element
    - Add id to the heading, add aria-labelledby to the section
    - Ensure individual project cards use `<article>` elements
    - Use h3 for project titles within articles
    - _Requirements: 5.2, 5.3, 5.4, 5.6_

  - [x] 4.6 Update Contact.jsx with h2 and section semantics
    - Change section heading to `<h2>` element
    - Add id to the heading, add aria-labelledby to the section
    - _Requirements: 5.2, 5.3, 5.6_

  - [x] 4.7 Add aria-label to Navbar nav element
    - Verify nav element has aria-label="Primary navigation" or similar descriptive label (2-50 chars)
    - _Requirements: 5.5_

  - [ ]* 4.8 Write property test for heading hierarchy validation
    - **Property 3: Heading Hierarchy Sequential Ordering**
    - **Validates: Requirements 5.3**
    - Create a heading hierarchy validator function and test with fast-check that no heading levels are skipped

- [x] 5. Implement image optimization and alt text
  - [x] 5.1 Create alt text formatter utility
    - Create `frontend/src/utils/seo-helpers.js` with `formatProjectAltText(projectName, description)` function
    - Return format: "[Project Name] - [description]" truncated to 125 chars
    - Ensure minimum 5 characters output
    - _Requirements: 6.1, 6.3_

  - [x] 5.2 Create image error handler utility
    - Add `handleImageError(event, projectName)` to `frontend/src/utils/seo-helpers.js`
    - Set fallback text showing project name, maintain reserved image space via CSS aspect-ratio
    - _Requirements: 6.5_

  - [x] 5.3 Update Projects.jsx with proper alt text and error handling
    - Apply `formatProjectAltText` to all project images
    - Add `onError` handler using `handleImageError`
    - Add explicit width/height or aspect-ratio CSS to prevent CLS
    - Set decorative images to alt=""
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [ ]* 5.4 Write property test for alt text format and length
    - **Property 4: Alt Text Format and Length Validation**
    - **Validates: Requirements 6.1, 6.3**
    - Test with fast-check that for any project name and description, output is 5-125 chars in correct format

  - [ ]* 5.5 Write property test for structured data validation
    - **Property 1: Structured Data Required Fields Validation**
    - **Validates: Requirements 2.5**
    - Create a validation function and test with fast-check that all required fields are non-empty strings

- [x] 6. Checkpoint - Verify semantic HTML and image optimization
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Implement URL and link optimization
  - [x] 7.1 Update Navbar.jsx with descriptive anchor text and hash link targets
    - Ensure all navigation links use descriptive text (About, Skills, Projects, Contact)
    - Verify each hash link href corresponds to an element with matching id in the DOM
    - Ensure graceful handling when target id doesn't exist (no-op scroll)
    - _Requirements: 10.1, 10.3, 10.4_

  - [x] 7.2 Update external links with security attributes
    - Add rel="noopener noreferrer" to all external links with target="_blank"
    - Apply to project GitHub links and live demo links in Projects.jsx
    - Apply to social links in Footer.jsx and any other external links
    - _Requirements: 10.2, 10.5_

  - [ ]* 7.3 Write property test for descriptive anchor text
    - **Property 7: Descriptive Anchor Text Validation**
    - **Validates: Requirements 10.1**
    - Test with fast-check that anchor text contains section-identifying words and not generic phrases

  - [ ]* 7.4 Write property test for external link security attributes
    - **Property 8: External Link Security Attributes**
    - **Validates: Requirements 10.2, 10.5**
    - Test with fast-check that external target="_blank" links always have noopener and noreferrer

  - [ ]* 7.5 Write property test for hash link target existence
    - **Property 9: Hash Link Target Existence**
    - **Validates: Requirements 10.3**
    - Test with fast-check that every hash link href has a corresponding DOM element with matching id

- [x] 8. Implement Core Web Vitals performance optimizations
  - [x] 8.1 Add resource preloading hints to index.html
    - Add `<link rel="preload">` for Inter font (critical above-fold resource)
    - Add preload for critical CSS needed for Hero and Navbar rendering
    - _Requirements: 7.5_

  - [x] 8.2 Implement lazy loading for below-fold content
    - Add `loading="lazy"` to all images below the initial viewport
    - Implement Intersection Observer wrapper for Three.js canvas components (About section)
    - Lazy-load FloatingParticles and ChatWidget using React.lazy + Suspense
    - _Requirements: 7.4, 7.6_

  - [x] 8.3 Update CRACO config for code splitting and defer
    - Configure webpack to code-split non-critical components (ChatWidget, FloatingParticles)
    - Ensure non-critical JS/CSS uses async or defer attributes
    - _Requirements: 7.4_

  - [x] 8.4 Add explicit dimensions to images for CLS prevention
    - Add width/height attributes or aspect-ratio CSS to all img elements
    - Ensure CLS score remains below 0.1
    - _Requirements: 6.4, 7.2_

- [x] 9. Implement pre-rendering for search engine crawlers
  - [x] 9.1 Install and configure react-snap
    - Add `react-snap` as dev dependency
    - Configure in package.json with reactSnap settings (source: "build", inlineCss: true, puppeteerArgs)
    - Add react-snap to postbuild script (after sitemap/robots generation)
    - _Requirements: 8.1, 8.2, 8.3_

  - [x] 9.2 Update index.html noscript element
    - Update `<noscript>` content to: "This portfolio requires JavaScript for full interactivity. Please enable JavaScript in your browser settings to view all content."
    - _Requirements: 8.4_

  - [x] 9.3 Verify pre-rendered output matches hydrated content
    - Ensure pre-rendered HTML contains text from all sections (Hero, About, Skills, Projects, Contact, Footer)
    - Verify meta tags, JSON-LD, and OG tags are present in the static HTML
    - _Requirements: 8.1, 8.2, 8.5_

- [x] 10. Implement mobile-friendliness optimizations
  - [x] 10.1 Verify viewport meta tag and responsive styles
    - Confirm viewport meta tag has width=device-width and initial-scale=1 (already present)
    - Audit CSS for any fixed-width elements that could cause horizontal overflow on 320px-1024px viewports
    - Fix any overflow issues found
    - _Requirements: 9.1, 9.2_

  - [x] 10.2 Ensure touch target sizing and spacing
    - Audit all buttons, links, and form inputs for minimum 48x48px tappable area at viewport ≤1024px
    - Add minimum spacing of 8px between adjacent touch targets
    - Fix any elements that don't meet the threshold
    - _Requirements: 9.3_

  - [x] 10.3 Verify text sizing and image scaling
    - Ensure body text is 16px or larger at viewport ≤768px
    - Ensure all images scale within viewport width without overflow at 320px+
    - _Requirements: 9.4, 9.5_

- [x] 11. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties using `fast-check`
- Unit tests validate specific examples and edge cases
- The project uses JavaScript (React with CRA+CRACO) — all code examples and implementations use JS/JSX
- The production domain is `https://sujalmeena.dev`
- react-snap is used for pre-rendering instead of SSR to minimize migration cost

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.4", "2.1", "2.2"] },
    { "id": 1, "tasks": ["1.2", "1.3", "2.3"] },
    { "id": 2, "tasks": ["2.4", "4.1", "4.7", "5.1", "5.2"] },
    { "id": 3, "tasks": ["4.2", "4.3", "4.4", "4.5", "4.6", "5.3", "7.1", "7.2"] },
    { "id": 4, "tasks": ["4.8", "5.4", "5.5", "7.3", "7.4", "7.5"] },
    { "id": 5, "tasks": ["8.1", "8.2", "8.4", "10.1", "10.2", "10.3"] },
    { "id": 6, "tasks": ["8.3", "9.2"] },
    { "id": 7, "tasks": ["9.1"] },
    { "id": 8, "tasks": ["9.3"] }
  ]
}
```
