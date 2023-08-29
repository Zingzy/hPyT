"""
hPyT - Hide Python Titlebar
Author - zingzy
version - 1.0.2
License - MIT
Homepage - https://github.com/zingzy/hPyT
"""

from .hPyT import FakeWindowMixin
from .baseMixedWindows import get_PyQt5, get_PySide2, get_customtkinter, get_wxPython

__all__ = [
    'FakeWindowMixin',
    'get_PyQt5',
    'get_PySide2',
    'get_customtkinter',
    'get_wxPython'
]

__version__ = '1.0.2'
