#!/usr/bin/env python3
"""
Caption image using direct Qwen3-VL inference (no vLLM).

Memory efficient approach for 8GB VRAM systems.

Usage:
    python caption_image_direct.py /path/to/image.jpg
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference_direct import load_model, caption_image

def main():
    if len(sys.argv) < 2:
        print("Usage: python caption_image_direct.py <image_path>")
        print("\nExample: python caption_image_direct.py test.jpg")
        sys.exit(1)

    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)

    print(f"Loading Qwen3-VL-2B model...")
    model, processor = load_model()

    print(f"\nGenerating caption for: {image_path}")
    caption = caption_image(image_path, model, processor)

    print(f"\n{'='*70}")
    print("Generated Caption:")
    print(f"{'='*70}")
    print(caption)
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
