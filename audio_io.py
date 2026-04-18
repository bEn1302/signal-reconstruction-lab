import torchaudio
import torch
import numpy as np

"""
Lädt eine Audiodatei und gibt das Signal x und die Abtastrate (Samplerate) zurück
doc: https://docs.pytorch.org/audio/stable/generated/torchaudio.load.html#torchaudio.load
"""


def load_signal(file_path, duration=None):
    print(f"Lade Datei: {file_path}")

    waveform, sr = torchaudio.load(file_path)

    # Auf Mono heruntermischen falls Stereo
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)

    # Dauer (duration) zuschneiden falls angegeben
    if duration is not None:
        num_frames = int(sr * duration)
        waveform = waveform[:, :num_frames]

    print(f"--> Die Abtastrate der Original-Datei beträgt {sr} Hz")
    print(f"--> Somit ist die Grenzfrequenz f_g < {round(sr/2,2)} Hz\n")

    # Wandle 2D-Tensor [1, Time] zurück in ein 1D-Numpy-Array [Time]
    x = waveform.squeeze().numpy()

    return x, sr


"""
Speichert das Signal als Audiodatei
"""


def save_signal(file_path, x, sr):
    print(f"Speichere Datei: {file_path}")

    # 1D-Numpy-Array --> Pytorch Tensor + Kanal-Dimension
    waveform = torch.from_numpy(x).unsqueeze(0).float()

    torchaudio.save(file_path, waveform, sr)


"""
Erzeugt die Zeitachse t passend zum Signal
"""


def get_time_axis(x, sr):
    return np.linspace(0, len(x) / sr, len(x))
