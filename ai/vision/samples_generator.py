"""
Generates synthetic realistic artisan raw test images and sample artifacts.
Creates test files for:
- Bamboo basket
- Pottery / Terracotta
- Handwoven textile
- Wooden handicraft
"""

import os
import math
from PIL import Image, ImageDraw, ImageFilter


def create_sample_images(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    # 1. Bamboo Basket (Raw photo: dim room, off-center, uneven lighting)
    w, h = 800, 600
    img1 = Image.new("RGB", (w, h), (130, 120, 110))  # Dull workshop floor
    draw1 = ImageDraw.Draw(img1)
    
    # Floor clutter
    for i in range(0, w, 40):
        draw1.line([(i, 0), (i, h)], fill=(115, 105, 95), width=1)

    # Woven Bamboo basket body (yellowish-brown weave)
    cx, cy, rx, ry = 440, 320, 180, 140
    for r in range(ry, 0, -8):
        shade = 160 + (ry - r) // 2
        draw1.ellipse([cx - int(rx * (r/ry)), cy - r, cx + int(rx * (r/ry)), cy + r], fill=(shade, shade - 30, 60))
    # Weave lines
    for angle in range(0, 360, 15):
        rad = math.radians(angle)
        x_end = cx + int(rx * 0.9 * math.cos(rad))
        y_end = cy + int(ry * 0.9 * math.sin(rad))
        draw1.line([(cx, cy), (x_end, y_end)], fill=(110, 80, 40), width=2)

    # Slightly dim lighting filter
    img1 = img1.filter(ImageFilter.GaussianBlur(radius=0.5))
    path1 = os.path.join(output_dir, "bamboo_basket.jpg")
    img1.save(path1, "JPEG", quality=85)

    # 2. Pottery / Terracotta Pot (Warm reddish brown clay with geometric motifs)
    w, h = 640, 640
    img2 = Image.new("RGB", (w, h), (150, 145, 140))  # Concrete table backdrop
    draw2 = ImageDraw.Draw(img2)
    
    # Pottery pot shape
    cx, cy = 300, 340
    # Base and body
    draw2.ellipse([cx - 150, cy - 120, cx + 150, cy + 160], fill=(185, 75, 45))
    # Neck and rim
    draw2.rectangle([cx - 60, cy - 180, cx + 60, cy - 110], fill=(195, 85, 50))
    draw2.ellipse([cx - 75, cy - 200, cx + 75, cy - 170], fill=(160, 60, 35))
    # Handpainted traditional white motifs
    for x in range(cx - 110, cx + 110, 24):
        draw2.polygon([(x, cy - 10), (x + 12, cy + 15), (x + 24, cy - 10)], outline=(240, 235, 220), width=2)
        draw2.ellipse([x + 8, cy + 30, x + 16, cy + 38], fill=(240, 235, 220))

    path2 = os.path.join(output_dir, "terracotta_pottery.jpg")
    img2.save(path2, "JPEG", quality=88)

    # 3. Handwoven Textile / Silk Dupatta (Rich indigo & gold zari patterns)
    w, h = 720, 960
    img3 = Image.new("RGB", (w, h), (90, 85, 80))  # Wooden loom bench
    draw3 = ImageDraw.Draw(img3)
    
    # Cloth drape
    draw3.polygon([(100, 60), (620, 90), (580, 890), (80, 850)], fill=(30, 50, 120))  # Royal indigo cloth
    # Gold zari border
    draw3.rectangle([110, 700, 570, 760], fill=(215, 175, 40))
    for i in range(120, 560, 20):
        draw3.line([(i, 705), (i + 10, 755)], fill=(160, 120, 20), width=2)
        draw3.line([(i + 10, 705), (i, 755)], fill=(245, 210, 70), width=2)

    # Small gold bootis (motifs)
    for row in range(150, 650, 80):
        for col in range(160, 540, 80):
            draw3.polygon([(col, row - 12), (col + 10, row), (col, row + 12), (col - 10, row)], fill=(225, 185, 50))

    path3 = os.path.join(output_dir, "handwoven_textile.jpg")
    img3.save(path3, "JPEG", quality=85)

    # 4. Wooden Handicraft (Carved elephant artifact with walnut finish)
    w, h = 750, 750
    img4 = Image.new("RGB", (w, h), (140, 135, 130))
    draw4 = ImageDraw.Draw(img4)

    # Carved wood figure
    cx, cy = 370, 390
    draw4.ellipse([cx - 160, cy - 100, cx + 140, cy + 110], fill=(110, 60, 30))  # Body
    draw4.ellipse([cx - 210, cy - 130, cx - 110, cy - 10], fill=(120, 65, 35))   # Head
    # Trunk
    draw4.arc([cx - 260, cy - 110, cx - 180, cy + 40], start=90, end=270, fill=(90, 50, 25), width=18)
    # Legs
    draw4.rectangle([cx - 140, cy + 60, cx - 90, cy + 160], fill=(95, 52, 26))
    draw4.rectangle([cx - 40, cy + 60, cx + 10, cy + 160], fill=(95, 52, 26))
    draw4.rectangle([cx + 60, cy + 60, cx + 110, cy + 160], fill=(95, 52, 26))
    # Carved patterns on saddle
    draw4.rectangle([cx - 80, cy - 80, cx + 60, cy + 10], fill=(175, 120, 45))
    draw4.ellipse([cx - 165, cy - 90, cx - 150, cy - 75], fill=(220, 210, 190))  # Eye

    path4 = os.path.join(output_dir, "wooden_handicraft.png")
    img4.save(path4, "PNG")

    print(f"Sample artisan product images generated in: {output_dir}")
    return [path1, path2, path3, path4]


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "samples")
    create_sample_images(out)
