import datetime
import html.parser
import pickle
import os
import urllib.request

from cmgibs import GibsColormap

class Parser(html.parser.HTMLParser):

    def __init__(self):
        super().__init__()
        self.filename = None
        self.filenames = []

    def handle_starttag(self, tag, attrs):
        """Look for HREF tags and grab their link
        :param str tag
        """
        self.filename = None
        if tag == 'a':
            _attrs = dict(attrs)
            if 'href' in _attrs:
                self.filename = _attrs['href']

    def handle_endtag(self, tag):
        if self.filename:
            if '.xml' in self.filename:
                self.filenames.append(self.filename)
            self.filename = None

def parse(url):
    """Parse a given URL for href tags and return the tags?
    :param str url: url string
    """
    _cmaps = dict()
    with urllib.request.urlopen(url) as response:
        # filenames
        parser = Parser()
        parser.feed(response.read().decode())
        print('Number colormaps to parse: {}\n'.format(len(parser.filenames)))
        # return parser.filenames[0]
        for filename in parser.filenames:
            # generate a request, process filename and cmap XML, add it
            req = urllib.request.Request(urllib.parse.urljoin(url, filename))
            filename = filename.replace('.xml', '')
            gibs = GibsColormap(req, filename)
            _cmaps[filename] = gibs.generate_cmap()
    return _cmaps

def load_cmaps():
    """
    Load a dictionary of NASA Gibs color maps from a .pkl file (if present) or
    go to the endpoint and get them and save them as a .pkl.

    :returns: A dict with {name: colormap}
    """
    # check if file exists
    loc_fp = os.path.join(os.getcwd(), 'cmap_d.pkl')
    if os.path.isfile(loc_fp):
        # open file, load it, return it
        with open(loc_fp, 'rb') as _cmaps:
            cmap_d = pickle.load(_cmaps)
            return cmap_d
    else:
        # go to the URL and create the dict
        cmaps_url = 'https://gibs.earthdata.nasa.gov/colormaps/v1.3/'
        cmap_d = parse(cmaps_url)
        # open a new file, pickle the dict, and save
        with open('cmap_d.pkl', 'wb') as f:
            pickle.dump(cmap_d, f)
            return cmap_d

cmap_d = load_cmaps()
cmap_d = {k: v for k, v in cmap_d.items() if v}
locals().update(cmap_d)
