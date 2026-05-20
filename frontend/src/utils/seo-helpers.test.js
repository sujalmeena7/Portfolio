import { formatProjectAltText, handleImageError } from './seo-helpers';

describe('formatProjectAltText', () => {
  it('returns projectName and description in correct format', () => {
    const result = formatProjectAltText('MyApp', 'A screenshot of the dashboard');
    expect(result).toBe('MyApp - A screenshot of the dashboard');
  });

  it('returns just projectName when no description is provided', () => {
    const result = formatProjectAltText('MyApp');
    expect(result).toBe('MyApp');
  });

  it('returns just projectName when description is empty string', () => {
    const result = formatProjectAltText('MyApp', '');
    expect(result).toBe('MyApp');
  });

  it('truncates output to 125 characters', () => {
    const longDesc = 'A'.repeat(200);
    const result = formatProjectAltText('Project', longDesc);
    expect(result.length).toBe(125);
    expect(result.startsWith('Project - ')).toBe(true);
  });

  it('ensures minimum 5 characters output by padding short names', () => {
    const result = formatProjectAltText('Hi');
    expect(result.length).toBe(5);
    expect(result.startsWith('Hi')).toBe(true);
  });

  it('handles empty projectName with description', () => {
    const result = formatProjectAltText('', 'Some description');
    expect(result).toBe(' - Some description');
  });

  it('handles null/undefined inputs gracefully', () => {
    const result = formatProjectAltText(null, undefined);
    expect(result.length).toBeGreaterThanOrEqual(5);
  });

  it('trims whitespace from inputs', () => {
    const result = formatProjectAltText('  MyApp  ', '  dashboard view  ');
    expect(result).toBe('MyApp - dashboard view');
  });

  it('handles exactly 125 characters without truncation', () => {
    const name = 'Project';
    const desc = 'A'.repeat(125 - name.length - 3); // 3 for " - "
    const result = formatProjectAltText(name, desc);
    expect(result.length).toBe(125);
  });
});

describe('handleImageError', () => {
  let img;
  let parent;

  beforeEach(() => {
    parent = document.createElement('div');
    img = document.createElement('img');
    parent.appendChild(img);
    document.body.appendChild(parent);
  });

  afterEach(() => {
    document.body.removeChild(parent);
  });

  it('hides the broken image element', () => {
    const event = { currentTarget: img, target: img };
    handleImageError(event, 'My Project');
    expect(img.style.display).toBe('none');
  });

  it('creates a fallback element with the project name', () => {
    const event = { currentTarget: img, target: img };
    handleImageError(event, 'My Project');
    const fallback = parent.querySelector('.image-fallback');
    expect(fallback).not.toBeNull();
    expect(fallback.textContent).toBe('My Project');
  });

  it('maintains reserved image space with aspect-ratio 16/9', () => {
    const event = { currentTarget: img, target: img };
    handleImageError(event, 'My Project');
    const fallback = parent.querySelector('.image-fallback');
    expect(fallback.style.aspectRatio).toBe('16 / 9');
  });

  it('styles the fallback with background color and centered text', () => {
    const event = { currentTarget: img, target: img };
    handleImageError(event, 'My Project');
    const fallback = parent.querySelector('.image-fallback');
    expect(fallback.style.display).toBe('flex');
    expect(fallback.style.alignItems).toBe('center');
    expect(fallback.style.justifyContent).toBe('center');
    expect(fallback.style.backgroundColor).toBeTruthy();
  });

  it('does not create duplicate fallbacks on multiple calls', () => {
    const event = { currentTarget: img, target: img };
    handleImageError(event, 'My Project');
    handleImageError(event, 'My Project');
    const fallbacks = parent.querySelectorAll('.image-fallback');
    expect(fallbacks.length).toBe(1);
  });

  it('uses fallback text when projectName is empty', () => {
    const event = { currentTarget: img, target: img };
    handleImageError(event, '');
    const fallback = parent.querySelector('.image-fallback');
    expect(fallback.textContent).toBe('Image unavailable');
  });

  it('uses event.target when currentTarget is not available', () => {
    const event = { target: img };
    handleImageError(event, 'Fallback Project');
    expect(img.style.display).toBe('none');
    const fallback = parent.querySelector('.image-fallback');
    expect(fallback).not.toBeNull();
    expect(fallback.textContent).toBe('Fallback Project');
  });

  it('sets width to 100% on the fallback element', () => {
    const event = { currentTarget: img, target: img };
    handleImageError(event, 'My Project');
    const fallback = parent.querySelector('.image-fallback');
    expect(fallback.style.width).toBe('100%');
  });
});
