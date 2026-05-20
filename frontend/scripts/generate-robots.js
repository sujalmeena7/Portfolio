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
  const sitemapUrl = 'https://sujalmeena.dev/sitemap.xml';
  const outputDir = path.resolve(__dirname, '..', 'build');
  const outputPath = path.join(outputDir, 'robots.txt');

  const content = [
    'User-agent: *',
    'Allow: /',
    'Disallow: /api/',
    '',
    `Sitemap: ${sitemapUrl}`,
    '' // trailing newline
  ].join('\n');

  try {
    // Create build directory if it doesn't exist
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    fs.writeFileSync(outputPath, content, 'utf8');
    console.log(`robots.txt generated successfully at ${outputPath}`);
  } catch (error) {
    process.stderr.write(`ERROR: robots.txt generation failed: ${error.message}\n`);
    process.exit(1);
  }
}

generateRobots();
