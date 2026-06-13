
import subprocess
from pathlib import Path

def download_video(url, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "yt-dlp",
        "-o", str(output_dir / "%(title)s.%(ext)s"),
        url
    ]

    subprocess.run(cmd)

    files = list(output_dir.glob("*.mp4"))
    return max(files, key=lambda f: f.stat().st_mtime)
