# Signal-Rekonstruktion & Interpolationsvergleich

Dieses Projekt demonstriert die Auswirkungen verschiedener Interpolationsmethoden auf digitale Audiosignale. Es zeigt anschaulich, wie Signale abgetastet und auf unterschiedliche Weise mathematisch rekonstruiert werden können.

## Features
* **Aufnahme:*** Sprachaufnahme
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
   git clone [https://github.com/bEn1302/signal-reconstruction-lab.git](https://github.com/bEn1302/signal-reconstruction-lab.git)
   cd signal-reconstruction-lab
2. Virtual Enviroment erstellen und aktivieren:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
3. Packete installieren
    ``` bash
    pip install -r requirements.txt

## Benutzung
1. Speichere die MP3-Datei (z.B. `aufnahme.mp3`) im Programmordner
2. Passe den Dateinamen und -pfad in der `main.py` an
3. Starte das Programm: 
    ```bash
    python main.py

## Ergebnisse
Das Programm erzeugt einen Plot, der die Rekonstruktion im Detail zeigt, und speichert drei Audiodateien ab, um die qualitativen Unterschiede direkt vergleichen zu können.

- ab dem Faktor 8 d.h. eine Abtastrate von ca. 5,513 kHz wird die Sprache bei der Stufen- & Lineare-Rekonstruktion undeutlicher
- ab dem Faktor 10 (4,41 kHz) ist die Sprache der Stufen-Rekonstruktion gerade so verständlich, Linear & Kubisch sind recht verständlich
- ab dem Faktor 20 (2,21 kHz) ist bei der Stufenform keine Sprache mehr erkennbar, bei der Linearen nur teilweise, bei der kubischen ist noch recht verständlich
- ab dem Faktor 50 (0,88 kHz) ist keine Sprache mehr verständlich, man hört sehr klar die unterschiede der verschiedenen Rekonstruktionen
- ab dem Faktor 100 (0,44 kHz) hört man viele Verzerrungen
- ab dem Faktor 1000 (0,04 kHz) ist nur noch ein "Knacken" oder "Brummen" zu hören


