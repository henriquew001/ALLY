```plantuml
@startuml
!define AzurePuml https://raw.githubusercontent.com/plantuml-stdlib/Azure-PlantUML/master/dist
!include AzurePuml/AzureCommon.puml
!include AzurePuml/Databases/AzureDatabaseForMariaDb.puml
!include AzurePuml/Compute/AzureAppService.puml
!include AzurePuml/General/AzureUsers.puml

node "Backend-Server" {
  [Python (Django/Flask)] as python
  AzureDatabaseForMariaDb(MariaDB, "Datenbank")
  [RESTful API] as api
  [Sphinx (Dokumentation)] as sphinx
  python --> MariaDB
  python --> api
  sphinx -- python
}

node "Webanwendung" {
  [React/Angular/Vue.js] as webapp
}

node "Mobile Apps" {
  [React Native/Flutter] as mobileapp
}

AzureUsers(User, "Benutzer")
User --> webapp : Webbrowser
User --> mobileapp : Mobile Apps
webapp --> api : REST API
mobileapp --> api : REST API

node "Versionkontrolle" {
  [Git (GitHub)] as git
}

node "Dokumentation" {
  [Markdown] as markdown
}

node "Lizenzen" {
  [LGPL/Kompatible] as lizenz
}

api --> python
@enduml
```
