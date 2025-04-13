# Projektarchitektur

## Übersicht

Dieses Dokument beschreibt die Architektur unseres Projekts, das einen Dienst bereitstellt, der sowohl über Webbrowser als auch über mobile Apps (Android, iOS, Windows) zugänglich ist.

## Komponenten

* **Backend-Server:**
    * **Programmiersprache:** Python (mit Django oder Flask)
    * **Datenbank:** PostgreSQL
    * **API:** RESTful API
    * **Dokumentation:** Sphinx
* **Webanwendung:**
    * **Frontend:** React, Angular oder Vue.js
* **Mobile Apps:**
    * **Cross-Plattform:** React Native oder Flutter
* **Versionskontrolle:** Git (mit GitHub)
* **Dokumentation:** Markdown

## Architekturdiagramm

Hier finden Sie eine Übersicht über unsere Systemarchitektur.

[Architekturdiagramm](architecture_diagram.md)

## Detailbeschreibung

### Backend-Server

Der Backend-Server bildet das Herzstück des Dienstes. Er ist verantwortlich für:

* Datenhaltung (PostgreSQL)
* Verarbeitung der Geschäftslogik (Python)
* Bereitstellung einer RESTful API für die Kommunikation mit der Webanwendung und den mobilen Apps

Die Dokumentation des Python-Codes erfolgt mit Sphinx.

### Webanwendung

Die Webanwendung ermöglicht den Zugriff auf den Dienst über Webbrowser. Sie kommuniziert über die RESTful API mit dem Backend-Server. Als Frontend-Frameworks stehen React, Angular oder Vue.js zur Auswahl.

### Mobile Apps

Die mobilen Apps ermöglichen den Zugriff auf den Dienst über mobile Geräte (Android, iOS, Windows). Sie kommunizieren ebenfalls über die RESTful API mit dem Backend-Server. Für die Entwicklung der Apps werden Cross-Plattform-Frameworks wie React Native oder Flutter verwendet.

### Versionskontrolle

Git und GitHub werden für die Versionskontrolle des Quellcodes verwendet. Für die kommunikation mit GitHub werden SSH-Schlüssel verwendet.

### Dokumentation

* Sphinx wird verwendet, um die Python-Code-Dokumentation zu generieren.
* Markdown wird für allgemeine Projektdokumentation und Entscheidungsdokumente verwendet.

### Lizenzierung

Es wird darauf geachtet, dass alle verwendeten Komponenten LGPL oder kompatible Lizenzen besitzen.

## Entscheidungen

* **Datenbank:** PostgreSQL wurde aufgrund der Komplexität des Projekts ausgewählt.
* **API:** RESTful APIs wurden aufgrund ihrer Einfachheit und weiten Verbreitung gewählt.
* **Dokumentation:** Sphinx und Markdown wurden aufgrund ihrer Leistungsfähigkeit und Benutzerfreundlichkeit gewählt.

## Nächste Schritte

* Auswahl der spezifischen Frontend- und Mobile-Frameworks.
* Implementierung der RESTful API.
* Einrichtung der Entwicklungsumgebung.
