"""
ducmagic __init__.py

>>> import ducmagic
>>> assert type(ducmagic.load()), dict
"""

from .ducmagic import cli  # noqa
from .ducmagic import load_ducmagic as load  # noqa

__all__ = [
    "load",
    "cli",
    ]
