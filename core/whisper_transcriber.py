from faster_whisper import WhisperModel
import os


# 在模組載入時就初始化一次模型，避免每次呼叫都重新載入（會非常慢）
# 強制使用 CPU，避免 cublas64_12.dll / CUDA 問題
model = WhisperModel(
    "small",
    device="cpu",        # 改成 CPU
    compute_type="int8", # CPU 上建議用 int8 或 int8_float32，速度較快、記憶體較省
)


def transcribe_video(video_path: str) -> str:
    """
    直接對影片檔做轉錄（faster-whisper 會自動用 ffmpeg 解音訊）
    :param video_path: 影片檔路徑 (mp4 / m4a / mp3 等)
    :return: 產生的 txt 檔路徑
    """

    # language="zh" 固定中文，有需要也可以改成 None 讓模型自動判斷
    segments, _ = model.transcribe(
        video_path,
        language="zh",
        beam_size=5,        # 可調，越大越精確但越慢
        vad_filter=True,    # 啟用 VAD，略過靜音段落
    )

    txt_path = video_path + ".txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        for s in segments:
            f.write(s.text + "\n")

    return txt_path