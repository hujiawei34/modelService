# Quick Start Guide

Get Qwen3-VL running in 5 minutes!

## Prerequisites
- Python 3.8+ with venv/conda
- NVIDIA GPU with CUDA 12.8+
- 8GB+ VRAM

## Setup (One-time)

```bash
# Navigate to vl directory
cd vl

# Install dependencies (~5 min)
pip install -r requirements.txt

# Download model (~5 min)
python download_model.py
```

## Run (Every time)

### Terminal 1: Start Server
```bash
python start_server.py
```

Wait for message: `Uvicorn running on http://0.0.0.0:8000`

### Terminal 2: Use Model

```bash
# Image captioning
python examples/caption_image.py image.jpg

# Visual Q&A
python examples/vqa.py image.jpg "What is this?"

# Scene analysis
python examples/analyze_scene.py image.jpg
```

## Python Usage

```python
from client import Qwen3VLClient

client = Qwen3VLClient()

# Image captioning
caption = client.caption_image("image.jpg")
print(caption)

# Answer questions
answer = client.answer_question("image.jpg", "What's the main color?")
print(answer)

# Analyze scene
analysis = client.analyze_scene("image.jpg")
print(analysis)
```

## Common Commands

| Task | Command |
|------|---------|
| Install | `pip install -r requirements.txt` |
| Download Model | `python download_model.py` |
| Start Server | `python start_server.py` |
| Test Image | `python examples/caption_image.py test.jpg` |
| Check Server | `curl http://localhost:8000/v1/models` |

## Troubleshooting

**GPU not found?**
```bash
nvidia-smi  # Verify GPU is detected
```

**Can't connect to server?**
- Check server is running in Terminal 1
- Wait 30 seconds for full startup
- Verify with: `curl http://localhost:8000/v1/models`

**Out of memory?**
- Edit `start_server.py`
- Reduce `--gpu-memory-utilization` from 0.85 to 0.75

**First inference is slow?**
- Normal! Model is warming up
- Subsequent requests are faster
- Typical times: 10-30 seconds on RTX 5060

## Next Steps

- Read `readme.md` for full documentation
- See `DEPLOYMENT.md` for detailed setup guide
- Check `examples/` for more examples
- Look at `client.py` for API details

## Support

For issues or questions:
1. Check `DEPLOYMENT.md` Troubleshooting section
2. Monitor GPU with: `nvidia-smi -l 1`
3. Check server logs in Terminal 1
