import math
import threading

try:
    import ctypes
    from ctypes.wintypes import HWND, RECT, UINT
except ImportError:
    raise ImportError("hPyT import Error : No Windows Enviorment Found")

set_window_pos = ctypes.windll.user32.SetWindowPos
set_window_long = ctypes.windll.user32.SetWindowLongPtrW
get_window_long = ctypes.windll.user32.GetWindowLongPtrA
def_window_proc = ctypes.windll.user32.DefWindowProcW
call_window_proc = ctypes.windll.user32.CallWindowProcW
flash_window_ex = ctypes.windll.user32.FlashWindowEx


GWL_STYLE = -16
GWL_EXSTYLE = -20
GWL_WNDPROC = -4

WS_MINIMIZEBOX = 0x00020000
WS_MAXIMIZEBOX = 0x00010000
WS_CAPTION = 0x00C00000
WS_SYSMENU = 0x00080000

WS_EX_LAYERED = 524288

WM_NCCALCSIZE = 0x0083
WM_NCHITTEST = 0x0084

SWP_NOZORDER = 4
SWP_NOMOVE = 2
SWP_NOSIZE = 1
SWP_FRAMECHANGED = 32

LWA_ALPHA = 2

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

class PWINDOWPOS(ctypes.Structure):
    _fields_ = [
        ("hWnd", HWND),
        ("hwndInsertAfter", HWND),
        ("x", ctypes.c_int),
        ("y", ctypes.c_int),
        ("cx", ctypes.c_int),
        ("cy", ctypes.c_int),
        ("flags", UINT),
    ]

class NCCALCSIZE_PARAMS(ctypes.Structure):
    _fields_ = [("rgrc", RECT * 3), ("lppos", ctypes.POINTER(PWINDOWPOS))]

rnbtbs = []
rnbbcs = []
titles = {}

class title_bar:
    @classmethod
    def hide(cls, window) -> None:
        def handle(hwnd: int, msg: int, wp: int, lp: int) -> int:
            if msg == WM_NCCALCSIZE and wp:
                lpncsp = NCCALCSIZE_PARAMS.from_address(lp)
                lpncsp.rgrc[0].top -= 6

            return call_window_proc(*map(ctypes.c_uint64, (globals()[old], hwnd, msg, wp, lp)))

        old, new = "old_wndproc", "new_wndproc"
        prototype = ctypes.WINFUNCTYPE(ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64)

        hwnd = module_find(window)

        globals()[old] = None
        globals()[new] = prototype(handle)
        globals()[old] = get_window_long(hwnd, GWL_WNDPROC)
        set_window_long(hwnd, GWL_WNDPROC, globals()[new])
        
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style & ~ WS_CAPTION
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)

    @classmethod
    def unhide(cls, window) -> None:
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style | WS_CAPTION
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)

class maximize_minimize_button():
    @classmethod
    def hide(cls, window) -> None:
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style & ~ WS_MAXIMIZEBOX & ~ WS_MINIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
    
    @classmethod
    def unhide(cls, window) -> None:
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style | WS_MAXIMIZEBOX | WS_MINIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)

class maximize_button:
    @classmethod
    def disable(cls, window) -> None:
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style & ~WS_MAXIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
    
    @classmethod
    def enable(cls, window) -> None:
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style | WS_MAXIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)

class minimize_button:
    @classmethod
    def disable(cls, window) -> None:
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style & ~WS_MINIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
    
    @classmethod
    def enable(cls, window) -> None:
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style | WS_MINIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)

class all_stuffs():
    @classmethod
    def hide(cls, window) -> None:
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style & ~ WS_SYSMENU
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)

    
    @classmethod
    def unhide(cls, window) -> None:
        hwnd = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style | WS_SYSMENU
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)

class window_flash:
    @classmethod
    def flash(cls, window, count=5, interval=1000) -> None:
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
    def stop(cls, window) -> None:
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
    def set(cls, window, opacity) -> None:
        hwnd = module_find(window)
        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)

        # Opacity is a value between 0 (transparent) and 255 (opaque)
        # If the input is a float between 0.0 and 1.0, convert it to an integer between 0 and 255
        if isinstance(opacity, float) and 0.0 <= opacity <= 1.0:
            opacity = int(opacity * 255)

        ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, opacity, LWA_ALPHA)

class title_bar_color:
    @classmethod
    def set(cls, window, color) -> None:
        color = convert_color(color)
        hwnd = module_find(window)
        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(ctypes.c_int(color)), 4)
        set_window_long(hwnd, GWL_EXSTYLE, old_ex_style)  # Reset the window style

    @classmethod
    def reset(cls, window) -> None:
        hwnd = module_find(window)
        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(ctypes.c_int(-1)), 4)
        set_window_long(hwnd, GWL_EXSTYLE, old_ex_style)

class title_bar_text_color:
    @classmethod
    def set(cls, window, color) -> None:
        color = convert_color(color)
        hwnd = module_find(window)
        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 36, ctypes.byref(ctypes.c_int(color)), 4)
        set_window_long(hwnd, GWL_EXSTYLE, old_ex_style)  # Reset the window style

    @classmethod
    def reset(cls, window) -> None:
        hwnd = module_find(window)
        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 36, ctypes.byref(ctypes.c_int(-1)), 4)
        set_window_long(hwnd, GWL_EXSTYLE, old_ex_style)

class border_color:
    @classmethod
    def set(cls, window, color) -> None:
        color = convert_color(color)
        hwnd = module_find(window)
        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 34, ctypes.byref(ctypes.c_int(color)), 4)
        set_window_long(hwnd, GWL_EXSTYLE, old_ex_style)  # Reset the window style

    @classmethod
    def reset(cls, window) -> None:
        hwnd = module_find(window)
        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 34, ctypes.byref(ctypes.c_int(-1)), 4)
        set_window_long(hwnd, GWL_EXSTYLE, old_ex_style)

class rainbow_title_bar:
    current_color = None

    @classmethod
    def start(cls, window, interval=5, color_stops=5) -> None:
        def color_changer(hwnd, interval):
            r, g, b = 200, 0, 0
            while hwnd in rnbtbs:
                cls.current_color = (r << 16) | (g << 8) | b

                ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(ctypes.c_int(cls.current_color)), 4)
                if r < 255 and g == 0 and b == 0:
                    r = min(255, r + color_stops)
                elif r == 255 and g < 255 and b == 0:
                    g = min(255, g + color_stops)
                elif r > 0 and g == 255 and b == 0:
                    r = max(0, r - color_stops)
                elif g == 255 and b < 255 and r == 0:
                    b = min(255, b + color_stops)
                elif g > 0 and b == 255 and r == 0:
                    g = max(0, g - color_stops)
                elif b == 255 and r < 255 and g == 0:
                    r = min(255, r + color_stops)
                elif b > 0 and r == 255 and g == 0:
                    b = max(0, b - color_stops)
                ctypes.windll.kernel32.Sleep(interval)
            else:
                ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(ctypes.c_int(-1)), 4)

        hwnd = module_find(window)
        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)

        rnbtbs.append(hwnd)
        thread = threading.Thread(target=color_changer, args=(hwnd, interval))
        thread.daemon = True
        thread.start()

        set_window_long(hwnd, GWL_EXSTYLE, old_ex_style)  # Reset the window style

    @classmethod
    def get_current_color(cls):
        color = cls.current_color
        b = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        r = color & 0xFF
        return (r, g, b)

    @classmethod
    def stop(cls, window) -> None:
        hwnd = module_find(window)
        if hwnd in rnbtbs:
            rnbtbs.remove(hwnd)
        else:
            raise ValueError('Rainbow title bar is not running on this window.')

class rainbow_border:
    current_color = None

    @classmethod
    def start(cls, window, interval=5, color_stops=5) -> None:
        def color_changer(hwnd, interval):
            r, g, b = 200, 0, 0
            while hwnd in rnbbcs:
                cls.current_color = (r << 16) | (g << 8) | b

                ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 34, ctypes.byref(ctypes.c_int(cls.current_color)), 4)
                if r < 255 and g == 0 and b == 0:
                    r = min(255, r + color_stops)
                elif r == 255 and g < 255 and b == 0:
                    g = min(255, g + color_stops)
                elif r > 0 and g == 255 and b == 0:
                    r = max(0, r - color_stops)
                elif g == 255 and b < 255 and r == 0:
                    b = min(255, b + color_stops)
                elif g > 0 and b == 255 and r == 0:
                    g = max(0, g - color_stops)
                elif b == 255 and r < 255 and g == 0:
                    r = min(255, r + color_stops)
                elif b > 0 and r == 255 and g == 0:
                    b = max(0, b - color_stops)
                ctypes.windll.kernel32.Sleep(interval)
            else:
                ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 34, ctypes.byref(ctypes.c_int(-1)), 4)

        hwnd = module_find(window)
        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)

        rnbbcs.append(hwnd)
        thread = threading.Thread(target=color_changer, args=(hwnd, interval))
        thread.daemon = True
        thread.start()

        set_window_long(hwnd, GWL_EXSTYLE, old_ex_style)  # Reset the window style

    @classmethod
    def get_current_color(cls):
        color = cls.current_color
        b = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        r = color & 0xFF
        return (r, g, b)

    @classmethod
    def stop(cls, window) -> None:
        hwnd = module_find(window)
        if hwnd in rnbbcs:
            rnbbcs.remove(hwnd)
        else:
            raise ValueError('Rainbow border is not running on this window.')

class window_frame:
    @classmethod
    def center(cls, window) -> None:
        hwnd = module_find(window)

        # Get the window's current position and size
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        window_width = rect.right - rect.left
        window_height = rect.bottom - rect.top

        # Get the screen's width and height
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)

        # Calculate the new position
        new_x = (screen_width - window_width) // 2
        new_y = (screen_height - window_height) // 2

        # Set the window's new position
        ctypes.windll.user32.SetWindowPos(hwnd, 0, new_x, new_y, 0, 0, 0x0001)

    @classmethod
    def center_relative(cls, window_parent, window_child) -> None:
        hwnd_parent = module_find(window_parent)
        hwnd_child = module_find(window_child)

        # Get the parent window's current position and size
        rect_parent = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd_parent, ctypes.byref(rect_parent))
        parent_width = rect_parent.right - rect_parent.left
        parent_height = rect_parent.bottom - rect_parent.top

        # Get the child window's current position and size
        rect_child = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd_child, ctypes.byref(rect_child))
        child_width = rect_child.right - rect_child.left
        child_height = rect_child.bottom - rect_child.top

        # Calculate the new position
        new_x = rect_parent.left + (parent_width - child_width) // 2
        new_y = rect_parent.top + (parent_height - child_height) // 2

        # Set the child window's new position
        ctypes.windll.user32.SetWindowPos(hwnd_child, 0, new_x, new_y, 0, 0, 0x0001)

    @classmethod
    def move(cls, window, x, y) -> None:
        hwnd = module_find(window)
        set_window_pos(hwnd, 0, x, y, 0, 0, 0x0001)

    @classmethod
    def resize(cls, window, width, height) -> None:
        hwnd = module_find(window)
        set_window_pos(hwnd, 0, 0, 0, width, height, 0x0001)

    @classmethod
    def minimize(cls, window) -> None:
        hwnd = module_find(window)
        ctypes.windll.user32.ShowWindow(hwnd, 6)

    @classmethod
    def maximize(cls, window) -> None:
        hwnd = module_find(window)
        ctypes.windll.user32.ShowWindow(hwnd, 3)

    @classmethod
    def restore(cls, window) -> None:
        hwnd = module_find(window)
        ctypes.windll.user32.ShowWindow(hwnd, 9)

class window_animation:
    @classmethod
    def circle_motion(cls, window, count=5, interval=5, radius=20) -> None:
        def motion():
            hwnd = module_find(window)
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            original_x = rect.left
            original_y = rect.top
            for angle in range(0, 360 * count, 5):  # move in a circle count times
                rad = math.radians(angle)
                x = original_x + int(radius * math.cos(rad))
                y = original_y + int(radius * math.sin(rad))
                ctypes.windll.user32.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0001)
                ctypes.windll.kernel32.Sleep(interval)

        thread = threading.Thread(target=motion)
        thread.daemon = True
        thread.start()

    @classmethod
    def vertical_shake(cls, window, count=5, interval=3, amplitude=20) -> None:
        def motion():
            hwnd = module_find(window)
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            original_y = rect.top
            for offset in range(0, 360 * count, count):  # move up and down 5 times
                rad = math.radians(offset)
                y = original_y + int(amplitude * math.sin(rad))
                ctypes.windll.user32.SetWindowPos(hwnd, 0, rect.left, y, 0, 0, 0x0001)
                ctypes.windll.kernel32.Sleep(interval)

        thread = threading.Thread(target=motion)
        thread.daemon = True
        thread.start()

    @classmethod
    def horizontal_shake(cls, window, count=5, interval=3, amplitude=20) -> None:
        def motion():
            hwnd = module_find(window)
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            original_x = rect.left
            for offset in range(0, 360 * count, count):  # move left and right 5 times
                rad = math.radians(offset)
                x = original_x + int(amplitude * math.sin(rad))
                ctypes.windll.user32.SetWindowPos(hwnd, 0, x, rect.top, 0, 0, 0x0001)
                ctypes.windll.kernel32.Sleep(interval)

        thread = threading.Thread(target=motion)
        thread.daemon = True
        thread.start()

class title_text:
    @classmethod
    def set(cls, window, title) -> None:
        hwnd = module_find(window)
        ctypes.windll.user32.SetWindowTextW(hwnd, title)

    @classmethod
    def stylize(cls, window, style=1) -> None:
        hwnd = module_find(window)
        if hwnd not in titles:
            title = ctypes.create_unicode_buffer(1024)
            ctypes.windll.user32.GetWindowTextW(hwnd, title, 1024)
            titles[hwnd] = title.value
        title = stylize_text(titles[hwnd], style)
        ctypes.windll.user32.SetWindowTextW(hwnd, title)

    @classmethod
    def reset(cls, window) -> None:
        hwnd = module_find(window)
        if hwnd in titles:
            ctypes.windll.user32.SetWindowTextW(hwnd, titles[hwnd])
            del titles[hwnd]

def stylize_text(text: str, style: int) -> str:
    normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    styles = [
        "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ1234567890",
        "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅1234567890",
        "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩1234567890",
        "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢",
        "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉1234567890",
        "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ①②③④⑤⑥⑦⑧⑨⓪",
        "ᗩᗷᑕᗪEᖴGᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭YᘔᗩᗷᑕᗪEᖴGᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭Yᘔ1234567890",
        "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘",
        "₳฿₵ĐɆ₣₲ⱧłJ₭Ⱡ₥₦Ø₱QⱤ₴₮ɄV₩ӾɎⱫ₳฿₵ĐɆ₣₲ⱧłJ₭Ⱡ₥₦Ø₱QⱤ₴₮ɄV₩ӾɎⱫ1234567890",
        "卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙1234567890"
    ]

    if style < 1 or style > len(styles):
        raise ValueError("Invalid style number")

    translation_table = str.maketrans(normal, styles[style - 1])
    return text.translate(translation_table)

def convert_color(color: tuple) -> int:
    if isinstance(color, tuple) and len(color) == 3:  # RGB format
        r, g, b = color
        return int(f"{b}{g}{r}", 16)
    elif isinstance(color, str) and color.startswith('#'):  # HEX format
        r, g, b = color[1:3], color[3:5], color[5:7]
        return int(f"{b}{g}{r}", 16)
    else:
        raise ValueError('Invalid color format. Expected RGB tuple or HEX string.')

def module_find(window) -> int:
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
    try:
        return window.root_window.get_window_info().window # for kivy
    except:
        pass

    return window    # others / notfound