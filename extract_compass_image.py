#!/usr/bin/env python3
"""
Run this once in Terminal to extract the Compass panel image:
  python3 ~/Desktop/my-portfolio/extract_compass_image.py
"""
import subprocess, sys, os

src = os.path.expanduser("~/Downloads/Compass/Compass Electrical Panel.pdf")
dst = os.path.join(os.path.dirname(__file__), "compass.png")

# Try pdf2image first
try:
    from pdf2image import convert_from_path
    imgs = convert_from_path(src, first_page=1, last_page=1, dpi=180)
    imgs[0].save(dst, "PNG")
    print(f"✓ Saved compass.png ({imgs[0].size[0]}×{imgs[0].size[1]})")
    sys.exit(0)
except Exception as e:
    print(f"pdf2image failed ({e}), trying ghostscript...")

# Fall back to ghostscript (usually pre-installed on Mac via Homebrew)
try:
    result = subprocess.run([
        "gs", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pngalpha",
        "-r180", "-dFirstPage=1", "-dLastPage=1",
        f"-sOutputFile={dst}", src
    ], capture_output=True, text=True)
    if os.path.exists(dst):
        print(f"✓ Saved compass.png via ghostscript")
    else:
        print("ghostscript failed:", result.stderr[-300:])
        sys.exit(1)
except FileNotFoundError:
    # Last resort: sips (built into macOS)
    result = subprocess.run(["sips", "-s", "format", "png", src, "--out", dst],
                            capture_output=True, text=True)
    if os.path.exists(dst):
        print(f"✓ Saved compass.png via sips")
    else:
        print("All methods failed. Please open the PDF in Preview, export page 1 as PNG,")
        print(f"and save it as:\n  {dst}")
