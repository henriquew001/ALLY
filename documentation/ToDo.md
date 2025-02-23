# ToDo

## Docker Umgebung Verbesserungen

### Sicherheit

- [ ] Passwörter nicht direkt in `docker-compose.yml` speichern
    - [ ] Docker Secrets für sensible Daten verwenden
    - [ ] Umgebungsvariablen aus externer Quelle laden
- [ ] Zugriffsbeschränkungen für Docker-Images und Container überprüfen und anpassen
- [ ] Regelmäßige Sicherheitsupdates für Docker-Engine und Container-Images durchführen

### Healthcheck

- [ ] `/health`-Endpoint im Backend-Service implementieren
    - [ ] Korrekten Zustand der Anwendung im Endpoint widerspiegeln
- [ ] Docker Compose Healthchecks konfigurieren, um Container-Zustände zu überwachen
- [ ] Überwachungssystem einrichten, um Healthchecks zu protokollieren und zu alarmieren

### Logging

- [ ] Logging zum Backend-Service hinzufügen
    - [ ] Fehler protokollieren
    - [ ] Wichtige Informationen protokollieren
    - [ ] Log-Level konfigurieren (Debug, Info, Warnung, Fehler)
- [ ] Zentralisiertes Log-Management einrichten (z.B. mit ELK Stack, Loki oder Graylog)
- [ ] Log-Rotation und -Archivierung konfigurieren, um Speicherplatz zu sparen

### Dockerfile Optimierung

- [ ] Dockerfiles überprüfen und optimieren
    - [ ] Multi-Stage Builds verwenden, um Image-Größe zu reduzieren
    - [ ] Minimale Basis-Images verwenden (z.B. alpine)
    - [ ] Caching von Docker-Layern optimieren
    - [ ] Unnötige Dateien und Abhängigkeiten entfernen
- [ ] Image-Scans auf Sicherheitslücken durchführen (z.B. mit Trivy oder Snyk)
- [ ] Das Port-Mapping 3306:3306 ist in Ordnung für lokale Entwicklung, sollte aber in Produktionsumgebungen vermieden werden.

### Netzwerk

- [ ] Benutzerdefinierte Netzwerke in Docker verwenden
    - [ ] Netzwerktreiber auswählen (Bridge, Overlay, Macvlan)
    - [ ] Subnetze und IP-Bereiche konfigurieren
- [ ] Container-Kommunikation über Netzwerke isolieren
- [ ] Netzwerkrichtlinien für Container festlegen, um Zugriff zu beschränken
- [ ] Reverse-Proxy für das Backend aufsetzen.
