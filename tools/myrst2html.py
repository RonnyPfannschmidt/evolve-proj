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
from sphinx.writers.html import HTMLWriter, HTMLTranslator
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
    highlighter = PygmentsBridge('html', 'fruity')

    class translator_class(HTMLTranslator):
        def __init__(self, *k, **kw):
            HTMLTranslator.__init__(self, *k, **kw)
            highlighter = PygmentsBridge('html', 'borland')
            self.stylesheet.append(
                self.embedded_stylesheet % highlighter.get_stylesheet()
            )


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
