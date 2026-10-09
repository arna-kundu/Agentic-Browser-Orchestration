
import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from app.voice.microphone import record_audio


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

api_key=os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing from .env")


def transcribe_audio(audio_path: str | Path) -> str:
    """Transcribe a WAV or other supported audio file using OpenAI."""

    file_path = Path(audio_path).expanduser().resolve()

    if not file_path.is_file():
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is missing from .env")

    client = OpenAI()

    with file_path.open("rb") as audio_file:
        result = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file,
        )

    return result.text


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe an audio file using OpenAI."
    )
    parser.add_argument(
        "audio",
        nargs="?",
        default=str(PROJECT_ROOT / "samples" / "microphone_input.wav"),
        help="Path to the audio file",
    )
    args = parser.parse_args()

    try:
        
        audio_path = record_audio(
                output_path=PROJECT_ROOT / "samples" / "microphone_input.wav"
            )

            # Transcribe the exact file that was recorded
        transcript = transcribe_audio(audio_path)
        print("\n========== TRANSCRIPT ==========")
        print(transcript)
        print("================================")

    except Exception as error:
        print(f"Transcription error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
