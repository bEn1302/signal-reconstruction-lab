# Signal-Rekonstruktion & Interpolationsvergleich

Dieses Projekt demonstriert die Auswirkungen verschiedener Interpolationsmethoden auf digitale Audiosignale. Es zeigt anschaulich, wie Signale abgetastet und auf unterschiedliche Weise mathematisch rekonstruiert werden können.

## Features
* **Abtastung:** Simulation von Downsampling an MP3-Dateien.
* **Interpolation:** Vergleich von drei Methoden:
  1. **Stufenform**
  2. **Linearisierung**
  3. **Lagrange-Interpolation** (stückweise stabil implementiert)
* **Visualisierung:** Plots zum Vergleich der Kurvenverläufe.
* **Audio-Export:** Export der Ergebnisse als `.wav`, um die Effekte hörbar zu machen.

## Installation
1. Repositiory klonen:
   ```bash
   git clone [https://github.com/DEIN_NUTZERNAME/signal-reconstruction-lab.git](https://github.com/DEIN_NUTZERNAME/signal-reconstruction-lab.git)
   cd signal-reconstruction-lab

2. Packete installieren
    ``` bash
    pip install -r requirements.txt

## Benutzung
1. Speichere die MP3-Datei (z.B. `aufnahme.mp3`) im Ordner AUDIO
2. Passe den Dateinamen in der `main.py` an
3. Starte das Programm: 
    ```bash
    python main.py

## Ergebnisse
Das Programm erzeugt einen Plot, der die Rekonstruktion im Detail zeigt, und speichert drei Audiodateien ab, um die qualitativen Unterschiede direkt vergleichen zu können.
