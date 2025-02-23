#!/bin/bash

create_folders() {
    mkdir backend database frontend documentation docker
    mkdir backend/app backend/tests
    mkdir database/init database/migrations
    mkdir frontend/web
    touch backend/app/__init__.py backend/app/main.py backend/app/models.py backend/app/routes.py backend/tests/__init__.py
    touch database/init/init.sql
    touch frontend/web/package.json
    touch docker/docker-compose.yml
    mkdir documentation/architecture documentation/api documentation/database
    touch documentation/architecture/architecture_diagram.md documentation/api/api_documentation.md documentation/database/database_schema.md
}
