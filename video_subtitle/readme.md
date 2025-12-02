
pip install yt-dlp

yt-dlp -x --audio-format mp3 "https://www.bilibili.com/video/BV1r54y1L7R3"

yt-dlp "https://www.bilibili.com/video/BV1r54y1L7R3"

whisper 1.m4a --model large-v3 --output_format srt --language Chinese
whisper 1.m4a --model medium --output_format srt --language Chinese