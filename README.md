Projection
==========

A parser for lecture notes (and other TeX documents) using custom syntax
to go from TeX to an HTML website via Markdown, thanks to Pandoc.

Your document will be parsed to a SQLite database, and this will then
be passed to the frontend code that turns it into a website.

You can define your own templates in `frontend/template`.


What?
-----

`projection` allows you to define three types of custom syntax:

### Sections

These sections will be broken up into different HTML documents, and can be
overlapping. One example use could be a set of 'sections' in a document,
and a set of 'lectures' over which they were covered. These might not
always be the same thing!

### Collectors

These are things that need to be 'picked up' throughout the document and
associated with the above 'Sections'. An example could be keypoints in a 
set of lecture notes. These can then be dynamically displayed on each
relevant page.

### Removals

These are items that need to be removed from the HTML output. Examples
might include things like LaTeX positioning commands for images.


Parameter File
--------------

To run `projection`, you will need to specify a parameterfile, which is
written in the `YAML` structured text format.

```yaml
meta:
  title: "Hello World"  # Title of your website
  author: "Author"  # Your name!
  database: "example.db"  # Name of your databse


sections:
  - name: "Sections"  # Name of this section (needs to be unique) to
                      # display on the website.
    syntax: "section"  # The custom syntax you wish to use to denote
                       # a new section. This corresponds to
                       #    %%\section{name_of_section}.
    level: 1           # Heading level. Use 0 to not display.


collectors:
  - name: "Keypoints"  # The name of the section of collectors to display
    syntax: "keypoint" # The custom syntax -- this corresponds to
                       #    %%\keypoint{keypoint_text}.


removals:
  - name: "PDFONLY"  # Name, this is arbritary.
    syntax:
      start: "beginpdfonly"  # Start syntax (%%\beginpdfonly)
      end: "endpdfonly"      # End syntax.  (%%\endpdfonly)
```

You can define as many of these with as many names as you wish!


