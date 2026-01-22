import audio_io
import signal_interpolation as sip
import plots
import matplotlib.pyplot as plt
import os


def get_user_input():

    while True:
        input_file = input(
            "Gib den Pfad zu deiner Datei an (z.B: AUDIO/INPUT/aufnahme_1.mp3): "
        )

        if os.path.exists(input_file):
            file_path = input_file
            break
        else:
            print(f"Die Datei '{input_file}' wurde nicht gefunden.")

    try:
        factor = int(
            input("Jeder wievielte Wert soll genommen werden? (Faktor, z.B. 10): ")
        )  # 15-20 gut
        if factor < 1:
            print("Faktor muss mindestens 1 sein. Setze Faktor auf 1.")
            factor = 1
    except ValueError:
        print("Ungültige Eingabe (keine Zahl). Faktor auf Standardwert 15 gesetzt.")
        factor = 15

    show_plots = (
        input("Möchtest du eine grafische Visualisierung? (y/n): ").lower() == "y"
    )

    return file_path, factor, show_plots


def main():
    # Eingabe
    file_path, factor, show_plots = get_user_input()

    # Daten aus Datei laden
    x, sr = audio_io.load_signal(file_path, duration=20)
    t = audio_io.get_time_axis(x, sr)

    # Verarbeiten
    x_samp, t_samp = sip.downsample_signal(x, t, factor)  # Downsampling
    reconstructions = sip.reconstruct_signal(t_samp, x_samp, t)  # Rekonstruktion

    sr_new = sr / factor
    print(f"--> Das entspricht einer neuen Abtastrate von {round(sr_new,2)} Hz \n")

    # Speichern
    audio_io.save_signal(
        f"AUDIO/OUTPUT/out_stufen_sr{round(sr_new)}Hz.wav",
        reconstructions["stufen"],
        sr,
    )
    audio_io.save_signal(
        f"AUDIO/OUTPUT/out_linear._sr{round(sr_new)}Hz.wav",
        reconstructions["linear"],
        sr,
    )
    audio_io.save_signal(
        f"AUDIO/OUTPUT/out_kubisch._sr{round(sr_new)}Hz.wav",
        reconstructions["kubisch"],
        sr,
    )

    # Darstellen
    if show_plots:
        print("--> Generiere Plots...")
        plots.plot_results(t, x, t_samp, x_samp, reconstructions)
        plots.error_analysis(t, x, t_samp, x_samp, reconstructions)

        for f in [5, 50, 500, 2000, 5000]:
            # Verarbeiten
            x_samp, t_samp = sip.downsample_signal(x, t, f)
            reconstructions = sip.reconstruct_signal(t_samp, x_samp, t)
            plots.plot_comparison(t, reconstructions, f)

        plt.show()


if __name__ == "__main__":
    main()

"""
    Ergebnisse beim Ausprobieren (interessante Werte):
    - Unterscheid Erkennbar ab Faktor :
"""
