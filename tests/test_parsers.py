"""
Tests for the parser.

This can be found in objects.py.
"""

from parser.objects import Parser
from parser.generators import Collector

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

