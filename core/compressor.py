import shutil
import subprocess
import os
import sys


def _ffmpeg_cmd():
    """
    決定使用哪一個 ffmpeg：
    - 若是打包後的 exe，優先使用 core/ffmpeg/ffmpeg.exe
    - 否則使用系統 PATH 裡的 ffmpeg
    """
    if getattr(sys, "frozen", False):
        base_dir = sys._MEIPASS  # pyinstaller 解壓目錄
    else:
        base_dir = os.path.dirname(__file__)

    ffmpeg_path = os.path.join(base_dir, "ffmpeg", "ffmpeg.exe")
    if os.path.exists(ffmpeg_path):
        return ffmpeg_path
    return "ffmpeg"


def _ensure_ffmpeg():
    """
    確認 ffmpeg 存在：
    - 系統 PATH 有 ffmpeg，或
    - core/ffmpeg/ffmpeg.exe 存在
    """
    has_system_ffmpeg = shutil.which("ffmpeg") is not None
    has_local_ffmpeg = os.path.exists(
        os.path.join(os.path.dirname(__file__), "ffmpeg", "ffmpeg.exe")
    )
    if not (has_system_ffmpeg or has_local_ffmpeg):
        raise RuntimeError(
            "找不到 ffmpeg，請先安裝或放入 PATH，"
            "或將 ffmpeg.exe 放在 core/ffmpeg/ 底下。"
        )


def compress_video(input_path, output_path, mode="notebooklm"):
    """
    影片壓縮工具

    參數:
        input_path : str 或 Path
        output_path: str 或 Path
        mode:
            - notebooklm: 1280p, CRF 30
            - high      : 1080p, CRF 23
            - medium    : 720p,  CRF 28
            - bitrate   : 固定視訊碼率 1500k
    """
    _ensure_ffmpeg()
    ffmpeg = _ffmpeg_cmd()

    input_path = str(input_path)
    output_path = str(output_path)

    print(f"[compress_video] mode={mode}")
    print(f"[compress_video] input={input_path}")
    print(f"[compress_video] output={output_path}")

    if mode == "notebooklm":
        cmd = [
            ffmpeg, "-y",
            "-i", input_path,
            "-vf", "scale=1280:-1",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "30",
            "-c:a", "aac",
            "-b:a", "128k",
            output_path,
        ]

    elif mode == "high":
        cmd = [
            ffmpeg, "-y",
            "-i", input_path,
            "-vf", "scale='min(1920,iw)':-2",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "160k",
            output_path,
        ]

    elif mode == "medium":
        cmd = [
            ffmpeg, "-y",
            "-i", input_path,
            "-vf", "scale='min(1280,iw)':-2",
            "-c:v", "libx264",
            "-preset", "faster",
            "-crf", "28",
            "-c:a", "aac",
            "-b:a", "128k",
            output_path,
        ]

    elif mode == "bitrate":
        cmd = [
            ffmpeg, "-y",
            "-i", input_path,
            "-c:v", "libx264",
            "-b:v", "1500k",
            "-c:a", "aac",
            "-b:a", "128k",
            output_path,
        ]
    else:
        raise ValueError(f"Unknown compress mode: {mode}")

    print(f"[compress_video] cmd={' '.join(cmd)}")

    # 把 ffmpeg 的輸出抓出來，方便 debug
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,            # 改成二進位模式
    )

    # 以 UTF-8 嘗試解碼，遇到不支援的字節就忽略
    stdout_text = result.stdout.decode("utf-8", errors="ignore") if result.stdout else ""
    stderr_text = result.stderr.decode("utf-8", errors="ignore") if result.stderr else ""

    print("[compress_video] ffmpeg stdout:", stdout_text)
    print("[compress_video] ffmpeg stderr:", stderr_text)

    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg 執行失敗，returncode={result.returncode}")