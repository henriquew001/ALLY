#!/bin/bash

# Variablen
REPO_URL="git@github.com:henriquew001/ConsciousFit.git"

# Unterscripte einbinden
source scripts/create_folders.sh
source scripts/create_gitignore.sh
source scripts/create_readme.sh
source scripts/create_github_actions_workflow.sh
source scripts/commit_and_push.sh

#create_folders
#create_gitignore
#create_readme
#create_github_actions_workflow
#commit_and_push
