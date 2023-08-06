"""Top-level package of w7x."""

__author__ = """Daniel Böckenhoff"""
__email__ = "dboe@ipp.mpg.de"
__version__ = "0.3.6"
import pathlib

__built__ = not pathlib.Path(__file__, "..", "..", "setup.py").resolve().exists()
from . import compatibility

# from . import simulation
# from . import diagnostic
from .switches import distribute, stateful, exposed
from . import core
from . import model
from . import config
from . import lib
from . import plotting

from .state import (
    State,
    StateComponent,
    StateComposite,
    StateLeaf,
)
from .core import (
    node,
    dependencies,
    compute,
    start_scheduler,
)
