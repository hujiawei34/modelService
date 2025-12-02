# Qwen3-VL Model Deployment

Deploy the Qwen3-VL-4B-Instruct-FP8 model for image recognition and understanding on WSL2 with NVIDIA RTX 5060 (8GB VRAM).

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download Model
```bash
python download_model.py
```

### 3. Start API Server
```bash
python start_server.py
```

The server will start on `http://localhost:8000`

### 4. Use the Client
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

## Examples

See the `examples/` directory for complete example scripts:
- `caption_image.py` - Generate detailed image captions
- `vqa.py` - Ask questions about images
- `analyze_scene.py` - Detailed scene analysis

Example usage:
```bash
python examples/caption_image.py /path/to/image.jpg
python examples/vqa.py /path/to/image.jpg "What is the main object?"
python examples/analyze_scene.py /path/to/image.jpg
```

## Model Information

- **Model**: Qwen3-VL-4B-Instruct-FP8
- **Size**: ~4.5GB (FP8 quantized)
- **VRAM Usage**: 4-5GB
- **Framework**: vLLM
- **Quantization**: FP8 (50% memory savings, negligible quality loss)
- **Capabilities**:
  - Image captioning
  - Visual question answering (VQA)
  - Object detection and localization
  - Scene understanding
  - Text extraction (32 languages)
  - Spatial reasoning
  - Chart/diagram interpretation

## Architecture

```
├── download_model.py      # Download model from HuggingFace
├── start_server.py        # Start vLLM API server
├── client.py              # Python client library
├── test_inference.py      # Verify setup and VRAM usage
├── requirements.txt       # Python dependencies
├── examples/              # Example scripts
│   ├── caption_image.py
│   ├── vqa.py
│   └── analyze_scene.py
└── readme.md
```

## Common Commands

### Download Model
```bash
python download_model.py
```

### Start Server
```bash
python start_server.py
```

### Test Inference
```bash
python test_inference.py
```

### Run Examples
```bash
# Image captioning
python examples/caption_image.py <image_path>

# Visual Q&A
python examples/vqa.py <image_path> "<question>"

# Scene analysis
python examples/analyze_scene.py <image_path>
```

## API Endpoints

The vLLM server provides OpenAI-compatible API endpoints:

- `GET /v1/models` - List available models
- `POST /v1/chat/completions` - Chat completion with images

## Troubleshooting

### VRAM Issues
- Model uses ~4-5GB VRAM after loading
- If out of memory, reduce `--max-model-len` in `start_server.py`
- Monitor with: `watch nvidia-smi`

### Connection Issues
- Ensure server is running: `python start_server.py`
- Check port: `lsof -i :8000`
- Check firewall/network

### Slow Inference
- Normal on RTX 5060 (~5-30 seconds depending on image size)
- Reduce image resolution for faster processing
- Use batching for multiple requests

## For More Information

See `DEPLOYMENT.md` for detailed setup and troubleshooting guide.