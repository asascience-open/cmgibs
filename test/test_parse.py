import os
import unittest
import urllib

from cmgibs.cm import Parser

_url_ = 'https://gibs.earthdata.nasa.gov/colormaps/v1.3/'

class TestParse(unittest.TestCase):
    """Test the ability to parse CMGIBS colormaps from XML.

    # TODO
    Ideally, a unit test would be run on cm.parse() so we wouldn't have to break
    apart the method to test it.
    """

    def test_parse_html(self):
        """Test that the given XML can be parsed correctly.
        """
        with urllib.request.urlopen(_url_) as response:
            # initialize Parser
            parser = Parser()
            # feed it the response; this should create a list of filenames
            parser.feed(response.read().decode())
        assert isinstance(parser.filenames, list)
        # check we actually get valid xml filenames
        assert parser.filenames[0].endswith('.xml')
