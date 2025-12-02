import os
import sys
from faster_whisper import WhisperModel

print("Using faster-whisper version:", os.popen("pip show faster-whisper | grep Version").read().strip())
model = WhisperModel("medium", device="cuda")
from pathlib import Path
current_path = Path(__file__).resolve()
PROJECT_ROOT = current_path.parent.parent.parent

audio_path = PROJECT_ROOT/"1.m4a"
if not os.path.exists(audio_path):
    sys.exit("Audio file not found: " + str(audio_path))
print("Transcribing audio file:", audio_path)
segments, info = model.transcribe(str(audio_path))
for segment in segments:
    print(segment.start, segment.end, segment.text)
