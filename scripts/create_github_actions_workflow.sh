#!/bin/bash

create_github_actions_workflow() {
  mkdir -p .github/workflows
  cat <<EOF > .github/workflows/deploy-docs.yml
name: Deploy Sphinx Docs to GitHub Pages

on:
  push:
    branches:
      - main # oder master, je nach deinem Branch-Namen

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          pip install sphinx sphinx-rtd-theme myst-parser

      - name: Build Sphinx Docs
        run: |
          cd documentation
          make html

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./documentation/_build/html
}
EOF
