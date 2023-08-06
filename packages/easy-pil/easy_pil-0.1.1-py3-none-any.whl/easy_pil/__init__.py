from collections import namedtuple
from .canvas import Canvas
from .editor import Editor
from .font import Font
from .text import Text
from .utils import run_in_executor, load_image, load_image_async

__version__ = "0.1.1"
VersionInfo = namedtuple("VersionInfo", "major minor macro release")

version_info = VersionInfo(0, 1, 1, "stable")
