""" Extracts TODO: notes from source code.

See README.md for more intructions on how to run the script.
"""

__version__ = "0.2.1"

from .todo_extractor import search_folder  # noqa
from .cli import main  # noqa
