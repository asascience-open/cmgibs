#!/usr/bin/env python

import lxml.etree
import matplotlib.colors
import numpy as np
import os
import urllib.request

class GibsColormap(object):

    # open the XML schema with urllib, parse it with lxml
    xsd_url = 'https://raw.githubusercontent.com/nasa-gibs/onearth/master/src/colormaps/schemas/ColorMap_v1.3.xsd'
    raw_xsd = urllib.request.urlopen(xsd_url)
    XSD = lxml.etree.XMLSchema(lxml.etree.parse(raw_xsd))

    def __init__(self, req, name):
        """Initialize a GibsColormap object using a given HTTP request and name
        :param urllib request req: Request to a URL containing the colormap XML
        :param str name          : name of the GibsColormap file
        """
        self.name = name
        # open the req with urllib, parse with lxml
        self.doc = lxml.etree.parse(urllib.request.urlopen(req))

        # validate against XSD
        valid = GibsColormap.XSD.validate(self.doc)  # NOTE what are we doing with this?

        self.rgbs = []
        self.values = []

    def parse_range(self, s):
        """
        Parse a string range and convert it to array of floats.
        :param str s: string to parse

        :example
        s = '[-INF,0.00)'

        :returns
        s = [float('-inf'), 0.0]
        """
        try:
            # strip off the leading and trailing enclosures, split on comma
            s = list(map(float, s.lstrip('[, (').rstrip('], )').split(',')))
            # ensure interval to be len 2 when we cast it as a numpy array
            if len(s) < 2:
                # if single entry is negative/0, append 0 to it; likely means
                # this is the first ColorMapEntry tag of the XML
                if s[0] <= 0:
                    s.append(0.0)
                # if entry is positive, append +INF to it; likely means this
                # is the last ColorMapEntry tag of the XML
                if s[0] > 0:
                    s.append(float('inf'))
        except Exception as e:
            print('-'*80)
            print('For file: {:^80}\n'.format(self.name))
            traceback.print_exc()
            print('-'*80)
        return s


    def generate_cmap(self):
        """
        Generate a LinearSegmentedColormap from a GIBS ColorMap XML file. Each
        ColorMapEntry tag is of the form

        ```
        <ColorMapEntry rgb="179,0,2" transparent="false" value="[96,97)" ref="96"/>
        ```

        :notes

        - Ensuring val range is [0, 1] -
        Each RGB component in LinearSegmentedColormap mustbegin at x=0 and end
        at x=1. The values of the colormaps we are parsing do not necessarily
        guarantee this, so we must ensure it by offsetting by the minimum value
        and dividing by the range.
        """
        # get list of all the ColorMapEntry tags
        for e in self.doc.findall('ColorMap'):
            title = e.attrib.get('title', None)
            if title != 'No Data':
                # look for the legend type; if not continuous, we don't even
                # want to use this colormap
                if e.find('Legend').get('type') != 'continuous':
                    return None
                else:
                    cmap_entries = e.getchildren()[0].findall('ColorMapEntry')
                    print('--- Generating color map :{0:>60}:{1:>} ---'.format(self.name, title))
                    break  # we have the colormap we want, break out

        # iterate tags
        for e in cmap_entries:
            if set(['rgb', 'value']).issubset(set(e.keys())):
                # get the rgb vals, split on comma, convert to int, append
                self.rgbs.append(list(map(int, e.get('rgb').split(','))))
                # parse values, make sure they are floats
                val_range = self.parse_range(e.get('value'))
                # if val range not None, append it; else, skip
                if val_range:
                    self.values.append(val_range)
                else:
                    # return a None cmap -- we can't create a cmap with no vals
                    return {None}

        # NOTE if the cmap's final range was improperly formatted and does not
        # end in +INF, we'll need to force it to in order to adhere to the
        # intended color-value scheme
        if self.values[-1][1] != float('inf'):
            # append an additional range value with the first value equal to the
            # end value of the last range --> [lastval, float('inf')]
            self.values.append([self.values[-1][1], float('inf')])

        # ensuring total value range==[0, 1]
        # TODO remove try-except? Reformat?
        try:
            self.values = np.ma.masked_invalid(np.array(self.values))
            if np.ma.is_masked(self.values):
                _min = self.values.min()
                # .ptp() returns range (maximum - minimum) (peak-to-peak)
                rng = self.values.ptp()
                # normalize to [0, 1] range
                self.values = (self.values-_min)/rng
            else:
                # NOTE shouldn't this be doing a different operation?
                _min = self.values.min()
                rng = self.values.ptp()
                self.values = (self.values-_min)/rng

            print('TOTAL RANGE: [{0}, {1}] ({2})'.format(self.values.min(), self.values.max(), rng))

        except Exception:
            print('-'*80)
            print('For file: {:^80}\n'.format(self.name))
            traceback.print_exc()
            print('-'*80)

        # normalize RGB values into a [0, 1] range
        self.rgbs = list(map(lambda l: [x/255.0 for x in l], self.rgbs))

        # because we may have artificially added an extra range value, we must
        # also add another RGB array to match; we will duplicate the last RGB
        # for this, as this was the color intended
        if len(self.rgbs) != len(self.values):
            self.rgbs.append(self.rgbs[-1])

        percentages = []
        set_under = None
        set_over = None

        # find low/high out of range values to set colors for; set the masked
        # value to the non-masked value
        for a in zip(self.values, self.rgbs):
            # percentages.append((a[0][0], a[1]))
            if a[0][0] is np.ma.masked:
                set_under = a[1]
            else:
                percentages.append((a[0][0], a[1]))
            if a[0][1] is np.ma.masked:
                set_over = a[1]

        R = []
        G = []
        B = []

        for p in percentages:
            # assemble tuples of RGB vals
            R.append((p[0], p[1][0], p[1][0]))
            G.append((p[0], p[1][1], p[1][1]))
            B.append((p[0], p[1][2], p[1][2]))
        # zip them and create a dict for LinearSegmentedColormap
        RGB=zip(R,G,B)
        rgb=zip(*RGB)
        k=['red', 'green', 'blue']
        LinearL=dict(zip(k,rgb))

        # make the cmap
        self.cmap = matplotlib.colors.LinearSegmentedColormap(self.name, LinearL)

        # set the out-of-range colors
        if set_under:
            self.cmap.set_under(color=tuple(set_under), alpha=None)
        if set_over:
            self.cmap.set_over(color=tuple(set_over), alpha=None)

        return self.cmap
