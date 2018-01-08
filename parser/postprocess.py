from .objects import Parser
from .generators import Section, Collector, Removal

from typing import List

def assign_section_line_numbers(parser: Parser, id=None) -> List[Section]: 
    """
    Assign the sections their line numbers.

    Returns a list of Sections and _also_ modifies the parser object.
    """
    
    prev_match = None
    sections = []

    for line_number, match in parser.matches.items():
        if isinstance(match, Section) and match.id == id:
            match.line = line_number  # Cross-compat with collectors
            match.startline = line_number

            if prev_match is not None:
                prev_match.endline = line_number

            prev_match = match  # notably a _pointer_ to the match.

            sections.append(match)


    # Do the last one!
    prev_match.endline = len(parser.text)

    return sections


def assign_section_text(parser: Parser, id=None) -> List[Section]:
    """
    Assign the relevant text to each 'section'.

    Returns a list of Sections and _also_ modifies the parser object.
    """

    matches = parser.matches.values()
    sections = []
    filter_expression = lambda m: isinstance(m, Section) and m.id == id

    for match in filter(filter_expression, matches):
        match.text = "\n".join(parser.text[match.startline:match.endline])
        sections.append(match)

    return sections


def assign_collector_line_numbers(parser: Parser, id=None) -> List[Collector]:
    """
    Assign a line number to each 'collector'.

    Returns a list of collectors and _also_ modifies the parser object.
    """

    collectors = []
    filter_expression = lambda m: isinstance(m[1], Collector) and m[1].id == id

    for line, match in filter(filter_expression, parser.matches.items()):
        match.line = line
        collectors.append(match)

    return collectors


def assign_removal_line_numbers(parser: Parser, id=None) -> List[Removal]:
    """
    Assign the start/end line numbers to the removal items, and delete/pop
    the removal-end objects.
    """

    start = None
    end = None

    removals = []
    ends = []

    filter_expression = lambda m: isinstance(m[1], Removal) and m[1].id == id

    for line, match in filter(filter_expression, parser.matches.items()):
        match.line = line
        print(f"line {line} made it!")

        if match.se == "s":
            # Start!
            start = match

        elif match.se == "e":
            # End!
            end = match

            start.startline = start.line
            start.endline = end.line

            end = None
            start = None

            removals.append(start)
            ends.append(line)

        else:
            raise AttributeError("Start/end of Removal object not set.")


    for line in ends:
        del parser.matches[line]


    return removals


def assign_removal_text(parser: Parser, id=None) -> List[Removal]:
    """
    Assign the relevant text to the Removal object.
    """

    removals = []
    filter_expression = lambda m: isinstance(m[1], Removal) and m[1].id == id

    for line, match in filter(filter_expression, parser.matches.items()):
        match.text = "\n".join(parser.text[match.startline:match.endline+1])
        removals.append(match)

    return removals


