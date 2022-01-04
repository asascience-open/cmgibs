import ssl

ssl._create_default_https_context = ssl._create_unverified_context


from .gibs import GibsColormap
from .cm import cmap_d 

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
