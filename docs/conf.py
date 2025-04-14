import os
import sys
sys.path.insert(0, os.path.abspath('../../backend'))
sys.path.insert(0, os.path.abspath('../backend/app'))
sys.path.insert(0, os.path.abspath('../../backend/routers'))
sys.path.insert(0, os.path.abspath('./_ext'))

sys.path.insert(0, os.path.abspath('.'))

project = 'A L L Y'
copyright = '2025, Heinrich Weinz'
author = 'Heinrich Weinz'

extensions = [
    'sphinxcontrib.mermaid',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'myst_parser',
    'sphinxcontrib.plantuml',
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

plantuml_output_format = 'svg'
