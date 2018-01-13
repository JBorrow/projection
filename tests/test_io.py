"""
Tests for the IO -- including database tests.
"""

from projection.io import Database
from projection.parser.generators import Collector, Section

import os
import uuid


def test_insertion_extraction():
    """
    Creates a database, puts in a mock Collector and Section object, retrieves
    them and checks if they are the same.
    """

    db = Database("test.db")

    # Create mock objects.
    col = Collector(input="test", regex=".*?", id="keypoint", line=0)
    sec = Section(input="test", regex=".*?", id="section")
    sec.startline = 1
    sec.endline = 3

    db.insert_collector(tuple(col.pack().values()))
    db.insert_section(tuple(sec.pack().values()))

    output_col = db.grab_collectors()[0]
    output_sec = db.grab_sections()[0]

    assert col == output_col
    assert sec == output_sec

    del db

    os.remove("test.db")

