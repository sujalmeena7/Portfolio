const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://sujalmeena.xyz';
const BUILD_DIR = path.resolve(__dirname, '..', 'build');
const PUBLIC_DIR = path.resolve(__dirname, '..', 'public');
const OUTPUT_PATHS = [
  path.join(BUILD_DIR, 'sitemap.xml'),
  path.join(PUBLIC_DIR, 'sitemap.xml'),
];

function generateSitemap() {
  const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD format

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${BASE_URL}/</loc>
    <lastmod>${today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
`;

  try {
    for (const outputPath of OUTPUT_PATHS) {
      const dir = path.dirname(outputPath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.writeFileSync(outputPath, xml, 'utf8');
      console.log(`Sitemap generated successfully: ${outputPath}`);
    }
  } catch (error) {
    process.stderr.write(`ERROR: Sitemap generation failed: ${error.message}\n`);
    process.exit(1);
  }
}

generateSitemap();
