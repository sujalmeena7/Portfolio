/**
 * SEO helper utilities for the portfolio site.
 */

/**
 * Formats alt text for project images.
 *
 * @param {string} projectName - The name of the project.
 * @param {string} [description] - Optional description of what the image shows.
 * @returns {string} Formatted alt text between 5 and 125 characters.
 *
 * Format: "{projectName} - {description}" truncated to 125 chars.
 * If no description is provided, returns just the projectName.
 * Output is guaranteed to be at least 5 characters.
 */
export function formatProjectAltText(projectName, description) {
  const name = (projectName || '').trim();
  const desc = (description || '').trim();

  let altText;

  if (desc) {
    altText = `${name} - ${desc}`;
  } else {
    altText = name;
  }

  // Truncate to 125 characters max
  if (altText.length > 125) {
    altText = altText.slice(0, 125);
  }

  // Ensure minimum 5 characters by padding with spaces if needed
  if (altText.length < 5) {
    altText = altText.padEnd(5);
  }

  return altText;
}

/**
 * Handles image load errors by hiding the broken image and displaying
 * a styled fallback element with the project name.
 *
 * Maintains the reserved image space using CSS aspect-ratio to prevent
 * layout reflow (CLS).
 *
 * @param {Event} event - The error event from the img element's onError handler.
 * @param {string} projectName - The project name to display as fallback text.
 */
export function handleImageError(event, projectName) {
  const img = event.currentTarget || event.target;

  // Hide the broken image
  img.style.display = 'none';

  // Avoid creating duplicate fallbacks if handler fires multiple times
  const parent = img.parentElement;
  if (parent && parent.querySelector('.image-fallback')) {
    return;
  }

  // Create fallback element
  const fallback = document.createElement('div');
  fallback.className = 'image-fallback';
  fallback.textContent = projectName || 'Image unavailable';

  // Style the fallback to maintain reserved space and center text
  fallback.style.aspectRatio = '16 / 9';
  fallback.style.width = '100%';
  fallback.style.display = 'flex';
  fallback.style.alignItems = 'center';
  fallback.style.justifyContent = 'center';
  fallback.style.backgroundColor = '#1a1a2e';
  fallback.style.color = '#a0a0b0';
  fallback.style.fontSize = '1rem';
  fallback.style.fontWeight = '500';
  fallback.style.textAlign = 'center';
  fallback.style.padding = '1rem';
  fallback.style.borderRadius = '0.5rem';
  fallback.style.boxSizing = 'border-box';

  // Insert fallback after the hidden image
  img.insertAdjacentElement('afterend', fallback);
}
