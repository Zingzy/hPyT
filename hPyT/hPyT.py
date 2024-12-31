import math
import threading
import time
from typing import Any, Tuple, Union, List, Dict

try:
    import ctypes
    from ctypes.wintypes import HWND, RECT, UINT
    import winreg
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
WS_BORDER = 0x00800000

WS_EX_LAYERED = 524288

WM_NCCALCSIZE = 0x0083
WM_NCHITTEST = 0x0084

WM_NCACTIVATE = 0x0086
WM_NCPAINT = 0x0085

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
    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("hwnd", ctypes.c_void_p),
        ("dwFlags", ctypes.c_uint),
        ("uCount", ctypes.c_uint),
        ("dwTimeout", ctypes.c_uint),
    ]


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


rnbtbs: List[int] = []
rnbbcs: List[int] = []
accent_color_titlebars: List[int] = []
accent_color_borders: List[int] = []
titles: dict = {}


class title_bar:
    """Hide or unhide the title bar of a window."""

    _height_reduction: Dict[
        int, int
    ] = {}  # To track the height reduction applied for each window

    @classmethod
    def hide(cls, window: Any, no_span: bool = False) -> None:
        """
        Hide the title bar of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
            no_span (bool): Whether to resize the window to fit the content area only. Default is False.
        """

        def handle(hwnd: int, msg: int, wp: int, lp: int) -> int:
            if msg == WM_NCCALCSIZE and wp:
                # Adjust the non-client area (title bar) size
                # Here we are basically removing the top border (because the title bar in windows is made of 2 components: the actual titlebar and the border, both having same color)
                lpncsp = NCCALCSIZE_PARAMS.from_address(lp)
                lpncsp.rgrc[0].top -= border_width  # Reduce the height of the title bar

            elif msg in [WM_NCACTIVATE, WM_NCPAINT]:
                # Prevent Windows from drawing the title bar when the window is activated or painted
                # Here we are telling windows not to draw border when the window is switched
                return 1  # Tell Windows not to process further

            # Default processing for other messages
            return call_window_proc(
                *map(ctypes.c_uint64, (globals()[old], hwnd, msg, wp, lp))
            )

        old, new = "old_wndproc", "new_wndproc"
        prototype = ctypes.WINFUNCTYPE(
            ctypes.c_uint64,
            ctypes.c_uint64,
            ctypes.c_uint64,
            ctypes.c_uint64,
            ctypes.c_uint64,
        )

        hwnd: int = module_find(window)

        # Get the window and client dimensions
        rect = RECT()
        client_rect = RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        ctypes.windll.user32.GetClientRect(hwnd, ctypes.byref(client_rect))

        full_width: int = rect.right - rect.left
        full_height: int = rect.bottom - rect.top
        client_width: int = client_rect.right
        client_height: int = client_rect.bottom

        # Calculate the border width and title bar height
        border_width: int = (full_width - client_width) // 2
        title_bar_height: int = full_height - client_height - border_width

        # Override the window procedure if not already done
        if globals().get(old) is None:
            globals()[old] = get_window_long(hwnd, GWL_WNDPROC)

        globals()[new] = prototype(handle)
        set_window_long(hwnd, GWL_WNDPROC, globals()[new])

        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = (old_style & ~WS_CAPTION) | WS_BORDER
        set_window_long(hwnd, GWL_STYLE, new_style)

        if no_span:
            cls._height_reduction[hwnd] = title_bar_height
            set_window_pos(
                hwnd,
                0,
                0,
                0,
                full_width,
                full_height - title_bar_height,
                SWP_NOZORDER | SWP_NOMOVE,
            )
            return

        set_window_pos(
            hwnd,
            0,
            0,
            0,
            0,
            0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED,
        )

    @classmethod
    def unhide(cls, window: Any) -> None:
        """
        Unhide the title bar of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)

        if globals().get("old_wndproc") is not None:
            set_window_long(hwnd, GWL_WNDPROC, globals()["old_wndproc"])
            globals()["old_wndproc"] = None

        # Restore the original height if no_span was used
        height_reduction: int = cls._height_reduction.pop(hwnd, 0)

        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style | WS_CAPTION
        set_window_long(hwnd, GWL_STYLE, new_style)

        if height_reduction:
            rect = RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            set_window_pos(
                hwnd,
                0,
                0,
                0,
                rect.right - rect.left,
                rect.bottom - rect.top + height_reduction,
                SWP_NOZORDER | SWP_NOMOVE,
            )
            return

        set_window_pos(
            hwnd,
            0,
            0,
            0,
            0,
            0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED,
        )


class maximize_minimize_button:
    """Hide or unhide both the maximize and minimize buttons of a window."""

    @classmethod
    def hide(cls, window: Any) -> None:
        """
        Hide both the maximize and minimize buttons of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style & ~WS_MAXIMIZEBOX & ~WS_MINIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(
            hwnd,
            0,
            0,
            0,
            0,
            0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED,
        )

    @classmethod
    def unhide(cls, window: Any) -> None:
        """
        Unhide both the maximize and minimize buttons of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style | WS_MAXIMIZEBOX | WS_MINIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(
            hwnd,
            0,
            0,
            0,
            0,
            0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED,
        )


class maximize_button:
    """Enable or Disable only the maximize button of a window."""

    @classmethod
    def disable(cls, window: Any) -> None:
        """
        Disable the maximize button of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style & ~WS_MAXIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(
            hwnd,
            0,
            0,
            0,
            0,
            0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED,
        )

    @classmethod
    def enable(cls, window: Any) -> None:
        """
        Enable the maximize button of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style | WS_MAXIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(
            hwnd,
            0,
            0,
            0,
            0,
            0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED,
        )


class minimize_button:
    """Enable or Disable only the minimize button of a window."""

    @classmethod
    def disable(cls, window: Any) -> None:
        """
        Disable the minimize button of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style & ~WS_MINIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(
            hwnd,
            0,
            0,
            0,
            0,
            0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED,
        )

    @classmethod
    def enable(cls, window: Any) -> None:
        """
        Enable the minimize button of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style | WS_MINIMIZEBOX
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(
            hwnd,
            0,
            0,
            0,
            0,
            0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED,
        )


class all_stuffs:
    """Hide or unhide all the buttons, icon and title of a window."""

    @classmethod
    def hide(cls, window: Any) -> None:
        """
        Hide all the buttons, icon and title of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style & ~WS_SYSMENU
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(
            hwnd,
            0,
            0,
            0,
            0,
            0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED,
        )

    @classmethod
    def unhide(cls, window: Any) -> None:
        """
        Unhide all the buttons, icon and title of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)
        old_style = get_window_long(hwnd, GWL_STYLE)
        new_style = old_style | WS_SYSMENU
        set_window_long(hwnd, GWL_STYLE, new_style)
        set_window_pos(
            hwnd,
            0,
            0,
            0,
            0,
            0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED,
        )


class window_flash:
    """Adds a flashing simulation to a window, which is useful for alerting the user or grabbing their attention."""

    @classmethod
    def flash(cls, window: Any, count: int = 5, interval: int = 1000) -> None:
        """
        Flash the specified window.

        Args:
            window (object): The window object to flash (e.g., a Tk instance in Tkinter).
            count (int): The number of times to flash the window. Default is 5.
            interval (int): The interval between each flash in milliseconds. Default is 1000.

        Example:
            >>> window_flash.flash(window, count=10, interval=500)
        """

        hwnd: int = module_find(window)
        info = FLASHWINFO(
            cbSize=ctypes.sizeof(FLASHWINFO),
            hwnd=hwnd,
            dwFlags=FLASHW_ALL | FLASHW_TIMER,
            uCount=count,
            dwTimeout=interval,
        )
        flash_window_ex(ctypes.pointer(info))

    @classmethod
    def stop(cls, window: Any) -> None:
        """
        Stop the flashing simulation of the specified window immediately.

        Args:
            window (object): The window object to stop flashing (e.g., a Tk instance in Tkinter).

        Example:
            >>> window_flash.flash(window, count=20, interval=1000)
            >>> time.sleep(5)
            >>> window_flash.stop(window)
        """

        hwnd: int = module_find(window)
        info = FLASHWINFO(
            cbSize=ctypes.sizeof(FLASHWINFO),
            hwnd=hwnd,
            dwFlags=FLASHW_STOP,
            uCount=0,
            dwTimeout=0,
        )
        flash_window_ex(ctypes.pointer(info))


class opacity:
    """Change the opacity of the specified window."""

    @classmethod
    def set(cls, window: Any, opacity: float) -> None:
        """
        Set the opacity of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
            opacity (int/float): The opacity value to set. It should be a value between 0 (transparent) and 1 (opaque).

        Example:
            >>> opacity.set(window, 0.5) # sets the window opacity to 50%
            >>> opacity.set(window, 1) # sets the window opacity to 100% (oppaque)
        """

        hwnd: int = module_find(window)
        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)

        # Opacity is a value between 0 (transparent) and 255 (opaque)
        # If the input is a float between 0.0 and 1.0, convert it to an integer between 0 and 255
        if isinstance(opacity, float) and 0.0 <= opacity <= 1.0:
            opacity = int(opacity * 255)

        ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, opacity, LWA_ALPHA)


class title_bar_color:
    """Change the color of the title bar of a window."""

    @classmethod
    def set(cls, window: Any, color: Union[Tuple[int, int, int], str]) -> None:
        """
        Set the color of the title bar of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
            color (tuple/string): The RGB or HEX color value to set. It can be a tuple of integers (e.g., (255, 0, 0)) or a HEX string (e.g., "#FF0000").

        Example:
            >>> title_bar_color.set(window, (255, 0, 0))
        """

        converted_color: int = convert_color(color)
        hwnd: int = module_find(window)
        if hwnd in accent_color_titlebars:
            accent_color_titlebars.remove(hwnd)
        if hwnd in rnbtbs:
            raise RuntimeError(
                "Failed to change the title bar color. Please stop the rainbow titlebar effect using the `stop()` function."
            )

        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, 35, ctypes.byref(ctypes.c_int(converted_color)), 4
        )
        set_window_long(hwnd, GWL_EXSTYLE, old_ex_style)  # Reset the window style

    @classmethod
    def set_accent(cls, window: Any) -> None:
        """
        Set the color of the title bar of the specified window to the system accent color.

        Args:
            window (object): The window objec   t to modify (e.g., a Tk instance in Tkinter).
        """

        def set_titlebar_color_accent(hwnd) -> None:
            old_accent: str = "#000000"

            while hwnd in accent_color_titlebars:
                if old_accent != get_accent_color():
                    color: int = convert_color(get_accent_color())
                    old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
                    new_ex_style = old_ex_style | WS_EX_LAYERED
                    set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        hwnd, 35, ctypes.byref(ctypes.c_int(color)), 4
                    )
                    set_window_long(
                        hwnd, GWL_EXSTYLE, old_ex_style
                    )  # Reset the window style

                    old_accent = get_accent_color()

                time.sleep(1)

        hwnd: int = module_find(window)
        if hwnd in rnbtbs:
            raise RuntimeError(
                "Failed to change the title bar color. Please stop the rainbow titlebar effect using the `stop()` function."
            )

        if hwnd not in accent_color_titlebars:
            accent_color_titlebars.append(hwnd)
            thread = threading.Thread(
                target=set_titlebar_color_accent, args=(hwnd,), daemon=True
            )
            thread.start()
        else:
            raise RuntimeError(
                "The titlebar's color of the specified window is already set to the accent color."
            )

    @classmethod
    def reset(cls, window: Any) -> None:
        """
        Reset the color of the title bar of the specified window to the default theme.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)
        if hwnd in accent_color_titlebars:
            accent_color_titlebars.remove(hwnd)
        if hwnd in rnbtbs:
            raise RuntimeError(
                "Failed to reset the title bar color. Please stop the rainbow titlebar effect using the `stop()` function."
            )

        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, 35, ctypes.byref(ctypes.c_int(-1)), 4
        )
        set_window_long(hwnd, GWL_EXSTYLE, old_ex_style)


class title_bar_text_color:
    """Change the color of the title bar text of a window."""

    @classmethod
    def set(cls, window, color: Union[Tuple[int, int, int], str]) -> None:
        """
        Set the color of the title bar text of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
            color (tuple/string): The RGB or HEX color value to set. It can be a tuple of integers (e.g., (255, 0, 0)) or a HEX string (e.g., "#FF0000").

        Example:
            >>> title_bar_text_color.set(window, (255, 0, 0))
        """

        converted_color: int = convert_color(color)
        hwnd: int = module_find(window)
        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, 36, ctypes.byref(ctypes.c_int(converted_color)), 4
        )
        set_window_long(hwnd, GWL_EXSTYLE, old_ex_style)  # Reset the window style

    @classmethod
    def reset(cls, window: Any) -> None:
        """
        Reset the color of the title bar text of the specified window to the default color.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)
        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, 36, ctypes.byref(ctypes.c_int(-1)), 4
        )
        set_window_long(hwnd, GWL_EXSTYLE, old_ex_style)


class border_color:
    """Change the color of the border of a window."""

    @classmethod
    def set(cls, window: Any, color: Union[Tuple[int, int, int], str]) -> None:
        """
        Set the color of the border of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
            color (tuple/string): The RGB or HEX color value to set. It can be a tuple of integers (e.g., (255, 0, 0)) or a HEX string (e.g., "#FF0000").

        Example:
            >>> border_color.set(window, (255, 0, 0))
        """

        converted_color: int = convert_color(color)
        hwnd: int = module_find(window)
        if hwnd in accent_color_borders:
            accent_color_borders.remove(hwnd)
        if hwnd in rnbbcs:
            raise RuntimeError(
                "Failed to change the border color. Please stop the rainbow border effect using the `stop()` function."
            )

        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, 34, ctypes.byref(ctypes.c_int(converted_color)), 4
        )
        set_window_long(hwnd, GWL_EXSTYLE, old_ex_style)  # Reset the window style

    @classmethod
    def set_accent(cls, window: Any) -> None:
        """
        Set the color of the border of the specified window to the system accent color.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
        """

        def set_border_color_accent(hwnd) -> None:
            old_accent: str = "#000000"

            while hwnd in accent_color_borders:
                if not old_accent == get_accent_color():
                    color = convert_color(get_accent_color())
                    old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
                    new_ex_style = old_ex_style | WS_EX_LAYERED
                    set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        hwnd, 34, ctypes.byref(ctypes.c_int(color)), 4
                    )
                    set_window_long(
                        hwnd, GWL_EXSTYLE, old_ex_style
                    )  # Reset the window style

                    old_accent = get_accent_color()

                time.sleep(1)

        hwnd: int = module_find(window)
        if hwnd in rnbbcs:
            raise RuntimeError(
                "Failed to change the border color. Please stop the rainbow border effect using the `stop()` function."
            )

        if hwnd not in accent_color_borders:
            accent_color_borders.append(hwnd)
            thread = threading.Thread(
                target=set_border_color_accent, args=(hwnd,), daemon=True
            )
            thread.start()
        else:
            raise RuntimeError(
                "The border's color of the specified window is already set to the accent color."
            )

    @classmethod
    def reset(cls, window: Any) -> None:
        """
        Reset the color of the border of the specified window to the default color.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)
        if hwnd in accent_color_borders:
            accent_color_borders.remove(hwnd)
        if hwnd in rnbbcs:
            raise RuntimeError(
                "Failed to reset the border color. Please stop the rainbow border effect using the `stop()` function."
            )

        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, 34, ctypes.byref(ctypes.c_int(-1)), 4
        )
        set_window_long(hwnd, GWL_EXSTYLE, old_ex_style)


class rainbow_title_bar:
    """Add a rainbow effect to the title bar of a window."""

    current_color = None

    @classmethod
    def start(cls, window: Any, interval: int = 5, color_stops: int = 5) -> None:
        """
        Start the rainbow effect on the title bar of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
            interval (int): The interval between each color change in milliseconds. Default is 5.
            color_stops (int): The number of color stops between each RGB value. Default is 5.

        Example:
            >>> rainbow_title_bar.start(window, interval=10, color_stops=10)

        Notes:
            The `interval` parameter controls the speed of the rainbow effect, and the `color_stops` parameter controls the number of color stops between each RGB value.
            Higher values for `interval` will result in a slower rainbow effect.
            Higher values for `color_stops` might skip most of the colors defying the purpose of the rainbow effect.
        """

        def color_changer(hwnd: int, interval: int) -> None:
            r, g, b = 200, 0, 0
            while hwnd in rnbtbs:
                cls.current_color = (r << 16) | (g << 8) | b

                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, 35, ctypes.byref(ctypes.c_int(cls.current_color)), 4
                )
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
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, 35, ctypes.byref(ctypes.c_int(-1)), 4
                )

        hwnd: int = module_find(window)
        if hwnd in accent_color_titlebars:
            accent_color_titlebars.remove(hwnd)

        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)

        if hwnd not in rnbtbs:
            rnbtbs.append(hwnd)
            thread = threading.Thread(target=color_changer, args=(hwnd, interval))
            thread.daemon = True
            thread.start()
        else:
            raise RuntimeError(
                "The rainbow title bar effect is already applied to this window."
            )

        set_window_long(hwnd, GWL_EXSTYLE, old_ex_style)  # Reset the window style

    @classmethod
    def get_current_color(cls) -> Tuple[int, int, int]:
        """
        Get the current RGB color value of the title bar, which is being displayed by the rainbow effect.
        Can be useful if you want to synchronize the title bar's rainbow effect with other elements of the window.

        Returns:
            tuple: A tuple containing the RGB color values of the title bar.

        Notes:
            Example implementation of this feature available at [examples/rainbow-synchronization-example.py](https://github.com/Zingzy/hPyT/blob/main/examples/rainbow-synchronization-example.py).
        """

        color = cls.current_color
        if color is None:
            return (0, 0, 0)  # Default color if current_color is None
        b = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        r = color & 0xFF
        return (r, g, b)

    @classmethod
    def stop(cls, window: Any) -> None:
        """
        Stop the rainbow effect on the title bar of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)
        if hwnd in rnbtbs:
            rnbtbs.remove(hwnd)
        else:
            raise ValueError("Rainbow title bar is not running on this window.")


class rainbow_border:
    """Add a rainbow effect to the border of a window."""

    current_color = None

    @classmethod
    def start(cls, window: Any, interval: int = 5, color_stops: int = 5) -> None:
        """
        Start the rainbow effect on the border of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
            interval (int): The interval between each color change in milliseconds. Default is 5.
            color_stops (int): The number of color stops between each RGB value. Default is 5.

        Example:
            >>> rainbow_border.start(window, interval=10, color_stops=10)

        Notes:
            The `interval` parameter controls the speed of the rainbow effect, and the `color_stops` parameter controls the number of color stops between each RGB value.
            Higher values for `interval` will result in a slower rainbow effect.
            Higher values for `color_stops` might skip most of the colors defying the purpose of the rainbow effect.
        """

        def color_changer(hwnd, interval: int):
            r, g, b = 200, 0, 0
            while hwnd in rnbbcs:
                cls.current_color = (r << 16) | (g << 8) | b

                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, 34, ctypes.byref(ctypes.c_int(cls.current_color)), 4
                )
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
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, 34, ctypes.byref(ctypes.c_int(-1)), 4
                )

        hwnd: int = module_find(window)
        if hwnd in accent_color_borders:
            accent_color_borders.remove(hwnd)

        old_ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        new_ex_style = old_ex_style | WS_EX_LAYERED
        set_window_long(hwnd, GWL_EXSTYLE, new_ex_style)

        if hwnd not in rnbbcs:
            rnbbcs.append(hwnd)
            thread = threading.Thread(target=color_changer, args=(hwnd, interval))
            thread.daemon = True
            thread.start()
        else:
            raise RuntimeError(
                "The rainbow border effect is already applied to this window."
            )

        set_window_long(hwnd, GWL_EXSTYLE, old_ex_style)  # Reset the window style

    @classmethod
    def get_current_color(cls) -> Tuple[int, int, int]:
        """
        Get the current RGB color value of the border, which is being displayed by the rainbow effect.
        Can be useful if you want to synchronize the border's rainbow effect with other elements of the window.

        Returns:
            tuple: A tuple containing the RGB color values of the border.

        Notes:
            Example implementation of this feature available at [examples/rainbow-synchronization-example.py](https://github.com/Zingzy/hPyT/blob/main/examples/rainbow-synchronization-example.py
        """

        color = cls.current_color
        if color is None:
            return (0, 0, 0)  # Default color if current_color is None
        b = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        r = color & 0xFF
        return (r, g, b)

    @classmethod
    def stop(cls, window: Any) -> None:
        """
        Stop the rainbow effect on the border of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)
        if hwnd in rnbbcs:
            rnbbcs.remove(hwnd)
        else:
            raise ValueError("Rainbow border is not running on this window.")


class window_frame:
    """Change the position, size, and state of a window."""

    @classmethod
    def center(cls, window: Any) -> None:
        """
        Center the specified window on the screen.

        Args:
            window (object): The window object to center (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)

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
    def center_relative(cls, window_parent: Any, window_child: Any) -> None:
        """
        Center the specified child window relative to the parent window.

        Args:
            window_parent (object): The parent window object (e.g., a Tk instance in Tkinter).
            window_child (object): The child window object to center with respect to the `window_parent` (e.g., a Tk instance in Tkinter).

        Example:
            >>> window_frame.center_relative(parent_window, child_window)
        """

        hwnd_parent: int = module_find(window_parent)
        hwnd_child: int = module_find(window_child)

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
    def move(cls, window: Any, x: int, y: int) -> None:
        """
        Move the specified window to the specified position.

        Args:
            window (object): The window object to move (e.g., a Tk instance in Tkinter).
            x (int): The new X-coordinate of the window.
            y (int): The new Y-coordinate of the window.

        Example:
            >>> window_frame.move(window, 100, 100) # moves the window to (100, 100)
        """

        hwnd: int = module_find(window)
        set_window_pos(hwnd, 0, x, y, 0, 0, 0x0001)

    @classmethod
    def resize(cls, window: Any, width: int, height: int) -> None:
        """
        Resize the specified window to the specified width and height.

        Args:
            window (object): The window object to resize (e.g., a Tk instance in Tkinter).
            width (int): The new width of the window.
            height (int): The new height of the window.

        Example:
            >>> window_frame.resize(window, 800, 600) # resizes the window to 800x600
        """

        hwnd: int = module_find(window)
        set_window_pos(hwnd, 0, 0, 0, width, height, 0x0001)

    @classmethod
    def minimize(cls, window: Any) -> None:
        """
        Minimize the specified window.

        Args:
            window (object): The window object to minimize (e.g., a Tk instance in Tkinter).
        """

        hwnd = module_find(window)
        ctypes.windll.user32.ShowWindow(hwnd, 6)

    @classmethod
    def maximize(cls, window: Any) -> None:
        """
        Maximize the specified window.

        Args:
            window (object): The window object to maximize (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)
        ctypes.windll.user32.ShowWindow(hwnd, 3)

    @classmethod
    def restore(cls, window: Any) -> None:
        """
        Restore a minimized or maximized window to its original size and position.
        """

        hwnd: int = module_find(window)
        ctypes.windll.user32.ShowWindow(hwnd, 9)


class window_animation:
    """Add linear animations to a window."""

    @classmethod
    def circle_motion(
        cls, window: Any, count: int = 5, interval: int = 5, radius: int = 20
    ) -> None:
        """
        Move the specified window in a circular motion.

        Args:
            window (object): The window object to move (e.g., a Tk instance in Tkinter).
            count (int): The number of times to move the window in a circle. Default is 5.
            interval (int): The interval between each movement in milliseconds. Default is 5.
            radius (int): The radius of the circular motion. Default is 20.

        Example:
            >>> window_animation.circle_motion(window, count=10, interval=10, radius=30)

        Notes:
            The `interval` parameter controls the speed of the circular motion. Lower values will result in a faster circular motion.
        """

        def motion() -> None:
            hwnd: int = module_find(window)
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            original_x = rect.left
            original_y = rect.top
            for angle in range(0, 360 * count, 5):  # move in a circle count times
                rad: float = math.radians(angle)
                x = original_x + int(radius * math.cos(rad))
                y = original_y + int(radius * math.sin(rad))
                ctypes.windll.user32.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0001)
                ctypes.windll.kernel32.Sleep(interval)

        thread = threading.Thread(target=motion)
        thread.daemon = True
        thread.start()

    @classmethod
    def vertical_shake(
        cls, window: Any, count: int = 5, interval: int = 3, amplitude: int = 20
    ) -> None:
        """
        Shake the specified window vertically.

        Args:
            window (object): The window object to shake (e.g., a Tk instance in Tkinter).
            count (int): The number of times to shake the window. Default is 5.
            interval (int): The interval between each shake in milliseconds. Default is 3.
            amplitude (int): The amplitude or upward/downward distance of the shake. Default is 20.

        Example:
            >>> window_animation.vertical_shake(window, count=10, interval=5, amplitude=30)

        Notes:
            The `interval` parameter controls the speed of the shake. Lower values will result in a faster
        """

        def motion() -> None:
            hwnd: int = module_find(window)
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            original_y = rect.top
            for offset in range(0, 360 * count, count):  # move up and down 5 times
                rad: float = math.radians(offset)
                y = original_y + int(amplitude * math.sin(rad))
                ctypes.windll.user32.SetWindowPos(hwnd, 0, rect.left, y, 0, 0, 0x0001)
                ctypes.windll.kernel32.Sleep(interval)

        thread = threading.Thread(target=motion)
        thread.daemon = True
        thread.start()

    @classmethod
    def horizontal_shake(
        cls, window: Any, count: int = 5, interval: int = 3, amplitude: int = 20
    ) -> None:
        """
        Shake the specified window horizontally.

        Args:
            window (object): The window object to shake (e.g., a Tk instance in Tkinter).
            count (int): The number of times to shake the window. Default is 5.
            interval (int): The interval between each shake in milliseconds. Default is 3.
            amplitude (int): The amplitude or left/right distance of the shake. Default is 20.

        Example:
            >>> window_animation.horizontal_shake(window, count=10, interval=5, amplitude=30)

        Notes:
            The `interval` parameter controls the speed of the shake. Lower values will result in a faster shake.
        """

        def motion() -> None:
            hwnd: int = module_find(window)
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            original_x = rect.left
            for offset in range(0, 360 * count, count):  # move left and right 5 times
                rad: float = math.radians(offset)
                x = original_x + int(amplitude * math.sin(rad))
                ctypes.windll.user32.SetWindowPos(hwnd, 0, x, rect.top, 0, 0, 0x0001)
                ctypes.windll.kernel32.Sleep(interval)

        thread = threading.Thread(target=motion)
        thread.daemon = True
        thread.start()


class title_text:
    """Play with the title of a window."""

    @classmethod
    def set(cls, window: Any, title: str) -> None:
        """
        Changes the title of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
            title (str): The new title to set.
        """

        hwnd: int = module_find(window)
        ctypes.windll.user32.SetWindowTextW(hwnd, title)

    @classmethod
    def stylize(cls, window: Any, style: int = 1) -> None:
        """
        Stylize the title of the specified window.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
            style (int): The style to apply to the title. There are 10 styles available (1-10). Default is 1.
        """

        hwnd: int = module_find(window)
        if hwnd not in titles:
            title = ctypes.create_unicode_buffer(1024)
            ctypes.windll.user32.GetWindowTextW(hwnd, title, 1024)
            titles[hwnd] = title.value
        title = ctypes.create_unicode_buffer(stylize_text(titles[hwnd], style))
        ctypes.windll.user32.SetWindowTextW(hwnd, title)

    @classmethod
    def reset(cls, window: Any) -> None:
        """
        Remove the stylized title of the specified window and reset it to the original title.

        Args:
            window (object): The window object to modify (e.g., a Tk instance in Tkinter).
        """

        hwnd: int = module_find(window)
        if hwnd in titles:
            ctypes.windll.user32.SetWindowTextW(hwnd, titles[hwnd])
            del titles[hwnd]


def stylize_text(text: str, style: int) -> str:
    """
    Helper function to stylize the text based on the specified style.

    Args:
        text (str): The text to stylize.
        style (int): The style to apply to the text. There are 10 styles available (1-10).

    Returns:
        str: The stylized text based on the specified style.

    Example:
        stylize_text("Hello, World!", 3)

    Raises:
        ValueError: If the specified style is not between 1 and 10.
    """

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
        "卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙1234567890",
    ]

    if style < 1 or style > len(styles):
        raise ValueError("Invalid style number")

    translation_table: dict[int, int] = str.maketrans(normal, styles[style - 1])
    return text.translate(translation_table)


def convert_color(color: Union[Tuple[int, int, int], str]) -> int:
    """
    Helper function to convert the color value to an integer.

    Args:
        color (tuple/string): The RGB or HEX color value to convert.

    Returns:
        int: The converted color value as an integer.
    """

    if isinstance(color, tuple) and len(color) == 3:  # RGB format
        r, g, b = color
        return (b << 16) | (g << 8) | r
    elif isinstance(color, str) and color.startswith("#"):  # HEX format
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        return (b << 16) | (g << 8) | r
    else:
        raise ValueError("Invalid color format. Expected RGB tuple or HEX string.")


def get_accent_color() -> str:
    """
    Helper function to get the system accent color.

    Returns:
        tuple: A tuple containing the RGB color values of the system accent color.

    Example:
        >>> get_accent_color()
    """

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\DWM")
    value, type = winreg.QueryValueEx(key, "ColorizationAfterglow")
    winreg.CloseKey(key)

    if len(hex(value)[4:]) == 6:
        return "#" + hex(value)[4:]
    else:
        return "#" + hex(value)[2:]


def module_find(window: Any) -> int:
    """
    Helper function to find the window handle based on the module used.

    Args:
        window (object): The window object to find.

    Returns:
        int: The window handle.
    """

    try:
        window.update()  # for tk
        return ctypes.windll.user32.GetParent(window.winfo_id())
    except Exception:
        pass
    try:
        return window.winId().__int__()  # for pyQt and PySide
    except Exception:
        pass
    try:
        return window.GetHandle()  # for wx
    except Exception:
        pass
    try:
        gdk_window = window.get_window()  # for PyGTK
        return gdk_window.get_xid()
    except Exception:
        pass
    try:
        return window.root_window.get_window_info().window  # for kivy
    except Exception:
        pass

    return window  # others / notfound
