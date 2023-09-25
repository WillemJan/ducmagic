"""
ducmagic __init__.py

>>> import ducmagic
>>> assert type(ducmagic.load()), dict
"""

from .ducmagic import cli  # noqa
from .ducmagic import load_ducmagic # noqa

__all__ = [
    "load_ducmagic",
    "cli",
    ]
