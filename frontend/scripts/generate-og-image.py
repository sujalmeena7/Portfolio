"""
Generate OG image for social media sharing.
Creates a 1200x630 PNG with branded text on a dark gradient background.
Output: frontend/public/og-image.png
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Image dimensions (minimum for OG images)
WIDTH = 1200
HEIGHT = 630

# Colors
BG_COLOR_TOP = (15, 23, 42)       # Dark slate (slate-900)
BG_COLOR_BOTTOM = (30, 41, 59)    # Slightly lighter slate (slate-800)
ACCENT_COLOR = (99, 102, 241)     # Indigo-500
TEXT_COLOR_PRIMARY = (255, 255, 255)   # White
TEXT_COLOR_SECONDARY = (148, 163, 184) # Slate-400
ACCENT_GLOW = (129, 140, 248)     # Indigo-400

def create_gradient(draw, width, height, color_top, color_bottom):
    """Create a vertical gradient background."""
    for y in range(height):
        ratio = y / height
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * ratio)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * ratio)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def draw_accent_elements(draw, width, height):
    """Draw decorative accent elements."""
    # Top-left accent corner
    for i in range(3):
        offset = i * 4
        draw.line([(40 + offset, 40), (40 + offset, 100)], fill=ACCENT_COLOR, width=2)
    for i in range(3):
        offset = i * 4
        draw.line([(40, 40 + offset), (100, 40 + offset)], fill=ACCENT_COLOR, width=2)

    # Bottom-right accent corner
    for i in range(3):
        offset = i * 4
        draw.line([(width - 40 - offset, height - 40), (width - 40 - offset, height - 100)], fill=ACCENT_COLOR, width=2)
    for i in range(3):
        offset = i * 4
        draw.line([(width - 40, height - 40 - offset), (width - 100, height - 40 - offset)], fill=ACCENT_COLOR, width=2)

    # Accent line separator
    draw.line([(100, height // 2 + 30), (width - 100, height // 2 + 30)], fill=ACCENT_COLOR, width=2)

    # Decorative dots pattern (top-right area)
    for row in range(5):
        for col in range(8):
            x = width - 250 + col * 20
            y = 60 + row * 20
            opacity = max(0, 255 - (row + col) * 30)
            if opacity > 50:
                draw.ellipse([(x-2, y-2), (x+2, y+2)], fill=(*ACCENT_COLOR, opacity))

def get_font(size):
    """Try to get a good font, fall back to default."""
    font_paths = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def get_bold_font(size):
    """Try to get a bold font, fall back to regular."""
    font_paths = [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return get_font(size)

def main():
    # Create image with RGBA for transparency support in elements
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR_TOP)
    draw = ImageDraw.Draw(img)

    # Draw gradient background
    create_gradient(draw, WIDTH, HEIGHT, BG_COLOR_TOP, BG_COLOR_BOTTOM)

    # Draw accent decorative elements
    draw_accent_elements(draw, WIDTH, HEIGHT)

    # Load fonts
    font_name = get_bold_font(56)
    font_title = get_font(32)
    font_subtitle = get_font(24)
    font_url = get_font(20)

    # Main name text
    name_text = "Sujal Meena"
    name_bbox = draw.textbbox((0, 0), name_text, font=font_name)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = (WIDTH - name_width) // 2
    name_y = HEIGHT // 2 - 100

    # Draw name with slight glow effect
    draw.text((name_x + 1, name_y + 1), name_text, fill=(99, 102, 241, 80), font=font_name)
    draw.text((name_x, name_y), name_text, fill=TEXT_COLOR_PRIMARY, font=font_name)

    # Job title
    title_text = "Full-Stack AI Engineer"
    title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (WIDTH - title_width) // 2
    title_y = name_y + 80

    draw.text((title_x, title_y), title_text, fill=ACCENT_GLOW, font=font_title)

    # Subtitle / tagline
    subtitle_text = "Agentic Workflows • RAG Pipelines • High-Performance Web Apps"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=font_subtitle)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (WIDTH - subtitle_width) // 2
    subtitle_y = title_y + 80

    draw.text((subtitle_x, subtitle_y), subtitle_text, fill=TEXT_COLOR_SECONDARY, font=font_subtitle)

    # URL at bottom
    url_text = "sujalmeena.dev"
    url_bbox = draw.textbbox((0, 0), url_text, font=font_url)
    url_width = url_bbox[2] - url_bbox[0]
    url_x = (WIDTH - url_width) // 2
    url_y = HEIGHT - 80

    draw.text((url_x, url_y), url_text, fill=TEXT_COLOR_SECONDARY, font=font_url)

    # Output path
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public')
    output_path = os.path.join(output_dir, 'og-image.png')

    # Save with optimization
    img.save(output_path, 'PNG', optimize=True)

    # Verify file size
    file_size = os.path.getsize(output_path)
    file_size_kb = file_size / 1024

    print(f"OG image generated successfully!")
    print(f"  Path: {output_path}")
    print(f"  Dimensions: {WIDTH}x{HEIGHT} pixels")
    print(f"  File size: {file_size_kb:.1f} KB")

    if file_size_kb > 500:
        print(f"  WARNING: File size exceeds 500 KB limit!")
        return 1

    if file_size_kb <= 500:
        print(f"  ✓ File size is within 500 KB limit")

    return 0

if __name__ == "__main__":
    exit(main())
