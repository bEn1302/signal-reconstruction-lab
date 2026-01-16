import librosa
import soundfile as sf
import numpy as np


"""
Lädt eine Audiodatei und gibt das Signal x und die Abtastrate (Samplerate) zurück
doc: https://librosa.org/doc/latest/generated/librosa.load.html#librosa.load
"""


def load_signal(file_path, duration=None):
    print(f"Lade Datei: {file_path}")
    x, sr = librosa.load(file_path, sr=None, mono=True, duration=duration)
    print(f"--> Die Abtastrate der Original-Datei beträgt {sr} Hz")
    return x, sr


"""
Speichert das Signal als Audiodatei
doc: https://python-soundfile.readthedocs.io/en/0.13.1/#read-write-functions
"""


def save_signal(file_path, x, sr):
    print(f"Speichere Datei: {file_path}")
    sf.write(file_path, x, sr)


"""
Erzeugt die Zeitachse t passend zum Signal
doc: https://numpy.org/doc/stable/reference/generated/numpy.linspace.html
"""


def get_time_axis(x, sr):
    return np.linspace(0, len(x) / sr, len(x))
