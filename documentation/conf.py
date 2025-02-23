# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'CoFi'
copyright = '2025, Heinrich Weinz'
author = 'Heinrich Weinz'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys
sys.path.insert(0, os.path.abspath('.'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'myst_parser', # falls du Markdown verwendest
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown', # falls du Markdown verwendest
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'de' # oder 'en', je nach Bedarf

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme' # oder 'alabaster' oder ein anderes Theme
# Wenn du sphinx_rtd_theme verwendest, musst du es installieren: pip install sphinx_rtd_theme

# Wenn du das alabaster theme nimmst:
# html_theme = 'alabaster'

html_static_path = ['_static']

# -- Options for Markdown Files ----------------------------------------------
# https://myst-parser.readthedocs.io/en/latest/configuration.html

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
