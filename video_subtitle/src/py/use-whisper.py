import os
import sys
import whisper

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
audio_path = os.path.join(PROJECT_ROOT, "1.m4a")

if not os.path.exists(audio_path):
    sys.exit("Audio file not found: " + audio_path)

print("Transcribing audio file:", audio_path)

# Load medium model with CUDA
model = whisper.load_model("medium", device="cuda")

# Transcribe audio
result = model.transcribe(audio_path, language="Chinese")

# Print segments with timing
for segment in result["segments"]:
    print(f"{segment['start']:.2f} {segment['end']:.2f} {segment['text']}")