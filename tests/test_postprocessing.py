"""
Unit tests for postprocess.py
"""

from projection.parser.postprocess import \
        assign_section_line_numbers,\
        assign_section_text,\
        assign_removal_line_numbers,\
        assign_removal_text


from projection.parser.objects import Parser
from projection.parser.generators import Section, Removal

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
        "# Section",
        "# Section 2\ngoodbye world",
        "# Section 3\n",
    ]

    assigned_sections = assign_section_text(parser)

    output = [m.text for m in assigned_sections]
    output_parser = [m.text for m in parser.matches.values() if isinstance(m, Section)]

    assert output == expected_output
    assert output_parser == expected_output


def test_assign_section_text_multiple():
    """
    Unit test for the function that assigns line numbers to the sections.
    """

    input_text = [
        r"hello world",
        r"%%\findme{Section}",
        r"%%\findyou{Section 2}",
        r"goodbye world",
        r"%%\findme{Section 3}",
        "",
    ]

    def secgen(input):
        return Section(input, r"%%\\findme{(.*?)}", capture=1, id=0)

    def secgenii(input):
        return Section(input, r"%%\\findyou{(.*?)}", capture=1, id=1)

    generators = {
        re.compile(r"%%\\findme{(.*?)}"): secgen,
        re.compile(r"%%\\findyou{(.*?)}"): secgenii,
    }

    parser = Parser(input_text, generators)

    line_numbered_sections_0 = assign_section_line_numbers(parser, id=0)
    line_numbered_sections_1 = assign_section_line_numbers(parser, id=1)

    expected_output_0 = [
        "# Section\n# Section 2\ngoodbye world",
        "# Section 3\n"
    ]

    expected_output_1 = [
        "# Section 2\ngoodbye world\n# Section 3\n"
    ]

    assigned_sections_0 = assign_section_text(parser, id=0)
    assigned_sections_1 = assign_section_text(parser, id=1)

    output_0 = [m.text for m in assigned_sections_0]
    output_1 = [m.text for m in assigned_sections_1]

    assert output_0 == expected_output_0
    assert output_1 == expected_output_1


def test_removal():
    """
    Unit test for the removal postprocessing functions.
    """

    input_text = [
        r"hello world",
        r"%%\beginpdfonly",
        r"THIS IS ONLY FOR THE PDF!",
        r"%%\endpdfonly",
        r"goodbye world",
        "",
    ]

    def remgens(input):
        return Removal(input, r"%%\\beginpdfonly", se="s", id="pdfonly")

    def remgene(input):
        return Removal(input, r"%%\\endpdfonly", se="e", id="pdfonly")

    generators = {
        re.compile(r"%%\\beginpdfonly"): remgens,
        re.compile(r"%%\\endpdfonly"): remgene
    }

    parser = Parser(input_text, generators)

    assign_removal_line_numbers(parser, "pdfonly")
    assign_removal_text(parser, "pdfonly")

    expected_text = "<!--\nTHIS IS ONLY FOR THE PDF!\n-->"

    assert parser.matches[1].text == expected_text

