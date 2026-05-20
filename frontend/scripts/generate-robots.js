const fs = require('fs');
const path = require('path');

/**
 * Generates a robots.txt file for the portfolio site.
 * Conforms to the Robots Exclusion Protocol syntax.
 *
 * Directives:
 * - User-agent: * (applies to all crawlers)
 * - Allow: / (allow crawling of all paths by default)
 * - Disallow: /api/ (prevent indexing of backend API endpoints)
 * - Sitemap: absolute URL to sitemap.xml
 */
function generateRobots() {
  const sitemapUrl = 'https://sujalmeena.xyz/sitemap.xml';
  const outputPaths = [
    path.join(path.resolve(__dirname, '..', 'build'), 'robots.txt'),
    path.join(path.resolve(__dirname, '..', 'public'), 'robots.txt'),
  ];

  const content = [
    'User-agent: *',
    'Allow: /',
    'Disallow: /api/',
    '',
    `Sitemap: ${sitemapUrl}`,
    '' // trailing newline
  ].join('\n');

  try {
    for (const outputPath of outputPaths) {
      const dir = path.dirname(outputPath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.writeFileSync(outputPath, content, 'utf8');
      console.log(`robots.txt generated successfully at ${outputPath}`);
    }
  } catch (error) {
    process.stderr.write(`ERROR: robots.txt generation failed: ${error.message}\n`);
    process.exit(1);
  }
}

generateRobots();
