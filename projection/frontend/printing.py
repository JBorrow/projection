"""
Pretty-printing functions for the database objects.
"""

from typing import List

from ..parser.generators import Collector, Section

def print_collectors(collectors: List[Collector]) -> str:
    """
    Prints the collectors as a nice HTML list.

    Returns a string.
    """

    create_li = lambda x: f"<li>{x.text}</li>"
    lis = "\n".join(list(map(create_li, collectors)))

    return f"<ul>\n{lis}\n</ul>"


def print_page_content(section: Section) -> str:
    """
    Prints the content of the section.

    Returns a string.
    """
    
    return section.output_text

