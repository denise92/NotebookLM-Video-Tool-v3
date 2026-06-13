import os
import threading
from pathlib import Path

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
        self.root.geometry("700x500")

        self.url_var = tk.StringVar()
        self.path_var = tk.StringVar(value=os.getcwd())

        # 下載區
        tk.Label(root, text="Video URL (m3u8/mp4):").pack()
        tk.Entry(root, textvariable=self.url_var, width=80).pack()

        tk.Label(root, text="Save Folder:").pack()
        tk.Entry(root, textvariable=self.path_var, width=80).pack()
        tk.Button(root, text="Select Folder", command=self.select_folder).pack()

        # ===== 壓縮選項區 =====
        self.enable_compress = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="下載後自動壓縮", variable=self.enable_compress).pack()

        tk.Label(root, text="壓縮模式：").pack()
        self.compress_mode = tk.StringVar(value="notebooklm")
        modes = [
            ("NotebookLM 預設 (1280p / CRF 30)", "notebooklm"),
            ("高品質 (1080p / CRF 23)", "high"),
            ("中等 (720p / CRF 28)", "medium"),
            ("只改碼率，不改解析度", "bitrate"),
        ]
        for text, val in modes:
            tk.Radiobutton(
                root,
                text=text,
                value=val,
                variable=self.compress_mode,
            ).pack(anchor="w")

        # 動作按鈕
        tk.Button(root, text="Download", command=self.start_download).pack()

        # Log 視窗
        self.log = tk.Text(root, height=15)
        self.log.pack(fill="both", expand=True)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)

    def log_print(self, msg: str):
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)

    def start_download(self):
        t = threading.Thread(target=self.process, daemon=True)
        t.start()

    def process(self):
        url = self.url_var.get()
        folder = self.path_var.get()

        if not url:
            self.log_print("請先輸入影片網址")
            return

        self.log_print("Downloading...")
        try:
            video = download_video(url, folder)
            video = Path(video)  # 統一轉成 Path
        except Exception as e:
            self.log_print(f"下載失敗：{e}")
            messagebox.showerror("錯誤", f"下載失敗：{e}")
            return

        # 顯示原始檔資訊
        try:
            info = get_video_info(str(video))
            self.log_print(f"Original file: {video}")
            self.log_print(f"Size: {info['size_mb']:.2f} MB")
            self.log_print(f"Duration: {info['duration']/60:.1f} min")
        except Exception as e:
            self.log_print(f"讀取影片資訊失敗：{e}")
            info = None

        # 預設用下載好的原檔
        target_for_transcribe = video

        # 如果勾選「下載後自動壓縮」，就依 RadioButton 模式壓縮
        if self.enable_compress.get():
            mode = self.compress_mode.get()
            out = video.with_name(f"{video.stem}_{mode}_compressed{video.suffix}")

            self.log_print(f"Compressing... mode={mode}")
            self.log_print(f"Output file: {out}")

            try:
                compress_video(video, out, mode=mode)

                # 顯示壓縮後資訊
                info_new = get_video_info(str(out))
                self.log_print(f"Compressed File: {out}")
                self.log_print(f"Compressed Size: {info_new['size_mb']:.2f} MB")
                self.log_print(
                    f"Compressed Duration: {info_new['duration']/60:.1f} min"
                )

                target_for_transcribe = out
            except Exception as e:
                self.log_print(f"壓縮失敗，將使用原檔進行逐字稿：{e}")
                messagebox.showwarning(
                    "壓縮失敗", f"壓縮失敗，將使用原檔進行逐字稿：{e}"
                )
                target_for_transcribe = video
        else:
            self.log_print("Skip compress（使用原檔）")
            target_for_transcribe = video

        # 逐字稿
        self.log_print("Transcribing (Whisper)...")
        try:
            txt = transcribe_video(str(target_for_transcribe))
        except Exception as e:
            self.log_print(f"逐字稿失敗：{e}")
            messagebox.showerror("錯誤", f"逐字稿失敗：{e}")
            return

        # 切分文字
        self.log_print("Splitting text...")
        try:
            split_txt(txt)
        except Exception as e:
            self.log_print(f"切分文字失敗：{e}")
            messagebox.showerror("錯誤", f"切分文字失敗：{e}")
            return

        self.log_print("DONE")
        messagebox.showinfo("完成", "影片處理完成！")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()