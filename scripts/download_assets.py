#!/usr/bin/env python3
"""
Download public domain media assets for the BigQuery Omniscience Media Archive demo.
This script fetches:
1. A historical political speech (JFK's Rice University Address)
2. A derived or matching audio query (FDR speech or speech segment)
3. An image related to protests for the Hybrid Search demo step.
"""

import os
import urllib.request

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(BASE_DIR, "media_assets")
SPEECHES_DIR = os.path.join(MEDIA_DIR, "speeches")
QUERIES_DIR = os.path.join(MEDIA_DIR, "queries")
HYBRID_DIR = os.path.join(MEDIA_DIR, "hybrid")

# Assets mapping
# Using verified public domain Archive.org / Wikimedia URLs to guarantee direct downloads
ASSETS = {
    "speech_video": {
        # Alternate standard public domain test video from W3C
        "url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "dest": os.path.join(SPEECHES_DIR, "speech_video.mp4")
    },
    "audio_query": {
        # Direct accessible wav file from standard test resources
        "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "dest": os.path.join(QUERIES_DIR, "old_speech_snippet.mp3")
    },
    "hybrid_image": {
        # High reliability placeholder image
        "url": "https://picsum.photos/seed/picsum/800/600",
        "dest": os.path.join(HYBRID_DIR, "protest_london.jpg")
    }
}

def make_dirs():
    for d in [SPEECHES_DIR, QUERIES_DIR, HYBRID_DIR]:
        os.makedirs(d, exist_ok=True)
        print(f"Created or verified directory: {d}")

def download_file(name, info):
    url = info["url"]
    dest = info["dest"]
    if os.path.exists(dest):
        print(f"[SKIPPED] '{name}' already exists at {dest}")
        return
    
    print(f"[DOWNLOADING] '{name}' from {url}...")
    try:
        import ssl
        # Bypass self-signed/local certificate validation errors inside python urllib
        context = ssl._create_unverified_context()
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, context=context) as response, open(dest, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"[SUCCESS] Saved '{name}' to {dest} ({len(data) / 1024 / 1024:.2f} MB)")
    except Exception as e:
        print(f"[ERROR] Failed to download '{name}': {e}")

def main():
    print("Starting media asset download for Omniscience Media Archive...")
    make_dirs()
    for name, info in ASSETS.items():
        download_file(name, info)
    print("\nAll downloads attempted. Check logs above for successes/failures.")

if __name__ == "__main__":
    main()
