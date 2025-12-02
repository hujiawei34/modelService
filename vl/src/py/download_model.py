#!/usr/bin/env python3
"""
Download the Qwen3-VL-4B-Instruct-FP8 model from HuggingFace.

This script downloads the model and stores it in the HuggingFace cache directory.
By default, models are cached in ~/.cache/huggingface/hub/

You can override the cache location by setting HF_HOME environment variable:
    export HF_HOME=/path/to/custom/cache
    python download_model.py
"""

import os
import sys
from pathlib import Path

def download_model():
    """Download the Qwen3-VL-4B-Instruct-FP8 model."""
    try:
        from huggingface_hub import snapshot_download
        import torch
    except ImportError:
        print("Error: Required packages not installed.")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)

    model_id = "Qwen/Qwen2-VL-2B-Instruct-AWQ"

    print(f"Downloading model: {model_id}")
    print(f"GPU: {torch.cuda.is_available() and torch.cuda.get_device_name(0) or 'CPU'}")
    print(f"CUDA version: {torch.version.cuda if torch.cuda.is_available() else 'N/A'}")

    # Check HuggingFace cache location
    hf_home = os.getenv('HF_HOME', os.path.expanduser('~/.cache/huggingface'))
    print(f"HuggingFace cache: {hf_home}")

    try:
        print("\nDownloading model (this may take several minutes)...")
        model_path = snapshot_download(
            repo_id=model_id,
            repo_type="model",
            cache_dir=os.path.join(hf_home, "hub"),
        )
        print("✓ Model downloaded successfully!")
        print(f"\nModel info:")
        print(f"  Model ID: {model_id}")
        print(f"  Local path: {model_path}")
        print(f"  Cache location: {hf_home}")
        print(f"\nYou can now use this model with vLLM:")
        print(f"  vllm serve {model_id} --gpu-memory-utilization 0.85 --load-format auto")

    except Exception as e:
        print(f"✗ Error downloading model: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    download_model()
