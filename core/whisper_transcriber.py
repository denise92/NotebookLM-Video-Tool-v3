
from faster_whisper import WhisperModel
import os

def transcribe_video(video_path):
    model = WhisperModel("small", device="cuda", compute_type="float16")

    segments, _ = model.transcribe(video_path, language="zh")

    txt_path = video_path + ".txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        for s in segments:
            f.write(s.text + "\n")

    return txt_path
