from cmgibs.cm import Parser
import cmgibs.gibs
import matplotlib.cm
import unittest
import urllib

class TestBuildCmap(unittest.TestCase):
    """Check if GibColormap can successfully create a colormap given a GIBS .xml
    file."""

    _url_ = 'https://gibs.earthdata.nasa.gov/colormaps/v1.3/'

    @classmethod
    def setUpClass(cls):
        """Set up the expensive stuff"""
        with urllib.request.urlopen(cls._url_) as response:
            # initialize Parser
            parser = Parser()
            # feed it the response; this should create a list of filenames
            parser.feed(response.read().decode())
        # get the first file -- only need to test one
        _fn = parser.filenames[0]
        # create request and replace .xml
        cls._req = urllib.request.Request(urllib.parse.urljoin(cls._url_, _fn))
        cls._fn = _fn.replace('.xml', '')

    def test_build_cmap(self):
        """Build a colormap"""
        gibs = cmgibs.gibs.GibsColormap(self._req, self._fn)
        cmap = gibs.generate_cmap()
        assert isinstance(cmap, matplotlib.colors.LinearSegmentedColormap)
