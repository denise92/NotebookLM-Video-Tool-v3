
import subprocess

def compress_video(input_file, output_file):
    cmd = [
        "ffmpeg","-y",
        "-i", input_file,
        "-vf","scale=1280:-2",
        "-c:v","libx264","-crf","30",
        "-c:a","aac","-b:a","64k",
        output_file
    ]
    subprocess.run(cmd)
