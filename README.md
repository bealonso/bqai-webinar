# BigQuery Omniscience Media Archive: Multimodal AI & Vector Search

Welcome to the **BigQuery Omniscience Media Archive** project repository! This repository contains a premium, high-fidelity demonstration of BigQuery's advanced **Multimodal AI** and **Vector Search** capabilities.

It showcases how to ingest unstructured historical media, autonomously maintain and generate high-dimensional vectors inside standard tables, and query them using cross-modal (text, audio) and unified hybrid (image + text) queries.

---

## 🚀 Key Technical Showcases

1. 🤖 **Autonomous Embedding Generation (`AI.EMBED`):** Harnesses BigQuery's native generated columns to automatically, asynchronously, and autonomously maintain 3072-dimensional multimodal embeddings in the background as new files are uploaded.
2. 📁 **GCS Object Tables Sync:** Integrates external GCS Object Tables (`assets_metadata`) to dynamically discover objects and synchronize them with standard tables.
3. 🔍 **Cross-Modal Semantic Discovery:** Executes standard `VECTOR_SEARCH` similarity queries on video files using natural language text descriptions and clipped speech audio snippets.
4. 🎯 **Precision Hybrid Search:** Combines visual location context (using U.S. Capitol photos) with textual keyword filtering (`SEARCH`) to isolate exact matches (JFK's Inaugural Address).

---

## 🛠️ Repository Structure

```directory
bqai-webinar/
├── bqai_multimodal_media_archive.ipynb  # Full interactive & parameterized Jupyter Notebook
├── walkthrough.md                       # Comprehensive step-by-step presentation guide
├── scripts/
│   ├── clip_speech_audio.py             # Precision speech alignment & clipping CLI tool
│   ├── upload_to_gcs.py                 # Local media sync to Cloud Storage bucket
│   ├── build_iconic_speeches.py         # Video asset downloader
│   ├── download_assets.py               # Supporting assets downloader
│   └── generate_audio_query.py          # Supporting TTS audio generator
├── sql/
│   ├── 01_setup.sql                     # base model, tables, and sync creation queries
│   ├── 02_cross_modal.sql               # text and audio vector search queries
│   └── 03_hybrid_search.sql             # Capital image + keyword search query
└── .gitignore                           # Workspace ignore filters
```

---

## 📁 Included Media Assets

| Asset Folder | Description |
| :--- | :--- |
| `/media_assets/speeches/` | **10 Speeches Videos:** Verified public-domain speech recordings (MLK, JFK, Reagan, FDR, Nixon, Eisenhower, RFK). |
| `/media_assets/queries/` | **3 Clipped Audios:** Aligned audio snippets of the exact featured lines of MLK, Reagan, and JFK speeches, created using our custom STT alignment tool. |
| `/media_assets/hybrid/` | **2 Capitol Images:** U.S. Capitol travel sight-seeing perspective (`capitol-dc.png`) and Capitol protest scene (`protest.png`). |

---

## 📖 How to Run the Demo

### 1. Run with the Parameterized Notebook (Recommended)
Open the [bqai_multimodal_media_archive.ipynb](bqai_multimodal_media_archive.ipynb) in VS Code, Vertex AI Workbench, or Google Colab. 
Set your variables in the configuration cell:
```python
PROJECT_ID = "your-project-id"
DATASET_ID = "your_dataset_id"
BUCKET_NAME = "your-bucket-name"
CONNECTION_ID = f"{PROJECT_ID}.us.your-connection-id"
```
You can then run the entire demo end-to-end with zero manual replacements!

### 2. Follow the Interactive Presentation Guide
Open the [walkthrough.md](walkthrough.md) file. It contains a complete presentation rundown, including architecture flow diagrams, GCS asset tables, and verified SQL queries designed to be executed directly in the BigQuery Studio console.

---

## ⚙️ Asset Auto-Clipper Tool

To clip any speech audio file to match a specific target line/phrase dynamically:
```bash
python3 scripts/clip_speech_audio.py \
  --input media_assets/queries/2-Reagan-Wall.mp3 \
  --line "Mr. Gorbachev open this gate Mr. Gorbachev tear down this wall" \
  --output media_assets/queries/2-Reagan-Wall_clipped.mp3 \
  --bucket your-bucket-name
```
*(This script transcodes the file into a standard 16kHz mono WAV, uploads it to GCS, transcribes it with word timestamps, matches your phrase, and precision-clips the original MP3 using static ffmpeg).*
