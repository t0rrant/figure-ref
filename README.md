# figure-ref

Provides a system to reference figures using labels, as happens in LaTeX.

## Requirements

`figure-ref` requires `BeautifulSoup4`.

```bash
pip install BeautifulSoup4
```

## How to Use

Add `'figure-ref'` to the `PLUGINS` list in your settings file, usually `pelicanconf.py`

### RestructuredText

This plugin will search for tags with the `caption` class that are children of any other tag with the `figure` tag

If you define an image as:

````rest
.. _fig-myfigure:

.. figure:: {static}/img/image.png
    :alt: an image alt

    an image caption
````

it will generate the following HTML output (assuming that is the first image in the article):

```html
<div class="figure" id="fig-myfigure">
<a href="/img/image.png"><img alt="an image alt" src="/img/image.png"></a>
<p class="caption"><span>Figure 1: </span>an image alt</p>
</div>
```

This figure can be referenced using the syntax:

1. `{#labelname}`
2. `{F#labelname}`

The first will be replaced by the figure number.
The second will be replaced by the text `Figure N`, where N is the figure number.

Both substitutions will act as a link to the figure.

This plugin allows you to have refs in the image caption, just like with LateX

### Markdown

**Note that at this time the figureAltCaption is not working, as a figure tag is no longer being generated.**
**I am still leaving the Markdown functionality due to it being the main target of this plugin, and if you use an**
**older version of pelican and the most recent version of this plugin it might still work.**
**The current version of pelican where this was tested is `4.2.0`**

This plugin will search for labels within `<figcaption>` tags. Figures and
figcaptions can be inserted in Markdown using the
[figureAltCaption](https://github.com/jdittrich/figureAltCaption) plugin with
Markdown. Labelled figures take the form:

```html
<figure>
  <img src="path/to/image.png">
  <figcaption>
  labelname :: This is the label text.
  </figcaption>
</figure>
```

In Markdown, using the aforementioned plugin, you can create such a figure
with the syntax `![labelname :: This is the label text.](path/to/image.png)`.

This would be traslated to
```html
<figure id="figref-labelname">
  <img src="path/to/image.png">
  <figcaption>
  <strong>Figure 1:</strong> This is the label text.
  </figcaption>
</figure>
```

This figure can be referenced in a paragraph using the syntax `{#labelname}`.
This will then be replaced by the figure number, which will act as a link
to the figure.

### Authors

Chris MacMackin <cmacmackin _at_ gmail.com>
Manuel Torrinha <manuel.torrinha _at_ tecnico.ulisboa.pt>

