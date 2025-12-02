# Deployment Guide: Qwen3-VL-4B-Instruct-FP8

Complete guide for setting up and deploying the Qwen3-VL-4B-Instruct-FP8 model on WSL2 with NVIDIA RTX 5060.

## Prerequisites

- WSL2 (Windows Subsystem for Linux 2)
- NVIDIA RTX 5060 (8GB VRAM)
- NVIDIA CUDA 12.8+ (verify with `nvcc --version`)
- Python 3.8+
- pip package manager

## Step 1: Environment Preparation

### Verify GPU Setup
```bash
# Check GPU is detected
nvidia-smi

# Expected output:
# NVIDIA GeForce RTX 5060 with 8GB VRAM
# Driver version should be recent
```

### Verify CUDA
```bash
# Check CUDA version
nvcc --version

# Should output CUDA version 12.8 or higher
```

### Create Virtual Environment (if not already done)
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate

# Verify activation
which python
```

## Step 2: Install Dependencies

Navigate to the vl directory:
```bash
cd vl
```

Install all required packages:
```bash
pip install -r requirements.txt
```

This installs:
- **vllm** (>=0.8.4) - Fast LLM inference engine
- **torch** (>=2.0.0) - Deep learning framework
- **transformers** (>=4.45.0) - Model and tokenizer utilities
- **pillow** (>=10.0.0) - Image processing
- **requests** (>=2.31.0) - HTTP client

Installation time: ~5-10 minutes depending on internet speed.

## Step 3: Download Model

Download the Qwen3-VL-4B-Instruct-FP8 model from HuggingFace:

```bash
python download_model.py
```

**What this does:**
- Downloads model files from HuggingFace (~4.5GB)
- Stores in HuggingFace cache (`~/.cache/huggingface/hub/`)
- Verifies GPU and CUDA configuration
- Prints download location

**Expected output:**
```
Downloading model: Qwen/Qwen3-VL-4B-Instruct-FP8
GPU: NVIDIA GeForce RTX 5060
CUDA version: 12.8
HuggingFace cache: /root/.cache/huggingface

Downloading model (this may take several minutes)...
✓ Model downloaded successfully!

Model info:
  Model ID: Qwen/Qwen3-VL-4B-Instruct-FP8
  Local path: /root/.cache/huggingface/hub/models--Qwen--Qwen3-VL-4B-Instruct-FP8/...
  Cache location: /root/.cache/huggingface

You can now use this model with vLLM:
  vllm serve Qwen/Qwen3-VL-4B-Instruct-FP8 --gpu-memory-utilization 0.85 --load-format auto
```

**Time:** 5-10 minutes (depends on network speed)

**Troubleshooting:**
- If download is slow, check internet connection
- Model must be downloaded only once; it's cached locally
- Free up at least 5GB disk space for the model

## Step 4: Test Model Loading

Before starting the server, verify the model loads correctly:

```bash
python test_inference.py
```

**What this does:**
- Loads model into GPU memory
- Verifies FP8 quantization loading
- Reports memory usage
- Tests basic functionality

**Expected output:**
```
============================================================
Qwen3-VL-4B Inference Test
============================================================

System Information:
  Device: cuda
  GPU: NVIDIA GeForce RTX 5060
  CUDA: 12.8
  Available VRAM: 8.0 GB

Loading model: Qwen/Qwen3-VL-4B-Instruct-FP8
This may take a minute on first load...
✓ Model loaded successfully

Memory Usage (after model load):
  Allocated: 4.25 GB
  Reserved: 4.50 GB

Next steps:
1. Install vLLM: pip install vllm
2. Start the vLLM server:
   vllm serve Qwen/Qwen3-VL-4B-Instruct-FP8 \
     --gpu-memory-utilization 0.85 \
     --load-format auto \
     --port 8000

3. Test with client.py script
```

**Time:** 2-5 minutes (first load is slower)

## Step 5: Start the vLLM API Server

In a dedicated terminal (recommended to use tmux or screen):

```bash
python start_server.py
```

**What this does:**
- Launches vLLM inference server
- Loads model with optimized VRAM settings
- Starts HTTP API on `http://localhost:8000`
- Displays server status

**Expected output:**
```
======================================================================
Qwen3-VL-4B-Instruct-FP8 vLLM Server
======================================================================

Model: Qwen/Qwen3-VL-4B-Instruct-FP8
Port: 8000
GPU Memory Utilization: 85%
Max Model Length: 4096 tokens

Starting server...

Once the server is running, you can test it with:
  curl http://localhost:8000/v1/models

Or use the client.py script for image inference.

Press Ctrl+C to stop the server.
----------------------------------------------------------------------

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Important Notes:**
- Keep this terminal open while using the model
- Server takes ~1-2 minutes to fully load on first start
- GPU memory usage will increase to ~5-6GB after model loads

**Verify Server is Running:**
```bash
# In another terminal
curl http://localhost:8000/v1/models
```

Should return:
```json
{
  "object": "list",
  "data": [
    {
      "id": "Qwen/Qwen3-VL-4B-Instruct-FP8",
      "object": "model",
      "created": ...,
      "owned_by": "vllm"
    }
  ]
}
```

## Step 6: Use the Model

### Option A: Python Client

In another terminal:

```python
from client import Qwen3VLClient

client = Qwen3VLClient()

# Image captioning
caption = client.caption_image("path/to/image.jpg")
print(caption)

# Visual question answering
answer = client.answer_question("path/to/image.jpg", "What is in this image?")
print(answer)

# Scene analysis
analysis = client.analyze_scene("path/to/image.jpg")
print(analysis)
```

### Option B: Command-Line Examples

```bash
# Image captioning
python examples/caption_image.py /path/to/image.jpg

# Visual question answering
python examples/vqa.py /path/to/image.jpg "What is the main object?"

# Scene analysis
python examples/analyze_scene.py /path/to/image.jpg
```

### Option C: Direct API Calls

```bash
# List models
curl http://localhost:8000/v1/models

# Chat completion (requires base64-encoded image)
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen3-VL-4B-Instruct-FP8",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "image", "image": "<base64-encoded-image>"},
          {"type": "text", "text": "What is in this image?"}
        ]
      }
    ],
    "temperature": 0.7,
    "max_tokens": 512
  }'
```

## Performance Expectations

### Memory Usage
- Model weights: ~3.5-4GB (FP8)
- KV cache: ~0.5-1.5GB (varies with input)
- OS/PyTorch overhead: ~0.5-1GB
- **Total**: ~4.5-6.5GB (safe on 8GB VRAM)

### Inference Speed (RTX 5060)
- Simple queries: 10-15 seconds
- Complex analysis: 20-30 seconds
- Batch processing: scales with image complexity

### VRAM Monitoring

Monitor VRAM during inference:
```bash
# In another terminal
watch -n 1 nvidia-smi
```

Expected pattern:
```
Before server start:  ~1-2GB used
After model load:     ~4.5GB used
During inference:     ~5-6.5GB peak
```

## Troubleshooting

### Issue: "No available memory for the cache blocks" or Negative KV Cache Memory

This error appears as:
```
Available KV cache memory: -3.79 GiB
ValueError: No available memory for the cache blocks.
Try increasing `gpu_memory_utilization` when initializing the engine.
```

**Root Cause:**
- GPU memory is over-allocated
- Not enough VRAM left for KV cache after model + overhead

**Solutions (in order):**
1. **Reduce max-model-len** (Recommended):
   ```python
   "--max-model-len", "2048",  # Reduce from 4096
   ```
   This reduces KV cache requirement by ~50%

2. **Reduce gpu-memory-utilization**:
   ```python
   "--gpu-memory-utilization", "0.70",  # Reduce from 0.80
   ```

3. **Combine both** (Best for 8GB VRAM):
   ```python
   "--gpu-memory-utilization", "0.70",
   "--max-model-len", "2048",
   ```

4. **Add --enforce-eager flag** (Last resort):
   ```python
   "--enforce-eager",  # Disable CUDA graphs (slightly slower)
   ```

5. **Close other GPU processes**:
   ```bash
   nvidia-smi  # Check for other apps using GPU
   ```

**Why this happens on WSL2:**
- WSL2 has additional memory overhead compared to native Linux
- Vision models are larger than text-only models
- 8GB VRAM is tight for 4B parameter models
- This is expected behavior, not a system error

### Issue: "CUDA out of memory"

**Solutions:**
1. Reduce `--max-model-len` in `start_server.py`:
   ```python
   "--max-model-len", "2048",  # Instead of 4096
   ```

2. Reduce `--gpu-memory-utilization`:
   ```python
   "--gpu-memory-utilization", "0.70",  # Instead of 0.80
   ```

3. Close other GPU-consuming applications
4. Reduce image resolution in client

### Issue: "Connection refused"

**Solutions:**
1. Verify server is running:
   ```bash
   curl http://localhost:8000/v1/models
   ```

2. Check if port 8000 is available:
   ```bash
   lsof -i :8000
   ```

3. Start server in correct directory:
   ```bash
   cd vl && python start_server.py
   ```

### Issue: Slow inference

**Solutions:**
1. First inference is slower (model warming up) - subsequent requests are faster
2. Reduce image resolution:
   ```python
   from PIL import Image
   img = Image.open("image.jpg")
   img.thumbnail((512, 512))  # Resize before sending
   ```

3. Check system resources:
   ```bash
   top  # Check CPU usage
   nvidia-smi  # Check GPU utilization
   ```

### Issue: Model takes long to load

**Reasons:**
- First load is slower as model is transferred to VRAM
- FP8 format requires loading and conversion
- Normal behavior - usually takes 1-2 minutes on first start

**Solutions:**
- Keep server running between requests
- Pre-warm with a simple test image
- Be patient on first load

## Advanced Configuration

### Custom VRAM Settings

Edit `start_server.py`:

```python
# For more aggressive memory usage (faster but riskier)
"--gpu-memory-utilization", "0.95",  # Max out VRAM

# For conservative memory usage (slower but safer)
"--gpu-memory-utilization", "0.70",  # Save more VRAM for other apps
```

### Custom Model Cache Location

```bash
# Set custom cache directory
export HF_HOME=/path/to/custom/cache

# Run download script
python download_model.py
```

### Batch Processing

```python
from client import Qwen3VLClient

client = Qwen3VLClient()

images = [
    "image1.jpg",
    "image2.jpg",
    "image3.jpg",
]

for img_path in images:
    caption = client.caption_image(img_path)
    print(f"{img_path}: {caption}")
```

## Production Deployment

For production use:

1. **Use systemd service** to auto-start server
2. **Setup reverse proxy** (nginx) for load balancing
3. **Add authentication** if exposed to network
4. **Monitor logs** for errors
5. **Setup health checks** for server availability
6. **Use process manager** (supervisor) for reliability

Example supervisor config:
```ini
[program:vllm-server]
directory=/root/code/deploy_models/vl
command=python start_server.py
autostart=true
autorestart=true
stderr_logfile=/var/log/vllm.err.log
stdout_logfile=/var/log/vllm.out.log
```

## Summary

| Step | Command | Time |
|------|---------|------|
| 1. Setup GPU | `nvidia-smi` | <1 min |
| 2. Install deps | `pip install -r requirements.txt` | 5-10 min |
| 3. Download model | `python download_model.py` | 5-10 min |
| 4. Test load | `python test_inference.py` | 2-5 min |
| 5. Start server | `python start_server.py` | 1-2 min |
| 6. Use model | `python examples/caption_image.py image.jpg` | <1 min |

**Total initial setup: ~15-30 minutes**

After initial setup, subsequent runs are much faster.
