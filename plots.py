import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import lagrange

"""
Hier werden die Daten geplottet
doc: https://matplotlib.org/stable/users/explain/quick_start.html
"""


# Echte Lagrange Berechnung nur für den Aussschnitt
def _calculate_local_lagrange(t_samp, x_samp, t_start, n_points, t_poly=None):
    try:
        t_lag_samp = t_samp[:n_points]
        x_lag_samp = x_samp[:n_points]
        t_lag_local = (
            t_lag_samp - t_start
        )  # Zeitverschiebung um t_start (Vermeidung numerischer Probleme)

        poly_lagrange = lagrange(t_lag_local, x_lag_samp)

        if t_poly is None:
            # vorher : t_poly = np.linspace(t_lag_samp[0], t_lag_samp[-1], 200)
            t_poly = np.linspace(t_lag_samp[0], t_lag_samp[-1], 200)

        y_poly: np.ndarray = poly_lagrange(t_poly - t_start)
        return t_poly, y_poly, n_points

    except Exception as e:
        print(f"Lagrange Fehler: {e}")
        return None, None, 0


def plot_results(
    t_orig: np.ndarray,
    x_orig: np.ndarray,
    t_samp: np.ndarray,
    x_samp: np.ndarray,
    recon_dict: dict,
    zoom_samples=20,
):
    # --- Plot: Gesamtansicht original Signal ---
    fig1, ax1 = plt.subplots(figsize=(15, 5))
    ax1.plot(t_orig, x_orig, "k", alpha=0.2, label="Original")
    ax1.set_title("Gesamtübersicht des Originalsignals")
    ax1.set_xlabel("Zeit [s]")
    ax1.set_ylabel("Signal x(t)")
    ax1.grid(True)

    # --- Plot: Zoom-Anischt ---
    fig2, ax2 = plt.subplots(figsize=(15, 8))

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
    ax2.plot(t_orig[mask], x_orig[mask], "k", alpha=0.2, lw=3, label="Original x(t)")
    ax2.plot(
        t_samp[mid : mid + zoom_samples],
        x_samp[mid : mid + zoom_samples],
        "ko",
        label="Abtastwerte",
    )

    # Rekonstruktion
    """
    Alt:
    plt.plot(t_orig[mask], recon_dict["stufen"][mask], "r--", label="1) Stufen")
    plt.plot(t_orig[mask], recon_dict["linear"][mask], "g--", label="2) Linear")
    plt.plot(t_orig[mask], recon_dict["kubisch"][mask], "m--", label="3) Kubisch")
    """

    # Rekontruktionsmethoden: (Stil,Beschriftung)
    styles = {
        "stufen": ("r--", "1) Stufen"),
        "linear": ("g--", "2) Linear"),
        "kubisch": ("m--", "3)kubisch"),
    }

    for method, (style, label) in styles.items():
        if method in recon_dict:
            ax2.plot(t_orig[mask], recon_dict[method][mask], style, label=label)

    # Lagrange
    n_points = int(
        input("Welche Ordnung soll dein Lagrange-Interpolation haben (1...20)?")
    )
    t_poly, y_poly, _ = _calculate_local_lagrange(
        t_samp[mid:], x_samp[mid:], t_start, n_points
    )

    if t_poly is not None:
        ax2.plot(
            t_poly, y_poly, "b:", label=f"4) Lagrange (lokal) {n_points-1}. Ordnung"
        )

    y_min, y_max = (
        np.min(x_orig[mask]),
        np.max(x_orig[mask]),
    )  # Skalierung, das y-Achse beim 1,5 fachen des Minimums beginnt/ des Maximums endet
    ax2.set_ylim(y_min * 1.5, y_max * 1.5)
    ax2.set_title("Signalrekonstruktion")
    ax2.set_xlabel("Zeit [s]")
    ax2.set_ylabel("Signal x(k)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)


# --- Entwicklung x(f) mit geringerer Abtastung (Faktor = 1...sr)
def plot_comparison(t_orig: np.ndarray, recon_dict: dict, factor: int):
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
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(24, 6), sharey=True)
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
        "lagrange": {"ax": ax4, "color": "b", "label": "Lagrange"},
    }

    for method, config in setup.items():
        if method in recon_dict or method == "lagrange":
            ax = config["ax"]
            # Fehlerberechnung nur für den maskierten Bereich

            if method == "lagrange":
                _, y_poly, order = _calculate_local_lagrange(
                    t_samp[mid:], x_samp[mid:], t_start, 20, t_poly=t_orig[mask]
                )
                abs_error = np.abs(x_orig[mask] - y_poly)
                if y_poly is not None:
                    abs_error = np.abs(x_orig[mask] - y_poly)
                else:
                    print("Lagrange Berechnung fehlgeschlagen, überspringe Plot.")
                    continue
            else:
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
