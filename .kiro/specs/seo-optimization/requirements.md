# Requirements Document

## Introduction

This document defines the requirements for comprehensive SEO optimization of Sujal Meena's portfolio website. The goal is to make the site discoverable by search engines, eligible for Google Search Console submission, and well-ranked in search results. The portfolio is a single-page React application (Create React App with CRACO) served alongside a FastAPI backend, deployed on EC2.

## Glossary

- **Portfolio_Site**: The React-based single-page application serving as Sujal Meena's portfolio website
- **Search_Engine**: Web crawlers and indexing services (primarily Google) that discover and rank web pages
- **Meta_Tag_System**: The collection of HTML meta elements in the document head that provide metadata to search engines and social platforms
- **Structured_Data_Module**: The JSON-LD schema markup embedded in the page to help search engines understand page content
- **Sitemap_Generator**: A build-time process that produces an XML sitemap listing all crawlable URLs
- **Robots_Configuration**: The robots.txt file that instructs search engine crawlers on which paths to crawl or ignore
- **Open_Graph_Tags**: Meta tags following the Open Graph protocol for rich link previews on social platforms (Facebook, LinkedIn)
- **Twitter_Card_Tags**: Meta tags specific to Twitter/X for controlling how links appear when shared
- **Core_Web_Vitals**: Google's set of metrics (LCP, FID/INP, CLS) measuring real-world user experience
- **Canonical_URL**: An HTML link element that specifies the preferred URL for a page to prevent duplicate content issues
- **Heading_Hierarchy**: The structured use of h1-h6 HTML elements to convey content organization to search engines
- **Pre_Renderer**: A service or build step that generates static HTML snapshots of the SPA for search engine crawlers

## Requirements

### Requirement 1: Meta Tag Configuration

**User Story:** As a site owner, I want comprehensive meta tags in the HTML head, so that search engines and social platforms display accurate information about my portfolio.

#### Acceptance Criteria

1. THE Meta_Tag_System SHALL include a title tag that contains the site owner's full name and professional role, with a total length between 30 and 60 characters
2. THE Meta_Tag_System SHALL include a meta description tag between 150 and 160 characters summarizing the portfolio's purpose
3. THE Meta_Tag_System SHALL include Open_Graph_Tags for og:title, og:description, og:image, og:url, and og:type, where og:image references an image with minimum dimensions of 1200x630 pixels
4. THE Meta_Tag_System SHALL include Twitter_Card_Tags with twitter:card set to "summary_large_image", and include twitter:title, twitter:description, and twitter:image
5. THE Meta_Tag_System SHALL include a Canonical_URL link element with rel="canonical" and an href value matching the fully qualified production domain URL where the site is deployed
6. WHEN the page HTML is fetched by a social platform crawler, THE Meta_Tag_System SHALL provide og:title, og:description, og:image, og:url, twitter:title, twitter:description, and twitter:image tags all with non-empty values so that a link preview renders with an image, title, and description

### Requirement 2: Structured Data Markup

**User Story:** As a site owner, I want JSON-LD structured data on my portfolio, so that search engines can display rich results and understand my professional profile.

#### Acceptance Criteria

1. THE Structured_Data_Module SHALL embed a JSON-LD script with @context set to "https://schema.org" and @type "Person" containing the properties: name, jobTitle, url, and at least 1 social profile link using the sameAs property
2. THE Structured_Data_Module SHALL embed a JSON-LD script with @context set to "https://schema.org" and @type "WebSite" containing the properties: name, url, and description with a maximum length of 160 characters
3. THE Structured_Data_Module SHALL produce valid JSON-LD that passes Google's Rich Results Test with zero errors and zero warnings
4. WHEN a search engine crawls the page, THE Structured_Data_Module SHALL be present in the initial HTML response without requiring JavaScript execution
5. THE Structured_Data_Module SHALL ensure every required property (name, jobTitle, url, sameAs in Person; name, url, description in WebSite) contains a non-empty string value

### Requirement 3: Sitemap Generation

**User Story:** As a site owner, I want an XML sitemap generated at build time, so that search engines can discover all important pages on my site.

#### Acceptance Criteria

1. THE Sitemap_Generator SHALL produce an XML sitemap that conforms to the Sitemaps.org protocol 0.9 schema and is written to frontend/build/sitemap.xml
2. THE Sitemap_Generator SHALL include exactly one URL entry containing the site's canonical base URL (the production domain root) with a lastmod element in W3C Datetime YYYY-MM-DD format set to the build date
3. THE Sitemap_Generator SHALL include a priority element set to 1.0 and a changefreq element set to "monthly" for the homepage URL entry
4. WHEN the build process completes, THE Sitemap_Generator SHALL output the sitemap.xml file to the frontend/build/ directory as part of the build step
5. IF the Sitemap_Generator fails to produce the sitemap.xml file, THEN THE build process SHALL fail with an error message indicating the sitemap generation failure

### Requirement 4: Robots.txt Configuration

**User Story:** As a site owner, I want a properly configured robots.txt file, so that search engine crawlers know which parts of my site to index and where to find the sitemap.

#### Acceptance Criteria

1. THE Robots_Configuration SHALL specify the wildcard user-agent (`User-agent: *`) and allow crawling of all paths by default
2. THE Robots_Configuration SHALL include a `Disallow: /api/` directive under the wildcard user-agent to prevent indexing of all backend API endpoints and their sub-paths
3. THE Robots_Configuration SHALL include a `Sitemap` directive containing the absolute URL of sitemap.xml in the format `https://<domain>/sitemap.xml`, where `<domain>` is the production domain of the deployed site
4. THE Robots_Configuration SHALL be served as a plain-text file at the path `/robots.txt` from the site root
5. THE Robots_Configuration SHALL conform to the Robots Exclusion Protocol syntax, containing no more than one `User-agent: *` group with its associated directives and one `Sitemap` directive

### Requirement 5: Semantic HTML and Heading Hierarchy

**User Story:** As a site owner, I want semantic HTML structure with proper heading hierarchy, so that search engines can understand the content organization and importance of each section.

#### Acceptance Criteria

1. THE Portfolio_Site SHALL use exactly one h1 element on the page, located within the Hero section, containing the site owner's primary headline text
2. THE Portfolio_Site SHALL use h2 elements for each major section heading (About, Skills, Projects, Contact), ensuring each section's visible title is rendered as an h2 element
3. THE Portfolio_Site SHALL maintain a sequential heading hierarchy without skipping levels, where h3 elements appear only within a parent section that contains an h2, and no heading level is omitted between ancestor and descendant headings
4. THE Portfolio_Site SHALL use semantic HTML5 elements to define page structure, including: a header element for the top navigation bar, a nav element for navigation link groups, a main element wrapping all primary content sections, section elements for each top-level content area (Hero, About, Skills, Projects, Contact), article elements for individual project cards, and a footer element for the page footer
5. THE Portfolio_Site SHALL include aria-label attributes on all nav elements and on any landmark region (header, main, footer) where more than one instance of that landmark type exists on the page, with each aria-label value containing 2 to 50 characters that identify the purpose of the region
6. WHEN the page is rendered, THE Portfolio_Site SHALL ensure every section element has either an aria-label attribute or an aria-labelledby attribute referencing the id of its heading element, so that each section is identifiable by assistive technologies

### Requirement 6: Image Optimization and Alt Text

**User Story:** As a site owner, I want all images to have descriptive alt text and be optimized for performance, so that search engines can index visual content and the site loads quickly.

#### Acceptance Criteria

1. THE Portfolio_Site SHALL include alt attributes on all img elements that convey meaningful content, where the alt text contains at minimum the subject of the image and its context within the page (e.g., project name and what the image depicts), with a length between 5 and 125 characters
2. THE Portfolio_Site SHALL use empty alt attributes (alt="") on images that serve a purely decorative purpose, including background patterns, grid overlays, and visual separators
3. WHEN project images are displayed, THE Portfolio_Site SHALL include alt text containing the project name followed by a description of the image content, formatted as "[Project Name] - [description of what the image shows]" with total length not exceeding 125 characters
4. THE Portfolio_Site SHALL specify explicit width and height attributes or aspect-ratio CSS on all img elements to maintain a Cumulative Layout Shift score of less than 0.1 as measured by Lighthouse
5. IF a project image fails to load, THEN THE Portfolio_Site SHALL display the project name as fallback text and maintain the reserved image space without causing layout reflow
6. THE Portfolio_Site SHALL serve images in files no larger than 500 KB each, in a web-optimized format (WebP, AVIF, or compressed PNG/JPEG)

### Requirement 7: Core Web Vitals Performance

**User Story:** As a site owner, I want my portfolio to meet Google's Core Web Vitals thresholds, so that performance does not negatively impact search rankings.

#### Acceptance Criteria

1. THE Portfolio_Site SHALL achieve a Largest Contentful Paint (LCP) of 2.5 seconds or less at the 75th percentile, measured using Lighthouse in mobile mode with simulated 4G throttling (1.6 Mbps download, 750 ms RTT)
2. THE Portfolio_Site SHALL achieve a Cumulative Layout Shift (CLS) score of 0.1 or less at the 75th percentile across the full page session lifetime
3. THE Portfolio_Site SHALL achieve an Interaction to Next Paint (INP) of 200 milliseconds or less at the 75th percentile for all user interactions including clicks, taps, and key presses
4. THE Portfolio_Site SHALL defer loading of JavaScript and CSS resources that are not required for rendering the initial viewport (Hero section, Navbar) by applying async or defer attributes to their script and link tags
5. THE Portfolio_Site SHALL preload fonts and resources required to render the above-the-fold content (Hero section and Navbar) using link rel="preload" hints in the document head
6. THE Portfolio_Site SHALL lazy-load images and the Three.js canvas component that are positioned below the initial viewport, initiating resource loading when the element is within 200 pixels of the visible viewport boundary

### Requirement 8: Pre-rendering for Search Engine Crawlers

**User Story:** As a site owner, I want search engine crawlers to receive fully rendered HTML content, so that my single-page application content is properly indexed.

#### Acceptance Criteria

1. THE Pre_Renderer SHALL generate static HTML within the root element that contains the text content from all rendered page sections (Hero, About, Skills, Projects, Contact, Footer)
2. WHEN a search engine crawler requests the page, THE Portfolio_Site SHALL serve pre-rendered HTML that includes the document title, meta description, Open Graph meta tags, and the text content of all page sections without requiring JavaScript execution
3. THE Pre_Renderer SHALL produce HTML output as part of the CRACO build step that is deployed as the index.html entry point, with the rendered content embedded inside the root div element
4. IF JavaScript fails to load, THEN THE Portfolio_Site SHALL display a noscript element containing a message that states JavaScript is required and directs the user to enable it in their browser settings
5. THE Pre_Renderer SHALL produce HTML output where the pre-rendered text content matches the content rendered by the client-side React application after hydration

### Requirement 9: Mobile-Friendliness

**User Story:** As a site owner, I want my portfolio to be fully responsive and mobile-friendly, so that it passes Google's mobile-friendliness criteria and ranks well in mobile search results.

#### Acceptance Criteria

1. THE Portfolio_Site SHALL include a viewport meta tag with width=device-width and initial-scale=1
2. THE Portfolio_Site SHALL render all text, images, and interactive elements without requiring horizontal scrolling on viewports from 320px to 1024px wide
3. WHILE the viewport width is 1024px or less, THE Portfolio_Site SHALL render all touch targets (buttons, links, form inputs) with a minimum tappable area of 48x48 CSS pixels and a minimum spacing of 8px between adjacent touch targets
4. WHILE the viewport width is 768px or less, THE Portfolio_Site SHALL render body text at a computed font size of 16px or larger
5. THE Portfolio_Site SHALL scale all images and media elements to fit within the viewport width without overflow or clipping on viewports 320px wide and above

### Requirement 10: URL and Link Optimization

**User Story:** As a site owner, I want clean URL structure and proper internal linking, so that search engines can efficiently crawl and understand the site's content relationships.

#### Acceptance Criteria

1. THE Portfolio_Site SHALL use anchor text that describes the link destination for all internal navigation links, where each link's visible text contains at least one word identifying the target section (e.g., "About", "Skills", "Work", "Contact") and SHALL NOT use generic phrases such as "click here", "read more", "link", or "here" as the sole anchor text
2. THE Portfolio_Site SHALL include rel="noopener noreferrer" on all external links (links with target="_blank" pointing to a domain other than the Portfolio_Site's own domain)
3. THE Portfolio_Site SHALL ensure every internal hash link href value (including #home, #about, #skills, #projects, and #contact) corresponds to an element with a matching id attribute rendered in the DOM at the time of navigation
4. IF an internal hash link is activated and no element with the target id exists in the DOM, THEN THE Portfolio_Site SHALL remain at the current scroll position without triggering a navigation error
5. WHEN external project links (GitHub repository links and live demo links) are rendered in the Projects section, THE Portfolio_Site SHALL include at minimum rel="noopener" on each anchor element that opens in a new tab
