"""
Tests for the parser.

This can be found in objects.py.
"""

from projection.parser.objects import Parser
from projection.parser.generators import Collector, Section, Removal

import re

def test_collector():
    """
    Unit test for the parser using the collector.

    Not yet implemented: line numbers.
    """

    input_text = [
        r"hello world",
        r"%%\findme{collector}",
        r"goodbye world",
        "",
    ]

    def colgen(input):
        return Collector(input, r"%%\\findme{.*?}")

    generators = {
        re.compile(r"%%\\findme{.*?}"): colgen,
    }

    parser = Parser(input_text, generators)

    expected_output = [
        r"hello world",
        "<!-- Collector {} -->".format(parser.matches[1].uid),
        r"goodbye world",
        ""
    ]

    assert expected_output == parser.text


def test_no_matches():
    """
    A test of the parser where there are no matches.
    """

    input_text = [
        r"hello world",
        r"goodbye world",
        "",
    ]

    def colgen_findme(input):
        return Collector(input, r"%%\\findme{.*?}")

    def colgen_lookfor(input):
        return Collector(input, r"%%\\lookfor{.*?}")

    def colgen_thethird(input):
        return Collector(input, r"%%\\thethird{.*?}")

    generators = {
        re.compile(r"%%\\findme{.*?}"): colgen_findme,
        re.compile(r"%%\\lookfor{.*?}"): colgen_lookfor,
        re.compile(r"%%\\thethird{.*?}"): colgen_thethird,
    }

    parser = Parser(input_text, generators)

    expected_output = [
        r"hello world",
        r"goodbye world",
        ""
    ]

    assert expected_output == parser.text


def test_section():
    """
    Unit test for the parser using the collector.

    Not yet implemented: line numbers.
    """

    input_text = [
        r"hello world",
        r"%%\findme{Section}",
        r"goodbye world",
        "",
    ]

    def secgen(input):
        return Section(input, r"%%\\findme{(.*?)}", capture=1)

    generators = {
        re.compile(r"%%\\findme{(.*?)}"): secgen,
    }

    parser = Parser(input_text, generators)

    expected_output = [
        r"hello world",
        "# Section".format(parser.matches[1].uid),
        r"goodbye world",
        ""
    ]

    assert expected_output == parser.text


def test_section_and_collector():
    """
    Unit test for the parser using the collector and the section
    at the same time!

    Not yet implemented: line numbers.
    """

    input_text = [
        r"hello world",
        r"%%\findme{Section}",
        r"%%\findcollector{Collector}",
        r"goodbye world",
        "",
    ]

    def secgen(input):
        return Section(input, r"%%\\findme{(.*?)}", capture=1)

    def colgen(input):
        return Collector(input, r"%%\\findcollector{.*?}")

    generators = {
        re.compile(r"%%\\findme{(.*?)}"): secgen,
        re.compile(r"%%\\findcollector{.*?}"): colgen,
    }

    parser = Parser(input_text, generators)

    expected_output = [
        r"hello world",
        "# {}".format(parser.matches[1].text),
        "<!-- Collector {} -->".format(parser.matches[2].uid),
        r"goodbye world",
        ""
    ]

    assert expected_output == parser.text


def test_removal():
    """
    Unit test for the removal class.
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

    expected_output = [
        r"hello world",
        r"<!--",
        r"THIS IS ONLY FOR THE PDF!",
        r"-->",
        r"goodbye world",
        "",
    ]

    assert parser.text == expected_output

