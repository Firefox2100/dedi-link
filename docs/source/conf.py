# Configuration file for the Sphinx documentation builder.

# -- Project information
import dedi_link
from packaging.version import Version


project = 'Decentralised Discovery Link'
copyright = '2024, Firefox2100'
author = 'Firefox2100'

# Extract version from package
_v = Version(dedi_link.__version__)

release = str(_v)
version = f'{_v.major}.{_v.minor}'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.plantuml',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
