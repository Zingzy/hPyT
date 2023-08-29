try:
    import ctypes
except ImportError:
    raise ImportError("hPtT import Error : No Windows Enviorment Found")

set_window_pos = ctypes.windll.user32.SetWindowPos
set_window_long = ctypes.windll.user32.SetWindowLongPtrW
get_window_long = ctypes.windll.user32.GetWindowLongPtrW
def_window_proc = ctypes.windll.user32.DefWindowProcW

GWL_STYLE = -16

WS_MINIMIZEBOX = 131072
WS_MAXIMIZEBOX = 65536

WS_SYSMENU = 524288

SWP_NOZORDER = 4
SWP_NOMOVE = 2
SWP_NOSIZE = 1
SWP_FRAMECHANGED = 32

WS_CAPTION = 12582912

class FakeWindowMixin:
    """This can be combined with inheritance with an external window class, while implementing the methods of this class."""
    def __init__(self):
        self.hwnd = module_find(self)
        
    def hide_title_bar(self):
        old_style = get_window_long(self.hwnd, GWL_STYLE)
        new_style = old_style & ~ WS_CAPTION
        set_window_long(self.hwnd, GWL_STYLE, new_style)
        set_window_pos(self.hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
        
    def unhide_title_bar(self):
        old_style = get_window_long(self.hwnd, GWL_STYLE)
        new_style = old_style | WS_CAPTION
        set_window_long(self.hwnd, GWL_STYLE, new_style)
        set_window_pos(self.hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
        
    def hide_maximize_minimize_button(self):
        old_style = get_window_long(self.hwnd, GWL_STYLE)
        new_style = old_style & ~ WS_MAXIMIZEBOX & ~ WS_MINIMIZEBOX
        set_window_long(self.hwnd, GWL_STYLE, new_style)
        set_window_pos(self.hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
    
    def unhide_maximize_minimize_button(self):
        old_style = get_window_long(self.hwnd, GWL_STYLE)
        new_style = old_style | WS_MAXIMIZEBOX | WS_MINIMIZEBOX
        set_window_long(self.hwnd, GWL_STYLE, new_style)
        set_window_pos(self.hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
        
    def disable_maximize_button(self):
        old_style = get_window_long(self.hwnd, GWL_STYLE)
        new_style = old_style & ~WS_MAXIMIZEBOX
        set_window_long(self.hwnd, GWL_STYLE, new_style)
        set_window_pos(self.hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
        
    def enable_maximize_button(self):
        old_style = get_window_long(self.hwnd, GWL_STYLE)
        new_style = old_style | WS_MAXIMIZEBOX
        set_window_long(self.hwnd, GWL_STYLE, new_style)
        set_window_pos(self.hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
        
    def disable_minimize_button(self):
        old_style = get_window_long(self.hwnd, GWL_STYLE)
        new_style = old_style & ~WS_MINIMIZEBOX
        set_window_long(self.hwnd, GWL_STYLE, new_style)
        set_window_pos(self.hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
        
    def enable_minimize_button(self):
        old_style = get_window_long(self.hwnd, GWL_STYLE)
        new_style = old_style | WS_MINIMIZEBOX
        set_window_long(self.hwnd, GWL_STYLE, new_style)
        set_window_pos(self.hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
        
    def hide_all(self):
        old_style = get_window_long(self.hwnd, GWL_STYLE)
        new_style = old_style & ~ WS_SYSMENU
        set_window_long(self.hwnd, GWL_STYLE, new_style)
        set_window_pos(self.hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
        
    def unhide_all(self):
        old_style = get_window_long(self.hwnd, GWL_STYLE)
        new_style = old_style | WS_SYSMENU
        set_window_long(self.hwnd, GWL_STYLE, new_style)
        set_window_pos(self.hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
        
    def set_window_pos(self, x, y, width, height):
        set_window_pos(self.hwnd, 0, x, y, width, height, SWP_NOZORDER)
    
    def set_window_size(self, width, height):
        set_window_pos(self.hwnd, 0, 0, 0, width, height, SWP_NOMOVE | SWP_NOZORDER)
        
    def set_window_position(self, x, y):
        set_window_pos(self.hwnd, 0, x, y, 0, 0, SWP_NOSIZE | SWP_NOZORDER)
    
    def set_window_title(self, title):
        ctypes.windll.user32.SetWindowTextW(self.hwnd, title)
        
    def set_window_icon(self, icon):
        ctypes.windll.user32.SendMessageW(self.hwnd, 128, 0, icon)

    def set_window_icon_big(self, icon):
        ctypes.windll.user32.SendMessageW(self.hwnd, 128, 1, icon)

    def set_window_icon_small(self, icon):
        ctypes.windll.user32.SendMessageW(self.hwnd, 128, 1, icon)


def module_find(window):
    try:
        window.update() # for tk
        return ctypes.windll.user32.GetParent(window.winfo_id())
    except:
        pass
    try:
        return window.winId().__int__() # for pyQt
    except:
        pass
    try:
        return window.GetHandle() # for wx
    except:
        pass
    return window    # others / notfound