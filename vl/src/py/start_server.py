#!/usr/bin/env python3
"""
Start vLLM API server for Qwen2-VL-2B-Instruct-AWQ.

This script launches the vLLM inference server with optimized settings for 8GB VRAM.
Uses 4-bit quantization (AWQ) to fit comfortably in memory.

Example usage:
    python start_server.py

The server will start on http://localhost:8000 by default.
"""

import subprocess
import sys
import os

def start_server():
    """Start the vLLM server."""
    model_id = "Qwen/Qwen2-VL-2B-Instruct-AWQ"
    port = 8000

    # vLLM command with settings for 8GB VRAM
    # Using AWQ quantization for significant memory savings
    cmd = [
        "vllm",
        "serve",
        model_id,
        "--gpu-memory-utilization", "0.82",   # High utilization allowed for small model
        "--max-model-len", "4096",            # Good context size
        "--quantization", "awq",              # Explicitly use AWQ
        "--enforce-eager",                    # Disable CUDA graphs
        "--load-format", "auto",
        "--port", str(port),
        "--dtype", "half",                    # AWQ usually works best with half/float16
    ]

    print("=" * 70)
    print("Qwen2-VL-2B-Instruct-AWQ vLLM Server")
    print("=" * 70)
    print(f"\nModel: {model_id}")
    print(f"Port: {port}")
    print(f"Quantization: AWQ (4-bit)")

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server()
