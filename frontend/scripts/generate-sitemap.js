const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://sujalmeena.dev';
const OUTPUT_DIR = path.resolve(__dirname, '..', 'build');
const OUTPUT_PATH = path.join(OUTPUT_DIR, 'sitemap.xml');

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
    if (!fs.existsSync(OUTPUT_DIR)) {
      fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }

    fs.writeFileSync(OUTPUT_PATH, xml, 'utf8');
    console.log(`Sitemap generated successfully: ${OUTPUT_PATH}`);
  } catch (error) {
    process.stderr.write(`ERROR: Sitemap generation failed: ${error.message}\n`);
    process.exit(1);
  }
}

generateSitemap();
