#!/usr/bin/env python3
"""
Example: Visual Question Answering (VQA) with Qwen3-VL.

This script demonstrates how to ask questions about images using
the Qwen3-VL model.

Usage:
    python vqa.py <image_path> <question>
"""

import sys
from pathlib import Path

# Add parent directory to path to import client
sys.path.insert(0, str(Path(__file__).parent.parent))

from client import Qwen3VLClient


def main():
    if len(sys.argv) < 3:
        print("Usage: python vqa.py <image_path> <question>")
        print("\nExamples:")
        print("  python vqa.py /path/to/image.jpg 'What is the main object?'")
        print("  python vqa.py /path/to/image.jpg 'How many people are in this image?'")
        print("  python vqa.py /path/to/image.jpg 'What is the weather like?'")
        sys.exit(1)

    image_path = sys.argv[1]
    question = sys.argv[2]

    print("=" * 70)
    print("Visual Question Answering with Qwen3-VL-4B")
    print("=" * 70)
    print(f"\nImage: {image_path}")
    print(f"Question: {question}")

    try:
        client = Qwen3VLClient()
        print("\nProcessing...")
        answer = client.answer_question(image_path, question)

        print("\nAnswer:")
        print("-" * 70)
        print(answer)
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
