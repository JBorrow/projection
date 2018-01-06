from .objects import Parser
from .generators import Section

from typing import List

def assign_section_line_numbers(parser: Parser) -> List[Section]: 
    """
    Assign the sections their line numbers.

    Returns a list of Sections and _also_ modifies the parser object.
    """
    
    prev_match = None
    sections = []

    for line_number, match in parser.matches.items():
        if isinstance(match, Section):
            match.startline = line_number

            if prev_match is not None:
                prev_match.endline = line_number

            prev_match = match  # notably a _pointer_ to the match.

            sections.append(match)


    # Do the last one!
    prev_match.endline = len(parser.text)

    return sections


def assign_section_text(parser: Parser) -> List[Section]:
    """
    Assign the relevant text to each 'section'.

    Returns a list of Sections and _also_ modifies the parser object.
    """

    matches = parser.matches.values()
    sections = []

    for match in filter(lambda m: isinstance(m, Section), matches):
        match.text = parser.text[match.startline:match.endline]
        sections.append(match)

    return sections

