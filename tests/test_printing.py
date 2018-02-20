"""
Tests the pretty-printing functions.
"""

from projection.frontend.printing import print_collectors
from projection.parser.generators import Collector, Section

import re


def test_print_collectors():
    """
    Tests frontend.printing.print_collectors.
    """

    input_text = [
        r"%%\findme{collector}",
        r"%%\findme{collector1}",
        r"%%\findme{collector2}",
    ]

    def colgen(input):
        return Collector(input, r"%%\\findme{(.*?)}", capture=1)

    collectors = list(map(colgen, input_text))

    output = print_collectors(collectors)

    expected_output = """<ul>
<li>collector</li>
<li>collector1</li>
<li>collector2</li>
</ul>"""

    print(output)

    assert expected_output == output


