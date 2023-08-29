from hPyT import FakeWindowMixin

def get_PyQt5():
    try:
        from PyQt5 import QtWidgets
        
        class MixedWindow(FakeWindowMixin, QtWidgets.QWidget):
            def __init__(self):
                QtWidgets.QWidget.__init__(self)
                FakeWindowMixin.__init__(self)
                
        return MixedWindow
    except ImportError:
        raise ImportError("hPyT import Error : No PyQt5 Enviorment Found")
    
def get_PySide2():
    try:
        from PySide2 import QtWidgets
        
        class MixedWindow(FakeWindowMixin, QtWidgets.QWidget):
            def __init__(self):
                QtWidgets.QWidget.__init__(self)
                FakeWindowMixin.__init__(self)
                
        return MixedWindow
    except ImportError:
        raise ImportError("hPyT import Error : No PySide2 Enviorment Found")
    
def get_customtkinter():
    try:
        from customtkinter import CTk
        
        class MixedWindow(FakeWindowMixin, CTk):
            def __init__(self):
                CTk.__init__(self)
                FakeWindowMixin.__init__(self)
                
        return MixedWindow
    except ImportError:
        raise ImportError("hPyT import Error : No customtkinter Enviorment Found")
    
def get_wxPython():
    try:
        import wx
        
        class MixedWindow(FakeWindowMixin, wx.Frame):
            def __init__(self):
                wx.Frame.__init__(self, parent=None)
                FakeWindowMixin.__init__(self)
                
        return MixedWindow
    except ImportError:
        raise ImportError("hPyT import Error : No wxPython Enviorment Found")