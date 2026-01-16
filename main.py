import audio_io
import signal_interpolation as sip
import plots

# Variablen
FILE = "AUDIO/aufnahme_1.mp3"
FACTOR = 15


def main():
    # Daten aus Datei laden
    x, sr = audio_io.load_signal(FILE, duration=20)
    t = audio_io.get_time_axis(x, sr)

    # Verarbeiten
    x_samp, t_samp = sip.downsample_signal(x, t, FACTOR)
    reconstructions = sip.reconstruct_signal(t_samp, x_samp, t)

    # Darstellen
    plots.plot_results(t, x, t_samp, x_samp, reconstructions)

    # Speichern
    audio_io.save_signal("out_stufen.wav", reconstructions["stufen"], sr)
    audio_io.save_signal("out_linear.wav", reconstructions["linear"], sr)
    audio_io.save_signal("out_kubisch.wav", reconstructions["kubisch"], sr)


if __name__ == "__main__":
    main()
