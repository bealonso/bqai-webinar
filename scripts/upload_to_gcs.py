#!/usr/bin/env python3
"""
Upload local media assets to Google Cloud Storage (GCS).
Synchronizes the downloaded media files with GCS paths to be referenced
as ObjectRef or URIs in BigQuery ML/AI queries.
"""

import os
import argparse
from google.cloud import storage

def upload_folder_to_gcs(local_dir, bucket_name, gcs_prefix=""):
    """
    Recursively uploads all files inside local_dir to a specified GCS bucket prefix.
    """
    try:
        storage_client = storage.Client()
    except Exception as e:
        print(f"[ERROR] Failed to initialize Google Cloud Storage client: {e}")
        print("Ensure you are logged in via 'gcloud auth application-default login'")
        return

    try:
        bucket = storage_client.lookup_bucket(bucket_name)
        if not bucket:
            print(f"[INFO] Bucket '{bucket_name}' not found. Attempting to create it...")
            bucket = storage_client.create_bucket(bucket_name)
            print(f"[SUCCESS] Created bucket: {bucket_name}")
    except Exception as e:
        print(f"[ERROR] Failed to find or create bucket '{bucket_name}': {e}")
        return

    print(f"Synchronizing {local_dir} to gs://{bucket_name}/{gcs_prefix} ...\n")
    
    uploaded_count = 0
    for root, _, files in os.walk(local_dir):
        for file in files:
            # Sync all standard media formats
            if not file.lower().endswith(('.mp3', '.mp4', '.jpg', '.jpeg', '.png', '.webp', '.ogg', '.wav')):
                continue
                
            local_path = os.path.join(root, file)
            
            # Compute GCS destination path relative to the local directory
            relative_path = os.path.relpath(local_path, local_dir)
            gcs_path = os.path.join(gcs_prefix, relative_path).replace("\\", "/")
            
            print(f"-> Uploading {relative_path} to gs://{bucket_name}/{gcs_path}...")
            try:
                blob = bucket.blob(gcs_path)
                blob.upload_from_filename(local_path)
                uploaded_count += 1
            except Exception as upload_error:
                print(f"   [FAILED] {relative_path}: {upload_error}")

    print(f"\n[COMPLETE] Finished uploading {uploaded_count} files to GCS.")

def main():
    parser = argparse.ArgumentParser(description="Upload media assets to GCS for Omniscience Media Archive.")
    parser.add_argument(
        "--bucket", 
        type=str, 
        required=True,
        help="The name of the GCS bucket (e.g. 'my-media-archive-bucket')"
    )
    parser.add_argument(
        "--prefix", 
        type=str, 
        default="media_archive",
        help="GCS directory prefix under which assets are uploaded (default: 'media_archive')"
    )
    
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_media_dir = os.path.join(base_dir, "media_assets")

    if not os.path.exists(local_media_dir) or not os.listdir(local_media_dir):
        print(f"[WARNING] Local media directory '{local_media_dir}' is empty or missing.")
        print("Please run 'download_assets.py' first to acquire the demo media files.")
        return

    upload_folder_to_gcs(local_media_dir, args.bucket, args.prefix)

if __name__ == "__main__":
    main()
