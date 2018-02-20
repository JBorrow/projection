"""
Pretty-printing functions for the database objects.
"""

from typing import List

from ..generators import Collector, Section

def print_collectors(collectors: List[Collector]) -> str:
    """
    Prints the collectors as a nice HTML list.

    Returns a string.
    """

    create_li = lambda x: f"<li>{x.output_text}</li>"
    lis = list(map(create_li, collectors))

    return f"<ul>\n{'\n'.join(lis)}\n</ul>"


def print_page_content(section: Section) -> str:
    """
    Prints the content of the section.

    Returns a string.
    """
    
    return section.output_text

