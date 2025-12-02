# GEMINI.md

This file provides context for Gemini when working with this repository.

## Project Overview

This project focuses on deploying small language and vision models locally on a Windows Subsystem for Linux (WSL2) environment equipped with an NVIDIA RTX 5060 (8GB VRAM).

The primary goal is to run efficient, low-memory models that fit within consumer hardware constraints. The current implementation features the **Qwen3-VL-4B-Instruct-FP8** vision-language model.

## Directory Structure

- **`vl/`**: Contains the deployment implementation for the Qwen3 Vision-Language model.
    - **`vl/examples/`**: Example scripts for image captioning, VQA, and scene analysis.
    - **`vl/client.py`**: Python client library for interacting with the model server.
    - **`vl/start_server.py`**: Script to launch the vLLM API server.
    - **`vl/download_model.py`**: Script to download the model artifacts.

## Technology Stack

- **Platform**: WSL2 (Linux)
- **Hardware Target**: NVIDIA RTX 5060 (8GB VRAM)
- **Inference Server**: vLLM (OpenAI-compatible API)
- **Model**: Qwen3-VL-4B-Instruct-FP8 (Quantized for efficiency)
- **Language**: Python 3.8+

## Development Workflow

### 1. Environment Setup

Dependencies are managed via `pip`. It is recommended to work within the `vl/` directory for the vision model context.

```bash
cd vl
pip install -r requirements.txt
```

### 2. Model Acquisition

Download the model weights from HuggingFace (requires internet access).

```bash
python vl/download_model.py
```

### 3. Running the Server

Start the vLLM inference server. This script includes specific optimizations for 8GB VRAM cards (e.g., FP8 quantization, memory utilization limits).

```bash
python vl/start_server.py
```

*Note: The server typically runs on `http://localhost:8000`.*

### 4. Usage & Testing

Use the provided client or example scripts to interact with the running server.

**Client Library:**
```python
from vl.client import Qwen3VLClient
client = Qwen3VLClient()
print(client.caption_image("path/to/image.jpg"))
```

**Example Scripts:**
```bash
python vl/examples/caption_image.py <image_path>
python vl/examples/vqa.py <image_path> "<question>"
python vl/examples/analyze_scene.py <image_path>
```

## Conventions

- **API-First**: The project prioritizes serving models via an API (vLLM) rather than standalone scripts for flexibility and scalability.
- **Memory Optimization**: All code and configurations must respect the strict 8GB VRAM limit. FP8 quantization and memory utilization flags are critical.
- **Documentation**: Keep `readme.md` and `DEPLOYMENT.md` inside subdirectories updated with specific model instructions.

## Key Configuration

Important flags usually found in `vl/start_server.py`:
- `--gpu-memory-utilization`: set to ~0.85 to prevent OOM errors.
- `--max-model-len`: set to ~4096 to balance context window and memory usage.
- `--quantization`: set to `fp8` for the Qwen3-VL model.
