這個版本已包含
✅ 1. 影片下載
支援 m3u8 / mp4
yt-dlp 自動抓取
✅ 2. 影片資訊
長度
檔案大小
✅ 3. 自動壓縮
FFmpeg 1280p
CRF 30（NotebookLM 專用）
✅ 4. RTX 5060 GPU 逐字稿
faster-whisper
CUDA 加速
✅ 5. TXT 自動切割
每 8000 字分段
適合 NotebookLM 上傳

一鍵打包 EXE

進入資料夾後執行：

pip install -r requirements.txt

再執行：

pyinstaller --onefile --windowed main.py

輸出在：

dist/main.exe

