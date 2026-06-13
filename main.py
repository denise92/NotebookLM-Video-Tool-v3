
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from core.downloader import download_video
from core.video_info import get_video_info
from core.compressor import compress_video
from core.whisper_transcriber import transcribe_video
from core.txt_splitter import split_txt

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("NotebookLM Video Tool v3")
        self.root.geometry("700x400")

        self.url_var = tk.StringVar()
        self.path_var = tk.StringVar(value=os.getcwd())

        tk.Label(root, text="Video URL (m3u8/mp4):").pack()
        tk.Entry(root, textvariable=self.url_var, width=80).pack()

        tk.Label(root, text="Save Folder:").pack()
        tk.Entry(root, textvariable=self.path_var, width=80).pack()

        tk.Button(root, text="Select Folder", command=self.select_folder).pack()
        tk.Button(root, text="Download", command=self.start_download).pack()

        self.log = tk.Text(root, height=15)
        self.log.pack(fill="both", expand=True)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)

    def log_print(self, msg):
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)

    def start_download(self):
        threading.Thread(target=self.process).start()

    def process(self):
        url = self.url_var.get()
        folder = self.path_var.get()

        self.log_print("Downloading...")
        video = download_video(url, folder)

        info = get_video_info(video)
        self.log_print(f"Size: {info['size_mb']:.2f} MB")
        self.log_print(f"Duration: {info['duration']/60:.1f} min")

        out = video.replace(".mp4", "_compressed.mp4")

        self.log_print("Compressing...")
        compress_video(video, out)

        self.log_print("Transcribing (Whisper)...")
        txt = transcribe_video(video)

        self.log_print("Splitting text...")
        split_txt(txt)

        self.log_print("DONE")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
