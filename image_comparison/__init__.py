from importlib.metadata import version

__version__ = version("pylinalg")
version_info = tuple(map(int, __version__.split(".")))

del version

from .image_comparison import *
from .image_processing import *
