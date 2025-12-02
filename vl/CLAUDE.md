# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a project for deploying small language and vision models locally on WSL2 with an NVIDIA RTX 5060 (8GB VRAM). The project includes:

- **vl/**: Vision-Language model deployment, specifically for Qwen3-VL small model for image recognition tasks

## Development Environment

- **Platform**: WSL2 (Windows Subsystem for Linux)
- **GPU**: NVIDIA RTX 5060 with 8GB VRAM
- **Primary focus**: Deploying lightweight models that fit within 8GB VRAM constraints

## Key Constraints

When developing model deployment solutions:
- Target models that can run on 8GB VRAM
- Consider memory optimization techniques (quantization, pruning, etc.)
- Use memory-efficient inference frameworks when possible
- Profile memory usage during development

## Common Dependencies

The project will likely need:
- PyTorch or similar ML framework
- CUDA/cuDNN for GPU acceleration
- Vision model libraries (e.g., transformers for Qwen3-VL)
- Image processing libraries (PIL, OpenCV)
- Python 3.8+

## Implemented: Qwen3-VL-4B Vision Model

The project now has a complete implementation of Qwen3-VL-4B-Instruct-FP8 deployment:

### Key Files

- **`vl/requirements.txt`** - Python dependencies (vLLM, PyTorch, transformers, etc.)
- **`vl/download_model.py`** - Download model from HuggingFace to local cache
- **`vl/start_server.py`** - Launch vLLM API server with 8GB VRAM optimizations
- **`vl/client.py`** - Python client library for making inference requests
- **`vl/test_inference.py`** - Verify model loading and VRAM usage
- **`vl/examples/`** - Example scripts for common use cases

### Common Commands

```bash
# Install dependencies
cd vl && pip install -r requirements.txt

# Download model (first time only, ~4.5GB)
python download_model.py

# Start API server
python start_server.py

# In another terminal, test inference
python examples/caption_image.py /path/to/image.jpg
python examples/vqa.py /path/to/image.jpg "What is in this image?"
python examples/analyze_scene.py /path/to/image.jpg
```

### Architecture Notes

**Deployment Stack:**
- Framework: vLLM (OpenAI-compatible API)
- Model: Qwen3-VL-4B-Instruct-FP8 from HuggingFace
- Quantization: FP8 (50% memory savings, ~4-5GB VRAM usage)
- GPU: NVIDIA RTX 5060 with Ampere architecture

**Design Decisions:**
1. **API-first approach**: vLLM server for scalability and easy integration
2. **FP8 quantization**: Balances performance and memory efficiency
3. **Client library**: Provides high-level abstraction over HTTP API
4. **Example scripts**: Demonstrate common vision tasks (captioning, VQA, scene analysis)

**VRAM Optimizations:**
- `--gpu-memory-utilization 0.85`: Uses 85% of 8GB, leaving headroom for OS
- `--max-model-len 4096`: Balanced token limit for image processing
- `--load-format auto`: Automatic FP8 support detection

### Testing & Validation

Test the setup with:
```bash
# Verify model loads and check VRAM usage
python vl/test_inference.py

# Start server and test with real images
python vl/start_server.py  # In one terminal
python vl/examples/caption_image.py test_image.jpg  # In another
```

### Future Enhancements

Possible improvements:
- Add batch processing capabilities to client
- Implement caching for repeated queries
- Add benchmarking script for RTX 5060
- Support for fine-tuning on custom data
- Multi-modal input support (video frames)
