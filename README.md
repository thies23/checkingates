# Check In Gates

Zeigt welches Gate als letztes genutzt wurde um eine Person in Pretix einzuchecken.

Als kleinen Hack für Jugend hackt Events entwickelt.

## Vorbereitung

### Installation

- `git clone https://github.com/thies23/checkingates`
- `pip install -r requirements.txt`
- `cp config.ini.example config.ini`
- config.ini füllen
- `cp gates.txt.example gates.txt`
- gates.txt füllen
- `python app.py`

### config.ini

`url` Die URL zu der CheckIn Liste

Die korrekte ID kann über den Endpunkt `https://{FQDN}/api/v1/organizers/{ORGANIZER}/events/{EVENT_SLUG}/checkinlists/` herausgefunden werden.

(*Wenn deine Pretix Instanz zB unter `https://anmeldung.alpaka.space` läuft, dein Organizer `test` heißt und dein Event `test123` heißt kannst du mit `https://anmeldung.alpaka.space/api/v1/organizers/test/events/test123/checkinlists` die korrekte ID herausfinden*)

`token` ein API token den du in den Organizer Settings erstellen kannst.

### gates.txt

Fülle die jeweilige Gate ID gefolgt von einem `;` und dann dem jeweiligen Ort in die Datei ein.
Diese wird bei jedem Seitenaufruf gelesen. Die Anwendung muss also nicht neu gestartet werden, wenn sich dort etwas ändert.