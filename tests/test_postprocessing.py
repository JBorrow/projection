"""
Unit tests for postprocess.py
"""

from parser.postprocess import \
        assign_section_line_numbers,\
        assign_section_text

from parser.objects import Parser
from parser.generators import Section

import re


def test_assign_section_line_numbers():
    """
    Unit test for the function that assigns line numbers to the sections.
    """

    input_text = [
        r"hello world",
        r"%%\findme{Section}",
        r"%%\findme{Section 2}",
        r"goodbye world",
        r"%%\findme{Section 3}",
        "",
    ]

    def secgen(input):
        return Section(input, r"%%\\findme{(.*?)}", capture=1)

    generators = {
        re.compile(r"%%\\findme{(.*?)}"): secgen,
    }

    parser = Parser(input_text, generators)

    line_numbered_sections = assign_section_line_numbers(parser)

    # from list
    line_numbers = [[m.startline, m.endline] for m in line_numbered_sections]
    # from object
    only_sections = [m for m in parser.matches.values() if isinstance(m, Section)]
    line_numbers_object = [[m.startline, m.endline] for m in only_sections]

    expected_output = [[1,2], [2,4], [4, 6]]

    assert expected_output == line_numbers
    assert expected_output == line_numbers_object


def test_assign_section_text():
    """
    Unit test for the function that assigns line numbers to the sections.
    """

    input_text = [
        r"hello world",
        r"%%\findme{Section}",
        r"%%\findme{Section 2}",
        r"goodbye world",
        r"%%\findme{Section 3}",
        "",
    ]

    def secgen(input):
        return Section(input, r"%%\\findme{(.*?)}", capture=1)

    generators = {
        re.compile(r"%%\\findme{(.*?)}"): secgen,
    }

    parser = Parser(input_text, generators)

    line_numbered_sections = assign_section_line_numbers(parser)

    expected_output = [
        [r"# Section"],
        [r"# Section 2", r"goodbye world"],
        [r"# Section 3", ""]
    ]

    assigned_sections = assign_section_text(parser)

    output = [m.text for m in assigned_sections]
    output_parser = [m.text for m in parser.matches.values() if isinstance(m, Section)]

    assert output == expected_output
    assert output_parser == expected_output

