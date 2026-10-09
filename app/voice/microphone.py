
from pathlib import Path

import sounddevice as sd
from scipy.io.wavfile import write


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_RATE = 16000
DEFAULT_DURATION = 5


def record_audio(
    duration: int = DEFAULT_DURATION,
    output_path: str | Path | None = None,
) -> Path:
    """Record audio from the default microphone and save it as WAV."""

    if duration <= 0:
        raise ValueError("Duration must be greater than zero.")

    if output_path is None:
        output_file = PROJECT_ROOT / "samples" / "microphone_input.wav"
    else:
        output_file = Path(output_path).expanduser().resolve()

    output_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"Recording for {duration} seconds. Speak now!")

    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
    )
    sd.wait()

    write(str(output_file), SAMPLE_RATE, audio)

    print(f"Audio saved to: {output_file}")
    return output_file


def main():
    """Run microphone recording as a standalone program."""

    try:
        duration = int(input("Enter recording duration in seconds: "))
        input("Press Enter to start recording...")

        record_audio(duration)

    except (ValueError, sd.PortAudioError) as error:
        print(f"Recording error: {error}")


if __name__ == "__main__":
    main()
