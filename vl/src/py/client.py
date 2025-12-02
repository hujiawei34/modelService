#!/usr/bin/env python3
"""
Python client for Qwen3-VL-4B vLLM API.

This client library provides easy-to-use functions for making image understanding
requests to the Qwen3-VL model via the vLLM API.

Usage:
    client = Qwen3VLClient(base_url="http://localhost:8000")

    # Image captioning
    caption = client.caption_image("path/to/image.jpg")
    print(caption)

    # Visual question answering
    answer = client.answer_question("path/to/image.jpg", "What is in this image?")
    print(answer)
"""

import base64
import requests
from pathlib import Path
from typing import Optional, Union


class Qwen3VLClient:
    """Client for Qwen3-VL-4B model via vLLM API."""

    def __init__(self, base_url="http://localhost:8000", model="Qwen/Qwen2-VL-2B-Instruct-AWQ", timeout=120):
        """Initialize the client.

        Args:
            base_url: Base URL of the vLLM API server
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.model = model

    def _get_image_payload(self, image_path: Union[str, Path]) -> dict:
        """Read image and return API payload object."""
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")

        suffix = path.suffix.lower()
        mime = "image/png" if suffix == ".png" else "image/jpeg"
        if suffix == ".webp": mime = "image/webp"

        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")

        return {
            "type": "image_url",
            "image_url": {"url": f"data:{mime};base64,{b64}"}
        }

    def _make_request(self, messages: list, temperature: float = 0.7, max_tokens: int = 512) -> str:
        """Make request to vLLM API."""
        # Handle cases where base_url might already include /v1
        if self.base_url.endswith("/v1"):
            url = f"{self.base_url}/chat/completions"
        else:
            url = f"{self.base_url}/v1/chat/completions"

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()

            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception(f"Unexpected API response: {result}")

        except requests.exceptions.ConnectionError:
            raise Exception(
                f"Could not connect to vLLM server at {self.base_url}. "
                "Is the server running? Start it with: python start_server.py"
            )
        except requests.exceptions.Timeout:
            raise Exception(f"Request timed out after {self.timeout}s")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")

    def caption_image(self, image_path: Union[str, Path], temperature: float = 0.7) -> str:
        """Generate a caption for an image.

        Args:
            image_path: Path to the image file
            temperature: Sampling temperature (0.0-1.0)

        Returns:
            Generated image caption
        """
        image_payload = self._get_image_payload(image_path)

        messages = [
            {
                "role": "user",
                "content": [
                    image_payload,
                    {"type": "text", "text": "Please describe this image in detail."},
                ],
            }
        ]

        return self._make_request(messages, temperature=temperature)

    def answer_question(
        self, image_path: Union[str, Path], question: str, temperature: float = 0.7
    ) -> str:
        """Answer a question about an image.

        Args:
            image_path: Path to the image file
            question: The question to ask about the image
            temperature: Sampling temperature (0.0-1.0)

        Returns:
            Answer to the question
        """
        image_payload = self._get_image_payload(image_path)

        messages = [
            {
                "role": "user",
                "content": [
                    image_payload,
                    {"type": "text", "text": question},
                ],
            }
        ]

        return self._make_request(messages, temperature=temperature)

    def analyze_scene(self, image_path: Union[str, Path], temperature: float = 0.7) -> str:
        """Analyze the scene in an image.

        Args:
            image_path: Path to the image file
            temperature: Sampling temperature (0.0-1.0)

        Returns:
            Scene analysis
        """
        image_payload = self._get_image_payload(image_path)

        messages = [
            {
                "role": "user",
                "content": [
                    image_payload,
                    {
                        "type": "text",
                        "text": "Analyze this scene. What are the main objects, their relationships, and the overall context?",
                    },
                ],
            }
        ]

        return self._make_request(messages, temperature=temperature)


if __name__ == "__main__":
    print("Qwen3-VL Client Library")
    print("=" * 50)
    print("\nUsage examples:")
    print("\n1. Image Captioning:")
    print("   client = Qwen3VLClient()")
    print("   caption = client.caption_image('image.jpg')")
    print("\n2. Visual Q&A:")
    print("   answer = client.answer_question('image.jpg', 'What is this?')")
    print("\n3. Scene Analysis:")
    print("   analysis = client.analyze_scene('image.jpg')")
    print("\nMake sure the vLLM server is running first:")
    print("   python start_server.py")
