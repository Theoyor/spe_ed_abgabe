# Wie benutzt man den Bums

### Disclaimer:
- Wer Fehler in der Spielelogik glaubt gefunden zu haben schreibt ein Support Ticket oder einfach direkt Philipp  

- Gleiches gilt für Anzeigefehler und Theo

### Docker
- Docker installieren [Docker](https://www.docker.com/get-started)

- Falls du VS Code benutzt dann noch ne docker extension [Docker VS Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)


### Benutzung
- Bei VSCode einfach F5 Drücken, wenn der Ordner geöffnet ist.
- Wenn das Spiel durchgelaufen ist, erscheint ein Hallo statt der weißen Seite im Browserfenster, dann einfach /render an die URL anhängen für Visualisierung
- Beispiel: http://localhost:49196/  und http://localhost:49196/render
- Wenn mehrere Spiele mit dem gleichen Code getestet werden sollen, am besten beide URLs in verschiedenen Tabs auf haben. Um ein neues Spiel zu starten erst die original-URL neu laden, dann die mit /render
-  Wenn der Code geändert wird, muss das Programm erst komplett neu gestartet werden



### Programmieren

- Einmal die zwei Klassen aus game.py grob anschauen, in game.py passiert die Spielelogik und Verbindung zum Docker
- In util.py befinden sich Funktionen, die alle gebrauchen können
- In name.py befindet sich die jeweilige KI von uns, diese muss natürlich mit dem Rest verbunden werden 

# Teilen ist Heilen
##### Gegenseitig helfen ist wichtig, alle Funktionen, die auch andere Gebrauchen könnten bitte kommentiert in util.py schreiben und am Anfang auch in den extra dafür erstellten Discord Chat 