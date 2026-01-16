import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import lagrange

"""

doc: https://matplotlib.org/stable/users/explain/quick_start.html
"""


def plot_results(t_orig, x_orig, t_samp, x_samp, recon_dict, zoom_samples=20):
    plt.figure(figsize=(15, 8))

    # Zoom Bereich festlegen
    mid = len(t_samp) // 2  # Mitte der Samplerate
    # Ausschnit der Betrachtet wird festlegen
    t_start, t_end = (
        t_samp[mid],
        t_samp[mid + zoom_samples],
    )
    # Maske um nur die Werte auszuwählen, die im Zeitfenster liegen
    mask = (t_orig >= t_start) & (t_orig <= t_end)

    """ Plots """
    # Original Zeitkontinueirlich und Zeitdiskret
    plt.plot(t_orig[mask], x_orig[mask], "k", alpha=0.2, lw=3, label="Original x(t)")
    plt.plot(
        t_samp[mid : mid + zoom_samples],
        x_samp[mid : mid + zoom_samples],
        "ko",
        label="Abtastwerte",
    )

    # Rekonstruktion
    plt.plot(t_orig[mask], recon_dict["stufen"][mask], "r--", label="1) Stufen")
    plt.plot(t_orig[mask], recon_dict["linear"][mask], "g--", label="2) Linear")

    # Echte Lagrange Berechnung nur für den Aussschnitt
    try:
        n_points = 5
        t_lag_samp = t_samp[mid : mid + n_points]
        x_lag_samp = x_samp[mid : mid + n_points]

        # Zeitverschiebung um t_start
        t_lag_local = t_lag_samp - t_start

        poly_lagrange = lagrange(t_lag_local, x_lag_samp)
        t_poly = np.linspace(t_lag_samp[0], t_lag_samp[-1], 200)
        y_poly = poly_lagrange(t_poly - t_start)

        plt.plot(
            t_poly, y_poly, "b:", label=f"3) Lagrange (lokal) {n_points-1}. Ordnung"
        )

    except Exception as e:
        print(f"Lagrange Fehler: {e}")

    # Skalierung, das y-Achse beim 1,5 fachen des Minimums beginnt/ des Maximums endet
    plt.ylim(np.min(x_orig[mask]) * 1.5, np.max(x_orig[mask]) * 1.5)

    plt.title("Signalrekonstruktion: Audiotiver Vergleich")
    plt.xlabel("Zeit [s]")
    plt.ylabel("Signal x(t)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
