import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import lagrange

"""
Hier werden die Daten zum geplottet
doc: https://matplotlib.org/stable/users/explain/quick_start.html
"""


def plot_results(t_orig, x_orig, t_samp, x_samp, recon_dict, zoom_samples=20):
    # --- Plot: Gesamtansicht original Signal ---
    plt.figure(figsize=(15, 5))
    plt.plot(t_orig, x_orig, "k", alpha=0.2, label="Original")
    plt.title("Gesamtübersicht des Originalsignals")
    plt.xlabel("Zeit [s]")
    plt.ylabel("Signal x(t)")
    plt.grid(True)

    # --- Plot: Zoom-Anischt ---
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
    plt.plot(t_orig[mask], recon_dict["kubisch"][mask], "m--", label="3) Kubisch")

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
            t_poly, y_poly, "b:", label=f"4) Lagrange (lokal) {n_points-1}. Ordnung"
        )

    except Exception as e:
        print(f"Lagrange Fehler: {e}")

    # Skalierung, das y-Achse beim 1,5 fachen des Minimums beginnt/ des Maximums endet
    plt.ylim(np.min(x_orig[mask]) * 1.5, np.max(x_orig[mask]) * 1.5)

    plt.title("Signalrekonstruktion")
    plt.xlabel("Zeit [s]")
    plt.ylabel("Signal x(k)")
    plt.legend()
    plt.grid(True, alpha=0.3)


# --- Entwicklung x(f) mit geringerer Abtastung (Faktor = 1...sr)
def plot_comparison(t_orig, recon_dict, factor):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
    fig.suptitle(f"Rekonstruktions-Vergleich | Abtastfaktor: {factor}", fontsize=16)

    ax1.plot(t_orig, recon_dict["stufen"], "r", alpha=0.7)
    ax1.set_title("Stufen")
    ax1.set_xlabel("Zeit [s]")
    ax1.grid(True, alpha=0.2)

    ax2.plot(t_orig, recon_dict["linear"], "g", alpha=0.7)
    ax2.set_title("Linear")
    ax2.set_xlabel("Zeit [s]")
    ax2.grid(True, alpha=0.2)

    ax3.plot(t_orig, recon_dict["kubisch"], "m", alpha=0.7)
    ax3.set_title("Kubisch")
    ax3.set_xlabel("Zeit [s]")
    ax3.grid(True, alpha=0.2)

    plt.tight_layout()


def error_analysis(t_orig, x_orig, t_samp, x_samp, recon_dict, zoom_samples=20):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6), sharey=True)
    fig.suptitle(
        "Detaillierte Fehleranalyse (Absoluter Fehler pro Methode)", fontsize=16
    )

    mid = len(t_samp) // 2  # Mitte der Samplerate
    t_start, t_end = (
        t_samp[mid],
        t_samp[mid + zoom_samples],
    )
    mask = (t_orig >= t_start) & (t_orig <= t_end)

    # Dictionary, um die Methoden den Achsen und Farben zuzuordnen
    setup = {
        "stufen": {"ax": ax1, "color": "r", "label": "Stufen"},
        "linear": {"ax": ax2, "color": "g", "label": "Linear"},
        "kubisch": {"ax": ax3, "color": "m", "label": "Kubisch"},
    }

    for method, config in setup.items():
        if method in recon_dict:
            ax = config["ax"]
            # Fehlerberechnung nur für den maskierten Bereich
            abs_error = np.abs(x_orig[mask] - recon_dict[method][mask])

            # Plot auf der jeweiligen Achse (ax.plot statt plt.plot)
            ax.plot(
                t_orig[mask],
                abs_error,
                color=config["color"],
                label=f"Fehler {config['label']}",
                alpha=0.8,
            )

            # Einstellungen für jeden Subplot
            ax.set_yscale("log")
            ax.set_ylim(1e-8, 2)
            ax.set_title(f"Methode: {config['label']}")
            ax.set_xlabel("Zeit [s]")
            ax.grid(True, which="both", ls="-", alpha=0.3)
            ax.legend(loc="upper right")

    # Y-Achsen-Beschriftung nur für den ersten Plot links
    ax1.set_ylabel("Absoluter Fehler (Log-Skala)")
    plt.tight_layout()
