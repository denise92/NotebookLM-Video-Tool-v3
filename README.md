# NotebookLM Video Tool v3

NotebookLM Video Tool v3 是一個用來下載、壓縮與轉錄影片的桌面工具，特別針對 NotebookLM 的影片摘要流程最佳化。

目前版本已包含：

- ✅ 影片下載：支援 `m3u8 / mp4`，透過 `yt-dlp` 自動抓取來源
- ✅ 影片資訊：顯示長度、檔案大小
- ✅ 自動壓縮：使用 FFmpeg 壓縮為適合 NotebookLM 的設定（多種模式）
- ✅ 逐字稿：使用 faster-whisper 在 CPU 上進行中文轉錄
- ✅ TXT 自動切割：每約 8000 字分段，方便 NotebookLM 上傳
- ✅ GUI：支援輸入網址下載，或直接選擇本機 mp4 影片處理

---

## 功能說明

### 1. 影片來源

工具提供兩種來源方式：

1. **輸入影片網址**
   - 填寫 `Video URL (m3u8/mp4)`。
   - 指定 `Save Folder` 儲存位置。
   - 按「Start (Download / Local)」開始下載與後續流程。

2. **選擇本機影片檔**
   - 按 `Browse Video`，選擇現有的 `mp4`（或其他支援格式）。
   - 不需要填寫 URL。
   - 按「Start (Download / Local)」直接對本機檔案進行壓縮與轉錄。

### 2. 影片資訊

下載或選檔後，會顯示：

- 檔案路徑
- 檔案大小（MB）
- 影片長度（分鐘）

### 3. 壓縮功能（FFmpeg）

勾選「下載/選檔後自動壓縮」即可啟用壓縮，支援四種模式：

- **NotebookLM 預設**：1280p、CRF 30、AAC 128k（適合 NotebookLM 影片摘要）
- **高品質**：最高 1080p、CRF 23，畫質較好、檔案較大
- **中等**：最高 720p、CRF 28，兼顧大小與畫質
- **只改碼率**：不改解析度，固定視訊碼率（例如 1500kbps）

壓縮完成後會顯示：

- 壓縮後檔案路徑
- 壓縮後檔案大小
- 壓縮後影片長度

### 4. 逐字稿（Whisper）

目前使用 **faster-whisper** 的 `small` 模型，在 **CPU** 模式下進行中文轉錄：

- `device="cpu"`
- `compute_type="int8"`
- `language="zh"`，支援繁體中文
- 轉錄結果輸出為 `原影片檔路徑 + ".txt"`

### 5. TXT 自動切割

為了方便 NotebookLM 上傳長文本，工具會將逐字稿 TXT：

- 依固定字數自動切割（例如每約 8000 字一份）
- 產生多個分段 TXT 檔，適合 NotebookLM 一次上傳多個檔案

---

## 安裝與執行

### 1. 建立虛擬環境

```bash
python -m venv .venv
```

啟用虛擬環境（Windows PowerShell）：

```bash
.\.venv\Scripts\Activate.ps1
```

### 2. 安裝依賴

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. 執行 GUI

```bash
python .\main.py
```

---

## 打包為執行檔（可選）

如果要打包成單一 `main.exe`：

```bash
pyinstaller --onefile --windowed main.py
```

輸出會在：

```text
dist\main.exe
```

你可以直接將 `main.exe` 提供給使用者使用（需搭配 ffmpeg 等必要檔案）。

---

## 注意事項

- **ffmpeg**  
  - 工具會優先尋找 `core/ffmpeg/ffmpeg.exe`，找不到時才使用系統 PATH 裡的 `ffmpeg`。
  - 若執行壓縮時出現找不到 ffmpeg 的錯誤，請確認：
    - 已安裝 ffmpeg 並加入 PATH，或
    - 在 `core/ffmpeg/` 放入 `ffmpeg.exe`。

- **Whisper / faster-whisper GPU 模式**  
  - 預設為 CPU 模式，避免 CUDA / `cublas64_12.dll` 安裝問題。
  - 若要啟用 GPU，需自行安裝相容的 CUDA Toolkit 與驅動，並在 `core/whisper_transcriber.py` 中將 `device` 改為 `"cuda"`。

---

## TODO / 未來計畫

- 加入支援多語言字幕輸出（SRT / VTT）
- 可選擇只做下載 + 壓縮、不進行逐字稿
- 增加批次處理多個影片檔的功能