__**Fritztracker**__

Das Programm Fritztracker ist dafür entwickelt, Daten, wie die Leistung und Temperatur von in die Fritzbox integrierten Systemen, zu dokumentieren und anschließend zu visualisieren.

1. Tracking:
- Um die Skripte zu nutzen, empfehle ich Linux/WSL/OSX als OS. Die Start- und Stoppskripte arbeiten mit dem Programm "Screen", welches das Programm im Hintergrund laufen lässt. Dieses gibt es nur für genannte Systeme.
- In dem Ordner, in dem die Tracking-Dateien gespeichert werden sollen, folgenden Befehl ausführen oder Dateien dort entpacken: `git clone git@github.com:FlyingAgent/FritzTracker.git`
- Folgende Befehle ausführen, um benötigte Programme zu installieren:
```
  sudo apt-get update
  sudo apt-get upgrade -y
  sudo apt-get install screen
```
```
sudo apt install -y python3 python3-dev python3-venv
```
```
sudo apt install -y python3-pip
```
- Python Installation überprüfen:
```
python -v && pip3 -v
```
- Im Zielordner das Setup-Skript ausführen:
```
sudo ./setup.sh
```
- Neue `.env` Datei erstellen, um Zugangsdaten zur Fritzbox für das Programm zu festzulegen. Ggf. muss erst ein Nutzer für diesen Anwendungsfall erstellt werden. Die `.env`-Datei sollte folgende Parameter enthalten:
```
FRITZBOX_ADDRESS=
FRITZBOX_USERNAME=
FRITZBOX_PASSWORD=
INTERVAL=60
```
Die Addresse der Fritzbox ist standartmäßig `192.168.178.1`. Der Interval bestimmt in welchem zeitlichen Abstand (Sekunden) Daten gespeichert werden sollen. Es empfiehlt sich diesen für die Analyse bei 60 zu lassen.
- Zum Starten/Stoppen des Tracking:
```
sudo ./start.sh
```
```
sudo ./stop.sh
```

2. Visualisierung
- Oben genannte Schritte bis einschließlich dem Setup-Skript ebenfalls ausführen. Screen muss hierbei allerdings nicht installiert werden.
- Die zu analysierende Datei in den gleichen Ordner verschieben, in dem die FritzTracker-Dateien ebenfalls vorliegen.
- Folgenden Befehl ausführen im Terminal, um die Visualisierung zu starten (entweder zuerst mit `cd` in diesen Ordner bewegen oder den vollständigen Dateipfad für `venv/bin/python`verwenden):
```
venv/bin/python analytics.py --path name_der_zu_analysierenden_datei.json
```
Zusatzälich können noch folgende Parameter optional angehängt werden, um die Analyse zu optimieren:
```
--scale ...
--max-power ...
--max-temp ...
```






