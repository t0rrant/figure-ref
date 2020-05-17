# -*- coding: utf-8 -*-
"""
figure_ref
==========

A Pelican plugin that provides a LaTeX-like system for referencing figure
elements within an article or page. Each figure caption is changed to match
its number according to order of appearance.

A figure caption is considered one of:

- `figcaption` tag which its parent is a `figure` tag
- any tag with `caption` class which its parent has the `figure` class

The figures can be referenced with the syntax {#labelname}, which will be replaced by
the figure number. The figure number will provide a link to the figure.
The figures can also be referenced with the syntax {F#labelname}, which will be replaced
by the string 'Figure N', where N is the figure number, and that whole string will provide
a link to the figure.
"""

import logging
import re

from bs4 import BeautifulSoup, FeatureNotFound

from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator

import sys

if sys.version_info[0] > 2:
    unicode = str

__version__ = '0.1.0'

# creates a group that matches 1 or more word or hyphen
REF_NUM_RE = re.compile(r'{#([\w\-]+)}')
# creates a group that matches 1 or more word or hyphen
REF_RE = re.compile(r'{F#([\w\-]+)}')
# creates a group that matches 1 or more word or hyphen
LABEL_RE = re.compile(r'^([\w\-]+) ::')
REF_NUM = "<a href='#{}'>{}</a>"
REF = "<a href='#{}'>Figure {}</a>"

LABEL = "<span>Figure {}:</span> "

logger = logging.getLogger(__name__)


def process_content(article):
    """
    Substitute reference links for an individual article or page.
    """
    try:
        soup = BeautifulSoup(article._content, 'lxml')
    except FeatureNotFound:
        soup = BeautifulSoup(article._content, 'html.parser')

    # Get figures and number them
    figures = []

    def format_caption(figure):
        if 'figure' in figure.parent.attrs['class'] and 'id' in figure.parent.attrs:
            figures.append(figure.parent.attrs['id'])
            new_tag = soup.new_tag("span")
            new_tag.string = "Figure {}: ".format(len(figures))
            figure.insert(0, new_tag)
        elif figure.parent.name == 'figure':
            caption = unicode(figure.contents[0])
            m = LABEL_RE.search(caption)
            if m:
                figures.append(m.group(1))
                figure.parent['id'] = m.group(1)
                new_tag = soup.new_tag("strong")
                figure.contents[0].replace_with(' ' + caption[m.end():])
                new_tag.string = "Figure {}:".format(len(figures))
                figure.insert(0, new_tag)

    def substitute_num(match):
        # Replace references to figures with links
        try:
            num = figures.index(match.group(1)) + 1
        except ValueError:
            logger.warning('`figure_ref` unable to find figure with label "{}" in file {}'.format(match.group(1),
                                                                                                  article.source_path))
            return match.string
        return REF_NUM.format(match.group(1), num)

    def substitute(match):
        # Replace references to figures with links
        try:
            num = figures.index(match.group(1)) + 1
        except ValueError:
            logger.warning('`figure_ref` unable to find figure with label "{}" in file {}'.format(match.group(1),
                                                                                                  article.source_path))
            return match.string
        return REF.format(match.group(1), num)

    for fig in soup.find_all(class_='caption'):
        format_caption(fig)

    for fig in soup.find_all('figcaption'):
        format_caption(fig)

    article._content = REF_NUM_RE.sub(substitute_num, unicode(soup))
    article._content = REF_RE.sub(substitute, unicode(soup))


def add_figure_refs(generators):
    # Process the articles and pages
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                process_content(article)
            for draft in generator.drafts:
                process_content(draft)
        elif isinstance(generator, PagesGenerator):
            for page in generator.pages:
                process_content(page)


def register():
    signals.all_generators_finalized.connect(add_figure_refs)

