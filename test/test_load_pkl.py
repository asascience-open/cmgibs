import matplotlib.cm
import os
import pickle
import unittest

class TestPkl(unittest.TestCase):
    """Test that the cmap_d.pkl file has been shipped with the package, and that
    it loads correctly.
    """
    @classmethod
    def setUpClass(cls):
        """Set stuff up before any tests are run"""
        cls._dir =  os.path.dirname(os.path.abspath('cmgibs/cmgibs'))
        cls._loc_fp = os.path.join(cls._dir, 'cmap_d.pkl')

    def test_check_pkl_exists(self):
        """Check the cmap_d.pkl file exists in cmgibs/cmgibs"""
        try:
            assert os.path.isfile(self._loc_fp)
        except AssertionError:
            m = '"cmap_d.pkl" not in {}; you\'ll need this '.format(self._dir)+\
                'to load the GIBS colormaps.'
            self.fail(m)

    def test_load_pkl(self):
        """Open the .pkl and ensure what's in it is a dict of colormaps"""
        if os.path.isfile(self._loc_fp):
            # load the .pkl
            with open(self._loc_fp, 'rb') as _cmaps:
                cmap_d = pickle.load(_cmaps)
            assert isinstance(cmap_d, dict)
            # test if all the values in cmap_d are matplotlib colormaps
        else:
            # fail the test
            self.fail('Check for cmap_d.pkl in {}'.format(self._dir))

    def test_import_dict(self):
        """Test the import of the cmap_d dictionary of colormaps"""
        try:
            import cmgibs
        except ImportError:
            self.fail()
            raise
        # access the color map dict
        cmaps = cmgibs.cmap_d
        assert isinstance(cmaps, dict)
        # register the color maps; if this passes, we're good
        for name, cmap in cmaps.items():
            matplotlib.cm.register_cmap(name=name, cmap=cmap)
