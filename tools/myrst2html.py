#!/usr/bin/python

import os
import sys
try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import Publisher, default_description, default_usage
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment as SphinxBuildEnvironment
from sphinx.config import Config as SphinxConfig
from sphinx.highlighting import PygmentsBridge


import sphinx.directives.code
import sphinx.directives.other
from sphinx.writers.html import HTMLWriter
from sphinx.builders.html import SingleFileHTMLBuilder

description = ('Generates (X)HTML documents from standalone reStructuredText '
               'sources.  ' + default_description)

config = SphinxConfig (None, None, None, None)
env = SphinxBuildEnvironment (os.path.dirname('.'), "", config)
#XXX: hacks
env.docname = sys.argv[1]
env.found_docs = set([sys.argv[1]])# set([filename])
settings_overrides = {'env': env}


class FakeBuilder:
    from sphinx.writers.html import HTMLTranslator as translator_class
    highlighter = PygmentsBridge('html', 'fruity')

    def __init__(self):
        self.config = config
        self.add_permalinks = False
        self.secnumbers = {}

publisher = Publisher(writer=HTMLWriter(FakeBuilder()))
publisher.set_components('standalone', 'restructuredtext', None)

publisher.publish(
    usage=default_usage,
    description=description,
    settings_overrides=settings_overrides)
