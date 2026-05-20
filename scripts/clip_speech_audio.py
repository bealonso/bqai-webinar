#!/usr/bin/env python3
"""
Clip a speech audio file to match a specific target line/phrase.
Uses a high-reliability architecture:
1. Transcodes the local input audio to a temporary mono 16kHz WAV file.
2. Uploads the WAV file to GCS and transcribes it with LINEAR16 config.
3. Word timestamps are aligned against the target phrase.
4. High-precision clipping is performed on the original input audio using ffmpeg.
"""

import os
import sys
import argparse
import subprocess
from google.cloud import storage
from google.cloud import speech

def get_ffmpeg_path():
    """Acquire the static ffmpeg binary path from imageio-ffmpeg library."""
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        print("[ERROR] imageio-ffmpeg library is not installed. Please install it using:")
        print("  python3 -m pip install imageio-ffmpeg")
        sys.exit(1)

def transcode_to_mono_wav(ffmpeg_path, input_path, wav_path):
    """Transcode input audio to a standard mono 16kHz WAV file for optimal speech recognition."""
    print(f"-> Transcoding input to standard mono 16kHz WAV: {wav_path}...")
    try:
        cmd = [
            ffmpeg_path, "-y",
            "-i", input_path,
            "-ac", "1",
            "-ar", "16000",
            wav_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("[SUCCESS] WAV transcoding finished.")
    except Exception as e:
        print(f"[ERROR] Transcoding to WAV failed: {e}")
        sys.exit(1)

def upload_to_gcs(local_path, bucket_name, gcs_path):
    """Uploads a local file to a GCS bucket."""
    print(f"-> Uploading {local_path} to gs://{bucket_name}/{gcs_path}...")
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        if not bucket.exists():
            bucket = client.create_bucket(bucket_name)
        blob = bucket.blob(gcs_path)
        blob.upload_from_filename(local_path)
        return f"gs://{bucket_name}/{gcs_path}"
    except Exception as e:
        print(f"[ERROR] Failed to upload file to GCS: {e}")
        sys.exit(1)

def delete_from_gcs(bucket_name, gcs_path):
    """Deletes a file from a GCS bucket."""
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(gcs_path)
        if blob.exists():
            blob.delete()
            print(f"-> Cleaned up GCS scratch file: gs://{bucket_name}/{gcs_path}")
    except Exception as e:
        print(f"[WARNING] Failed to clean up GCS scratch file: {e}")

def transcribe_audio(gcs_uri):
    """Transcribe WAV audio from GCS using Speech-to-Text with word timestamps."""
    print("-> Contacting Speech-to-Text API...")
    try:
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(uri=gcs_uri)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_word_time_offsets=True,
        )
        
        operation = client.long_running_recognize(config=config, audio=audio)
        print("-> Waiting for transcription operation to complete (this can take a few minutes)...")
        response = operation.result(timeout=600)
        print("[SUCCESS] Transcription finished.")
        return response
    except Exception as e:
        print(f"[ERROR] Speech-to-Text transcription failed: {e}")
        sys.exit(1)

def find_timestamp_alignment(response, target_phrase):
    """Find the best word-level alignment for the target phrase in the transcript."""
    words_list = []
    for result in response.results:
        alternative = result.alternatives[0]
        for word_info in alternative.words:
            # Clean word by removing punctuation and converting to lowercase
            clean_w = "".join(c for c in word_info.word.lower() if c.isalnum())
            
            # Safe timestamp parsing (compatible with both timedelta and protobuf Duration)
            if hasattr(word_info.start_time, "total_seconds"):
                start_sec = word_info.start_time.total_seconds()
                end_sec = word_info.end_time.total_seconds()
            else:
                start_sec = word_info.start_time.seconds + word_info.start_time.nanos / 1e9
                end_sec = word_info.end_time.seconds + word_info.end_time.nanos / 1e9
                
            words_list.append((clean_w, start_sec, end_sec, word_info.word))

    target_words = target_phrase.split()
    target_clean = ["".join(c for c in w.lower() if c.isalnum()) for w in target_words]
    n_target = len(target_clean)

    if not words_list:
        print("[ERROR] No words transcribed in audio.")
        return None

    best_match = None
    best_score = 0

    # Align the target words window over the transcribed words list
    for i in range(len(words_list) - n_target + 1):
        score = 0
        for j in range(n_target):
            if words_list[i + j][0] == target_clean[j]:
                score += 1
        if score > best_score:
            best_score = score
            best_match = (i, i + n_target - 1)

    # Require at least 50% match rate to prevent arbitrary alignment
    if best_match and best_score > n_target * 0.5:
        start_idx, end_idx = best_match
        start_time = words_list[start_idx][1]
        end_time = words_list[end_idx][2]
        matched_text = " ".join(w[3] for w in words_list[start_idx:end_idx+1])
        print(f"\n[ALIGNMENT MATCHED (Score: {best_score}/{n_target})]")
        print(f"  Text excerpt: \"{matched_text}\"")
        print(f"  Aligned Timestamps: {start_time:.2f}s to {end_time:.2f}s")
        return start_time, end_time
    else:
        print("[ERROR] Could not find a reliable alignment for target phrase in audio.")
        return None

def clip_audio(ffmpeg_path, input_path, output_path, start_time, end_time):
    """Clip the audio file between start_time and end_time using ffmpeg."""
    print(f"-> Clipping audio: {start_time:.2f}s to {end_time:.2f}s -> {output_path}...")
    try:
        cmd = [
            ffmpeg_path, "-y",
            "-ss", str(start_time),
            "-to", str(end_time),
            "-i", input_path,
            "-c:a", "libmp3lame",
            "-q:a", "2",
            output_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[SUCCESS] Saved clipped speech asset to: {output_path}")
    except Exception as e:
        print(f"[ERROR] Clipping failed: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Clip speech audio to match a specific target phrase.")
    parser.add_argument("--input", required=True, help="Path to the local source audio file.")
    parser.add_argument("--line", required=True, help="The target sentence to search and clip.")
    parser.add_argument("--output", required=True, help="Destination path for the clipped audio output.")
    parser.add_argument("--bucket", required=True, help="GCS bucket name for Speech-to-Text scratch upload.")
    
    args = parser.parse_args()

    # 1. Verify inputs
    if not os.path.exists(args.input):
        print(f"[ERROR] Source audio file not found at: {args.input}")
        sys.exit(1)

    # 2. Get ffmpeg path
    ffmpeg_path = get_ffmpeg_path()

    # 3. Transcode to standard mono 16kHz WAV locally
    temp_wav = f"{args.input}.temp.wav"
    transcode_to_mono_wav(ffmpeg_path, args.input, temp_wav)

    # 4. Upload WAV to GCS
    gcs_filename = f"temp_clip_source/{os.path.basename(temp_wav)}"
    gcs_uri = upload_to_gcs(temp_wav, args.bucket, gcs_filename)

    # 5. Transcribe & align
    try:
        response = transcribe_audio(gcs_uri)
        timestamps = find_timestamp_alignment(response, args.line)
    finally:
        # Clean up GCS and local scratch files immediately to prevent workspace clutter
        if os.path.exists(temp_wav):
            os.remove(temp_wav)
            print("-> Cleaned up local WAV scratch file.")
        delete_from_gcs(args.bucket, gcs_filename)

    if not timestamps:
        sys.exit(1)

    start_time, end_time = timestamps

    # 6. Perform precision clipping on the ORIGINAL input file
    clip_audio(ffmpeg_path, args.input, args.output, start_time, end_time)

if __name__ == "__main__":
    main()
