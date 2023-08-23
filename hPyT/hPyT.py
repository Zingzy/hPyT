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

class title_bar:
    @classmethod
    def hide(cls, window):
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style & ~ WS_CAPTION
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
    
    @classmethod
    def unhide(cls, window):
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style | WS_CAPTION
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)

class maximize_minimize_button():
    @classmethod
    def hide(cls, window):
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style & ~ WS_MAXIMIZEBOX & ~ WS_MINIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
    
    @classmethod
    def unhide(cls, window):
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style | WS_MAXIMIZEBOX | WS_MINIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)

class maximize_button:
    @classmethod
    def disable(cls, window):
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style & ~WS_MAXIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
    
    @classmethod
    def enable(cls, window):
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style | WS_MAXIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)

class minimize_button:
    @classmethod
    def disable(cls, window):
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style & ~WS_MINIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
    
    @classmethod
    def enable(cls, window):
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style | WS_MINIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)

class all_stuffs():
    @classmethod
    def hide(cls, window):
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style & ~ WS_SYSMENU
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
    
    @classmethod
    def unhide(cls, window):
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style | WS_SYSMENU
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)

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