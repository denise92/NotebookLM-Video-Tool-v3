
import subprocess, json, os

def get_video_info(path):
    cmd = [
        "ffprobe","-v","quiet",
        "-print_format","json",
        "-show_format","-show_streams",
        path
    ]

    out = subprocess.check_output(cmd)
    data = json.loads(out)

    duration = float(data["format"]["duration"])
    size_mb = os.path.getsize(path)/1024/1024

    return {"duration":duration,"size_mb":size_mb}
