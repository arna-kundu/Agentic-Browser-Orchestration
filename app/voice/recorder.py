import sounddevice as sd
import keyboard
import numpy as np
import soundfile as sf

#Default Sample rate of my Input Device is 44100
SAMPLE_RATE=44100
recording =[]

def callback(indata, frames, status, time):
    if status:
        print(status)
    recording.append(indata.copy())

def record_audio(output_path=f"../../samples/microphone_input.wav"):
    #record audio untill the user presses 'q'
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32', callback=callback):
        while not keyboard.is_pressed("q"):
            pass

    final_audio=np.concatenate(recording, axis=0)
    sf.write(
        "../../samples/microphone_input.wav",
        final_audio,
        SAMPLE_RATE
    )
    print("Saved microphone_input.wav")