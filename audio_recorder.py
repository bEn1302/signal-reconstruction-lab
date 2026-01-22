"""
Doc: https://people.csail.mit.edu/hubert/pyaudio/
"""

import wave
import sys
import time

import pyaudio

# Konfiguration
CHUNK = 1024  # Buffer-Größe
FORMAT = pyaudio.paInt16  # Audioformat (16-bit)
CHANNELS = 1 if sys.platform == "darwin" else 2  # Mono wenn MacOS sonst Stereo
RATE = 44100  # Abtastrate (CD-Qualität)
RECORD_SECONDS = 5  # Dauer der Aufnahme
OUTPUT_FILENAME = "eigene_aufnahme.wav"


def record_audio():
    print("Aufnahme startet in:")
    for i in range(3, 0, -1):
        print(f"{i}")
        time.sleep(1)
    print("Jetzt!")

    with wave.open(OUTPUT_FILENAME, "wb") as wf:
        p = pyaudio.PyAudio()
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )

        print("Recording...")
        for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
            wf.writeframes(stream.read(CHUNK))
        print("Done")

        stream.close()
        p.terminate()
