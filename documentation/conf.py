# Configuration file for the Sphinx documentation builder.

import os
import sys
#import lexers

#def setup(app):
#    app.add_lexer('mermaid', MermaidLexer())

sys.path.insert(0, os.path.abspath('.'))

project = 'Dein Projektname'
copyright = '2023, Dein Name'
author = 'Dein Name'

extensions = [
    'sphinxcontrib.mermaid',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'myst_parser',
]


source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'de'

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

# Aktiviere die Verarbeitung von Umlauten in HTML
html_use_smartypants = True
