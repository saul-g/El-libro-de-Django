import sys
#import django
from os.path import abspath, dirname, join

# Basic project info
project = u'Django, sobre ruedas'
copyright = u'2014-2016, Saul Garcia Monroy'
version = 1.8
release = 1.8
language = 'es'

# Build options
templates_path = ['_templates']
exclude_patterns = ['_build', 'README.rst']
source_suffix = '.rst'
master_doc = 'index'

#Extensions
sys.path.append(abspath(join(dirname(__file__), "_ext")))
extensions = ["djangodocs", "sphinx.ext.intersphinx"]

# Options for HTML output.
html_theme = 'djangobook'
html_theme_path = ['themes']
html_static_path = ['_static']
pygments_style = 'default'
html_use_index = True
html_show_sourcelink = False
html_show_sphinx = False
html_title = u"Django, sobre ruedas"
html_short_title = 'Django'
html_last_updated_fmt = '%b %d, %Y'
html_add_permalinks = False     # FIXME once styles are fixed to get the hover back.
html_use_smartypants = True
source_encoding = 'utf-8-sig'

latex_documents = [('index', 'Django.tex', 'Django, sobre ruedas',
                    'Saul Garcia Monroy', 'manual', 1)]

latex_elements = {
    'fontpkg': '\\usepackage{palatino}',
}

# texinfo builder
texinfo_documents = [
    ('index', 'Django, sobre ruedas.tex', u'Django, sobre ruedas',
    u'Saul Garcia Monroy', 'book'),
    ]

# ePub builder
epub_title = u'Django, sobre ruedas'
epub_author = u'Saul Garcia Monroy'
epub_publisher =u'Saul Garcia Monroy'
epub_copyright = u'Saul Garcia Monroy'
epub_cover = ('', 'epub-cover.html')
epub_theme = 'djangodocs-epub'

