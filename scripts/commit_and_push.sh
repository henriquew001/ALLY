#!/bin/bash

commit_and_push() {
  git add .
  git commit -m "Initial commit: Project structure, .gitignore, README"
  git push origin main
}
