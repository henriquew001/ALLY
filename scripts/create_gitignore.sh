#!/bin/bash

create_gitignore() {
  cat <<EOF > .gitignore
# Python
*.pyc
__pycache__/
.venv/

# Node.js
node_modules/

# Docker
.dockerenv

# MariaDB
*.log
*.err

# PostgreSQL (auskommentiert)
# *.log
# *.pid
# *.conf.swp
# *.sql.swp
# pg_hba.conf.swp
# pg_ident.conf.swp
# pg_stat_tmp/
# postgresql.conf.swp

# OS generated files #
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
EOF
}
