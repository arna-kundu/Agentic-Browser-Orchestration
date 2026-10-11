import sounddevice as sd
import keyboard
import numpy as np
from pathlib import Path
import soundfile as sf


PROJECT_ROOT = Path(__file__).resolve().parents[2]
#Default Sample rate of my Input Device is 44100
SAMPLE_RATE=44100
recording =[]

def callback(indata, frames, time, status):
    if status:
        print(status)
    recording.append(indata.copy())

def record_audio(output_path=PROJECT_ROOT / "samples" / "microphone_input.wav"):
    #record audio untill the user presses 'q'
    recording.clear()
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32', callback=callback):
        while not keyboard.is_pressed("q"):
            pass

    final_audio=np.concatenate(recording, axis=0)
    sf.write(
       PROJECT_ROOT / "samples" / "microphone_input.wav",
        final_audio,
        SAMPLE_RATE
    )
    print("Saved microphone_input.wav")
    
    return output_path