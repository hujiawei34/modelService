#!/usr/bin/env python3
"""
Example: Generate image captions with Qwen3-VL.

This script demonstrates how to use the client to generate detailed
descriptions of images using the Qwen3-VL model.

Usage:
    python caption_image.py <image_path>
"""

import sys
from pathlib import Path

# Add parent directory to path to import client
sys.path.insert(0, str(Path(__file__).parent.parent))

from client import Qwen3VLClient


def main():
    if len(sys.argv) < 2:
        print("Usage: python caption_image.py <image_path>")
        print("\nExample:")
        print("  python caption_image.py /path/to/image.jpg")
        sys.exit(1)

    image_path = sys.argv[1]

    print("=" * 70)
    print("Image Captioning with Qwen3-VL-4B")
    print("=" * 70)
    print(f"\nImage: {image_path}")

    try:
        client = Qwen3VLClient()
        print("\nGenerating caption...")
        caption = client.caption_image(image_path)

        print("\nCaption:")
        print("-" * 70)
        print(caption)
        print("-" * 70)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure the vLLM server is running:")
        print("  python start_server.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
