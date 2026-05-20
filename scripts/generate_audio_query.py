#!/usr/bin/env python3
"""
Generate custom speech audio query clips using Google Cloud Text-to-Speech.
This acts as a fallback or custom generation tool if public domain speech snippets
do not meet the specific audio-to-video demo needs.
"""

import os
import argparse

def generate_tts_audio(text, output_path, voice_name="en-US-Neural2-J"):
    """
    Synthesizes speech from the input text and saves it as an mp3/wav file.
    """
    try:
        from google.cloud import texttospeech
    except ImportError:
        print("[ERROR] google-cloud-text-to-speech package is not installed.")
        print("Please install it using: pip install google-cloud-text-to-speech")
        return False

    print(f"[SYNTHESIZING] Generating custom audio file: '{text}' -> {output_path}")
    try:
        client = texttospeech.TextToSpeechClient()
        input_text = texttospeech.SynthesisInput(text=text)

        # Build voice request, selecting neural high-quality voice
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name=voice_name
        )

        # Select standard audio encoding
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16 # WAV
        )

        response = client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )

        with open(output_path, "wb") as out:
            out.write(response.audio_content)
            print(f"[SUCCESS] Audio content written to {output_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to synthesize TTS: {e}")
        print("Make sure you have active application default credentials: gcloud auth application-default login")
        return False

def main():
    parser = argparse.ArgumentParser(description="Generate custom demo audio queries using Google Cloud TTS.")
    parser.add_argument(
        "--text", 
        type=str, 
        default="We choose to go to the Moon in this decade and do the other things, not because they are easy, but because they are hard.",
        help="Text transcript to convert into speech audio."
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default=None,
        help="Destination file path. Defaults to media_assets/queries/custom_speech_snippet.wav"
    )
    
    args = parser.parse_args()

    # Compute default path if not provided
    if args.output is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        args.output = os.path.join(base_dir, "media_assets", "queries", "custom_speech_snippet.wav")
        os.makedirs(os.path.dirname(args.output), exist_ok=True)

    generate_tts_audio(args.text, args.output)

if __name__ == "__main__":
    main()
