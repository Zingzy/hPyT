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

GWL_EXSTYLE = -20
WS_EX_LAYERED = 524288
LWA_ALPHA = 2

WS_CAPTION = 12582912

FLASHW_STOP = 0
FLASHW_CAPTION = 1
FLASHW_TRAY = 2
FLASHW_ALL = 3
FLASHW_TIMER = 4
FLASHW_TIMERNOFG = 12

class FLASHWINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint),
                ("hwnd", ctypes.c_void_p),
                ("dwFlags", ctypes.c_uint),
                ("uCount", ctypes.c_uint),
                ("dwTimeout", ctypes.c_uint)]

flash_window_ex = ctypes.windll.user32.FlashWindowEx

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

class window_flash:
    @classmethod
    def flash(cls, window, count=5, interval=0):
        hwnd = module_find(window)
        info = FLASHWINFO(
            cbSize=ctypes.sizeof(FLASHWINFO),
            hwnd=hwnd,
            dwFlags=FLASHW_ALL | FLASHW_TIMER,
            uCount=count,
            dwTimeout=interval
        )
        flash_window_ex(ctypes.pointer(info))

    @classmethod
    def stop(cls, window):
        hwnd = module_find(window)
        info = FLASHWINFO(
            cbSize=ctypes.sizeof(FLASHWINFO),
            hwnd=hwnd,
            dwFlags=FLASHW_STOP,
            uCount=0,
            dwTimeout=0
        )
        flash_window_ex(ctypes.pointer(info))

class opacity():
    @classmethod
    def set(cls, window, opacity):
        hwnd = module_find(window)
        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)

        # Opacity is a value between 0 (transparent) and 255 (opaque)
        # If the input is a float between 0.0 and 1.0, convert it to an integer between 0 and 255
        if isinstance(opacity, float) and 0.0 <= opacity <= 1.0:
            opacity = int(opacity * 255)

        ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, opacity, LWA_ALPHA)

class icon:
    @classmethod
    def set(cls, window, icon_path):
        hwnd = module_find(window)
        ctypes.windll.user32.SendMessageW(hwnd, 128, 1, icon_path)

def module_find(window):
    try:
        window.update() # for tk
        return ctypes.windll.user32.GetParent(window.winfo_id())
    except:
        pass
    try:
        return window.winId().__int__() # for pyQt and PySide
    except:
        pass
    try:
        return window.GetHandle() # for wx
    except:
        pass
    try:
        gdk_window = window.get_window() # for PyGTK
        return gdk_window.get_xid()
    except:
        pass
    return window    # others / notfound