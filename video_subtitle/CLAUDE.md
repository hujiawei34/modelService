# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a video subtitle generation project using OpenAI's Whisper model for audio transcription. The project extracts audio from videos and generates subtitles using either the standard Whisper model or the faster-whisper optimization.

## Architecture

- **src/py/**: Python scripts for audio transcription
  - `use-faster-whisper.py`: Main transcription script using the faster-whisper library (GPU-optimized)
  - `test_cuda.py`: Utility to verify CUDA/GPU availability and configuration

## Commands

### Running Audio Transcription
```bash
# Transcribe audio using faster-whisper (GPU-optimized)
python src/py/use-faster-whisper.py

# Verify GPU/CUDA setup
python src/py/test_cuda.py
```

### Downloading Media
```bash
# Install yt-dlp for downloading videos
pip install yt-dlp

# Download audio from video (MP3 format)
yt-dlp -x --audio-format mp3 "https://www.bilibili.com/video/BV1r54y1L7R3"

# Download video
yt-dlp "https://www.bilibili.com/video/BV1r54y1L7R3"
```

### Standard Whisper (CPU/GPU)
```bash
# Transcribe audio and generate SRT subtitles
whisper 1.m4a --model large-v3 --output_format srt --language Chinese
```

## Dependencies

- **faster-whisper**: GPU-optimized Whisper implementation
- **torch**: PyTorch for GPU acceleration
- **yt-dlp**: For downloading videos/audio from various platforms
- **openai-whisper** (optional): Standard Whisper model

## Key Implementation Details

- Audio files are expected in the project root directory (e.g., `1.m4a`)
- The `use-faster-whisper.py` script uses CUDA GPU acceleration and expects a CUDA-capable device
- Audio path is resolved relative to the project root directory via `PROJECT_ROOT`
- Transcription output includes segment timing (start/end) and text content
- Currently configured for Chinese language transcription with the `large-v3` model
