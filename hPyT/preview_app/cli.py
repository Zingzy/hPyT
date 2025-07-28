from tkinter import StringVar
from dataclasses import dataclass
from typing import Dict
from webbrowser import open as open_link
import os.path
from os import chdir
import subprocess
import sys
import tempfile

try:
    from customtkinter import (
        CTk,
        CTkImage,
        CTkFrame,
        CTkLabel,
        CTkButton,
        CTkSlider,
        CTkOptionMenu,
        CTkToplevel,
        CTkScrollableFrame,
    )

    import customtkinter
    from win32mica import ApplyMica, MicaStyle, MicaTheme
    from PIL import Image
except ModuleNotFoundError:
    print(
        "The hPyT Preview program needs the following additional dependencies to be installed for working:\n"
    )
    print("- customtkinter")
    print("- win32mica")
    print("- Pillow")

    install_modules_permission = input("\nWould you like to install them? (Y/N): ")

    if install_modules_permission.lower() == "y":
        print("\n")
        subprocess.call(
            f'"{sys.executable}" -m pip install customtkinter win32mica Pillow',
            shell=True,
        )

        print("\nRelaunching the preview program...\n")
        subprocess.call(f'"{sys.executable}" -m hPyT', shell=True)
        sys.exit(0)
    else:
        sys.exit(0)

from hPyT import (
    title_bar_color,
    window_animation,
    window_flash,
    window_frame,
    title_bar,
    maximize_minimize_button,
    opacity,
    all_stuffs,
    rainbow_title_bar,
    rainbow_border,
    title_text,
    window_dwm,
    corner_radius,
    get_accent_color,
)

# Change the current directory to the one where the demo program is
# This fixes FileNotFoundError exceptions
chdir(os.path.dirname(__file__))

try:
    theme_accent = (
        open("assets/theme.json", "r").read().replace("#616107", get_accent_color())
    )

    temp_dir = os.path.join(tempfile.gettempdir(), "hPyT Preview")

    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    open(os.path.join(temp_dir, "theme_accent.json"), "w").write(theme_accent)

    customtkinter.set_default_color_theme(os.path.join(temp_dir, "theme_accent.json"))
except Exception as e:
    print(e)
    customtkinter.set_default_color_theme("assets/theme.json")

customtkinter.set_appearance_mode("Dark")
IS_WINDOWS_11: bool = sys.getwindowsversion().build >= 22000


@dataclass
class ThemeConfig:
    """Configuration for app theming"""

    primary_color: str
    secondary_color: str
    button_color: str
    button_hover_color: str

    if IS_WINDOWS_11:
        primary_color = "black"
        secondary_color = "grey6"
        button_color = "grey13"
        button_hover_color = "grey16"
    else:
        primary_color = "#202020"
        secondary_color = "#2F2F2F"
        button_color = "#414141"
        button_hover_color = "#494949"

    fallback_bg_color: str = "#202020"
    fallback_frame_color: str = "#2F2F2F"
    fallback_button_color: str = "#414141"
    fallback_button_hover: str = "#494949"


class ImageManager:
    """Manages app images"""

    def __init__(self):
        self.images: Dict[str, CTkImage] = {}
        self._load_images()

    def _load_images(self):
        image_configs = {
            "hide": ("assets/hide.png", (15, 15)),
            "unhide": ("assets/unhide.png", (15, 15)),
            "rocket": ("assets/Rocket.png", (15, 15)),
            "enable": ("assets/enable.png", (15, 15)),
            "disable": ("assets/disable.png", (15, 15)),
            "play": ("assets/play.png", (15, 15)),
            "pause": ("assets/pause.png", (15, 15)),
            "history": ("assets/history.png", (20, 20)),
            "github": ("assets/github.png", (20, 20)),
            "pypi": ("assets/pypi.png", (20, 20)),
        }

        for name, (path, size) in image_configs.items():
            full_path = path
            self.images[name] = CTkImage(light_image=Image.open(full_path), size=size)

    def get(self, name: str) -> "CTkImage | None":
        return self.images.get(name)


class BaseComponent:
    """Base class for UI components"""

    def __init__(self, parent, theme: ThemeConfig):
        self.parent = parent
        self.theme = theme
        self.setup()

    def setup(self):
        pass


class CodeCopyButton(BaseComponent):
    """Reusable button for copying code snippets"""

    def __init__(
        self, parent, theme: ThemeConfig, code: str, button_text: str = "Copy Code"
    ):
        self.code = code
        self.button_text = button_text
        super().__init__(parent, theme)

    def setup(self):
        self.button = CTkButton(
            self.parent,
            text=self.button_text,
            command=self._copy_code,
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            font=("Segoe UI", 13),
        )

    def _copy_code(self):
        self.button.winfo_toplevel().clipboard_clear()
        self.button.winfo_toplevel().clipboard_append(self.code)

        self.button.configure(text="Copied !")
        self.parent.after(1000, lambda: self.button.configure(text=self.button_text))

    def pack(self, **kwargs):
        self.button.pack(**kwargs)


class FeatureFrame(BaseComponent):
    """Base class for feature frames"""

    def __init__(self, parent, theme: ThemeConfig, title: str, description: str):
        self.title = title
        self.description = description
        super().__init__(parent, theme)

    def setup(self):
        self.frame = CTkFrame(
            self.parent, fg_color=self.theme.secondary_color, width=160, height=250
        )
        self.frame.grid_propagate(False)
        self.frame.pack_propagate(False)

        self.title_label = CTkLabel(
            self.frame, text=self.title, font=("Segoe UI", 16, "bold"), wraplength=120
        )
        self.title_label.pack(padx=10, pady=10)

        self.description_label = CTkLabel(
            self.frame,
            text=self.description,
            wraplength=140,
            font=("Segoe UI", 13),
            justify="center",
        )
        self.description_label.pack(padx=10, pady=(10, 0))

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class TitleBarFeature(FeatureFrame):
    """Title bar control feature"""

    def __init__(self, parent, theme: ThemeConfig, window: CTk, images: ImageManager):
        super().__init__(parent, theme, "Title Bar", "Hide or unhide title bar")
        self.window = window
        self.images = images
        self._setup_controls()

    def _setup_controls(self):
        # Create a frame for no_span controls
        no_span_frame = CTkFrame(self.frame, fg_color=self.theme.secondary_color)
        no_span_frame.pack(padx=5, pady=0, fill="x")

        CTkLabel(
            no_span_frame,
            text="no_span",
            font=("Segoe UI", 13),
        ).pack(side="left", padx=(10, 10), pady=5)

        self.no_span_var = StringVar(value="True")
        self.no_span_menu = CTkOptionMenu(
            no_span_frame,
            values=["True", "False"],
            variable=self.no_span_var,
            fg_color=self.theme.button_color,
            font=("Segoe UI", 13),
            width=80,
            command=self._on_no_span_change,
        )
        self.no_span_menu.pack(side="left", padx=(0, 5), pady=5)

        self.rtl_toggle = CTkButton(
            self.frame,
            text="Enable RTL",
            command=self._on_rtl_change,
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            font=("Segoe UI", 13),
            image=self.images.get("enable"),
            compound="right",
        )
        self.rtl_toggle.pack(padx=10, pady=(5, 10), side="bottom")

        self.toggle_button = CTkButton(
            self.frame,
            text="   Hide",
            command=self._toggle_title_bar,
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            font=("Segoe UI", 13),
            image=self.images.get("hide"),
            compound="right",
        )
        self.toggle_button.pack(padx=10, pady=5, side="bottom")

        self.copy_button = CodeCopyButton(
            self.frame,
            self.theme,
            self._get_copy_code(),
        )
        self.copy_button.pack(padx=10, pady=5, side="bottom")

    def _get_copy_code(self) -> str:
        no_span = self.no_span_var.get()
        return f"""from hPyT import *\n\ntitle_bar.hide(window, no_span={no_span})\n# title_bar.unhide(window)"""

    def _on_no_span_change(self, _):
        self.copy_button.code = self._get_copy_code()

    def _on_rtl_change(self):
        if self.rtl_toggle.cget("text") == "Enable RTL":
            window_dwm.toggle_rtl_layout(self.window, enabled=True)
            self.rtl_toggle.configure(
                text="Disable RTL", image=self.images.get("disable")
            )
        else:
            window_dwm.toggle_rtl_layout(self.window, enabled=False)
            self.rtl_toggle.configure(
                text="Enable RTL", image=self.images.get("enable")
            )

    def _toggle_title_bar(self):
        if self.toggle_button.cget("text") == "   Hide":
            no_span = self.no_span_var.get().lower() == "true"
            title_bar.hide(self.window, no_span=no_span)

            self.toggle_button.configure(
                text="    Unhide",
                command=self._toggle_title_bar,
                image=self.images.get("unhide"),
            )
        else:
            title_bar.unhide(self.window)
            self.toggle_button.configure(
                text="   Hide",
                command=self._toggle_title_bar,
                image=self.images.get("hide"),
            )

        # Update copy code when state changes
        self.copy_button.code = self._get_copy_code()


class RainbowTitleBarFeature(FeatureFrame):
    """Rainbow title bar feature"""

    def __init__(self, parent, theme: ThemeConfig, window: CTk, images: ImageManager):
        super().__init__(
            parent, theme, "Rainbow Title Bar", "Adds a rainbow effect to the titlebar"
        )
        self.window = window
        self.images = images
        self._setup_controls()

    def _setup_controls(self):
        self.toggle_button = CTkButton(
            self.frame,
            text="   Start",
            command=self._toggle_rainbow,
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            font=("Segoe UI", 13),
            image=self.images.get("play"),
            compound="right",
        )
        self.toggle_button.pack(padx=10, pady=(5, 10), side="bottom")

        if not IS_WINDOWS_11:
            self.toggle_button.configure(state="disabled")

        self.copy_button = CodeCopyButton(
            self.frame,
            self.theme,
            """from hPyT import *\n\nrainbow_title_bar.start(window, interval=5, color_stops=5)\n# rainbow_title_bar.stop(window)""",
        )
        self.copy_button.pack(padx=10, pady=5, side="bottom")

    def _toggle_rainbow(self):
        if self.toggle_button.cget("text") == "   Start":
            rainbow_title_bar.start(self.window, interval=5, color_stops=5)
            self.toggle_button.configure(text="   Stop", image=self.images.get("pause"))
        else:
            rainbow_title_bar.stop(self.window)
            self.toggle_button.configure(text="   Start", image=self.images.get("play"))


class OpacityFeature(FeatureFrame):
    """Window opacity control feature"""

    def __init__(self, parent, theme: ThemeConfig, window: CTk):
        super().__init__(
            parent,
            theme,
            "Opacity",
            "Change the opacity of the window by moving the slider below",
        )
        self.window = window
        self._setup_controls()

    def _setup_controls(self):
        opacity_warning = CTkLabel(
            self.frame,
            text="Press Ctrl+Shift+R to reset the opacity if you can't see the window",
            wraplength=150,
            font=("Segoe UI", 12, "bold"),
            justify="center",
            text_color="#FF5050",
        )
        opacity_warning.pack(padx=10, pady=(10, 0))

        slider_frame = CTkFrame(self.frame, fg_color=self.theme.button_color)
        slider_frame.pack(padx=10, pady=10, side="bottom")

        self.opacity_slider = CTkSlider(
            slider_frame,
            from_=0,
            to=1,
            number_of_steps=10,
            fg_color=self.theme.button_color,
            width=120,
            progress_color=(
                customtkinter.ThemeManager.theme["CTkButton"]["fg_color"][0],
                customtkinter.ThemeManager.theme["CTkButton"]["fg_color"][0],
            ),
            command=self._on_opacity_change,
        )

        self.opacity_slider.pack(padx=10, pady=(5, 5), side="bottom")
        self.opacity_slider.set(1)

        self.window.bind(
            "<Control-Shift-R>",
            lambda event: [self.opacity_slider.set(1), opacity.set(self.window, 1.0)],
        )

        self.copy_button = CodeCopyButton(
            self.frame,
            self.theme,
            """from hPyT import *\n\nopacity.set(window, 0.5) # 0.5 is the opacity value""",
        )
        self.copy_button.pack(padx=10, pady=(5, 0), side="bottom")

    def _on_opacity_change(self, value):
        opacity.set(self.window, value)


class WindowFlashFeature(FeatureFrame):
    """Window flashing feature"""

    def __init__(self, parent, theme: ThemeConfig, window: CTk):
        super().__init__(parent, theme, "Flashing", "Start or stop flashing the window")
        self.window = window
        self._setup_controls()

    def _setup_controls(self):
        flash_warning = CTkLabel(
            self.frame,
            text="FLASH WARNING",
            wraplength=150,
            font=("Segoe UI", 12, "bold"),
            justify="center",
            text_color="#FF5050",
        )
        flash_warning.pack(padx=10, pady=(25, 0))

        self.flash_button = CTkButton(
            self.frame,
            text="Start Flashing",
            command=self._toggle_flash,
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            font=("Segoe UI", 13),
        )
        self.flash_button.pack(padx=10, pady=(5, 10), side="bottom")

        self.copy_button = CodeCopyButton(
            self.frame,
            self.theme,
            """from hPyT import *\n\nwindow_flash.flash(window, count=50, interval=100)\n# window_flash.stop(window)""",
        )
        self.copy_button.pack(padx=10, pady=5, side="bottom")

    def _toggle_flash(self):
        if self.flash_button.cget("text") == "Start Flashing":
            window_flash.flash(self.window, count=10000000, interval=100)
            self.flash_button.configure(text="Stop Flashing")
        else:
            window_flash.stop(self.window)
            self.flash_button.configure(text="Start Flashing")


class RainbowBorderFeature(FeatureFrame):
    """Rainbow border feature"""

    def __init__(self, parent, theme: ThemeConfig, window: CTk, images: ImageManager):
        super().__init__(
            parent,
            theme,
            "Rainbow Border",
            "Adds a rainbow effect to the border of the window",
        )
        self.window = window
        self.images = images
        self._setup_controls()

    def _setup_controls(self):
        self.toggle_button = CTkButton(
            self.frame,
            text="   Start",
            command=self._toggle_rainbow_border,
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            font=("Segoe UI", 13),
            image=self.images.get("play"),
            compound="right",
        )
        self.toggle_button.pack(padx=10, pady=(5, 10), side="bottom")

        if not IS_WINDOWS_11:
            self.toggle_button.configure(state="disabled")

        self.copy_button = CodeCopyButton(
            self.frame,
            self.theme,
            """from hPyT import *\n\nrainbow_border.start(window, interval=5, color_stops=5)\n# rainbow_border.stop(window)""",
        )
        self.copy_button.pack(padx=10, pady=5, side="bottom")

    def _toggle_rainbow_border(self):
        if self.toggle_button.cget("text") == "   Start":
            rainbow_border.start(self.window, interval=5, color_stops=5)
            self.toggle_button.configure(text="   Stop", image=self.images.get("pause"))
        else:
            rainbow_border.stop(self.window)
            self.toggle_button.configure(text="   Start", image=self.images.get("play"))


class MaximizeMinimizeFeature(FeatureFrame):
    """Maximize/Minimize button control feature"""

    def __init__(self, parent, theme: ThemeConfig, window: CTk, images: ImageManager):
        super().__init__(
            parent,
            theme,
            "Maximize Minimize",
            "Hide or unhide maximize and minimize button",
        )
        self.window = window
        self.images = images
        self._setup_controls()

    def _setup_controls(self):
        self.toggle_button = CTkButton(
            self.frame,
            text="   Hide",
            command=self._toggle_buttons,
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            font=("Segoe UI", 13),
            image=self.images.get("hide"),
            compound="right",
        )
        self.toggle_button.pack(padx=10, pady=(5, 10), side="bottom")

        self.copy_button = CodeCopyButton(
            self.frame,
            self.theme,
            """from hPyT import *\n\nmaximize_minimize_button.hide(window)\n# maximize_minimize_button.unhide(window)""",
        )
        self.copy_button.pack(padx=10, pady=5, side="bottom")

    def _toggle_buttons(self):
        if self.toggle_button.cget("text") == "   Hide":
            maximize_minimize_button.hide(self.window)
            self.toggle_button.configure(
                text="    Unhide", image=self.images.get("unhide")
            )
        else:
            maximize_minimize_button.unhide(self.window)
            self.toggle_button.configure(text="   Hide", image=self.images.get("hide"))


class AnimationsFeature(FeatureFrame):
    """Window animations feature"""

    def __init__(self, parent, theme: ThemeConfig, window: CTk):
        super().__init__(parent, theme, "Animations", "Add animations to the window")
        self.window = window
        self._setup_controls()

    def _setup_controls(self):
        self.circle_button = CTkButton(
            self.frame,
            text="Circle Motion",
            command=lambda: window_animation.circle_motion(
                self.window, interval=3, radius=50
            ),
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            font=("Segoe UI", 13),
        )
        self.circle_button.pack(padx=10, pady=(5, 10), side="bottom")

        self.vertical_button = CTkButton(
            self.frame,
            text="Vertical Shake",
            command=lambda: window_animation.vertical_shake(self.window, interval=2),
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            font=("Segoe UI", 13),
        )
        self.vertical_button.pack(padx=10, pady=(5, 5), side="bottom")

        self.copy_button = CodeCopyButton(
            self.frame,
            self.theme,
            """from hPyT import *\n\nwindow_animation.circle_motion(window, radius=50, interval=3)\n# window_animation.vertical_shake(window, amplitude=50, interval=3)\n# window_animation.horizontal_shake(window, amplitude=50, interval=3)""",
        )
        self.copy_button.pack(padx=10, pady=5, side="bottom")


class AllStuffsFeature(FeatureFrame):
    """All stuffs control feature"""

    def __init__(self, parent, theme: ThemeConfig, window: CTk, images: ImageManager):
        super().__init__(
            parent,
            theme,
            "All Stuffs",
            "Hide or unhide everything (buttons and icon) from titlebar",
        )
        self.window = window
        self.images = images
        self._setup_controls()

    def _setup_controls(self):
        self.toggle_button = CTkButton(
            self.frame,
            text="   Hide",
            command=self._toggle_all_stuffs,
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            font=("Segoe UI", 13),
            image=self.images.get("hide"),
            compound="right",
        )
        self.toggle_button.pack(padx=10, pady=(5, 10), side="bottom")

        self.copy_button = CodeCopyButton(
            self.frame,
            self.theme,
            """from hPyT import *\n\nall_stuffs.hide(window)\n# all_stuffs.unhide(window)""",
        )
        self.copy_button.pack(padx=10, pady=5, side="bottom")

    def _toggle_all_stuffs(self):
        if self.toggle_button.cget("text") == "   Hide":
            all_stuffs.hide(self.window)
            self.toggle_button.configure(
                text="    Unhide", image=self.images.get("unhide")
            )
        else:
            all_stuffs.unhide(self.window)
            self.toggle_button.configure(text="   Hide", image=self.images.get("hide"))


class AccentTitlebarFeature(FeatureFrame):
    """Accent titlebar feature"""

    def __init__(self, parent, theme: ThemeConfig, window: CTk, images: ImageManager):
        super().__init__(
            parent,
            theme,
            "Accent Titlebar",
            "Set the titlebar to follow the system accent color",
        )
        self.window = window
        self.images = images
        self._setup_controls()

    def _setup_controls(self):
        self.toggle_button = CTkButton(
            self.frame,
            text="Enable",
            command=self._toggle_accent,
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            font=("Segoe UI", 13),
            image=self.images.get("enable"),
            compound="right",
        )
        self.toggle_button.pack(padx=10, pady=(5, 10), side="bottom")

        if not IS_WINDOWS_11:
            self.toggle_button.configure(state="disabled")

        self.copy_button = CodeCopyButton(
            self.frame,
            self.theme,
            """from hPyT import *\n\ntitle_bar_color.set_accent(window)\n# title_bar_color.reset(window)""",
        )
        self.copy_button.pack(padx=10, pady=5, side="bottom")

    def _toggle_accent(self):
        if self.toggle_button.cget("text") == "Enable":
            title_bar_color.set_accent(self.window)
            self.toggle_button.configure(
                text="Disable", image=self.images.get("disable")
            )
        else:
            title_bar_color.reset(self.window)
            self.toggle_button.configure(text="Enable", image=self.images.get("enable"))


class CornerRadiusFeature(FeatureFrame):
    """Window corner radius control feature"""

    def __init__(self, parent, theme: ThemeConfig, window: CTk):
        super().__init__(
            parent,
            theme,
            "Corner Radius",
            "Change the corner radius of the window",
        )
        self.window = window
        self._setup_controls()

    def _setup_controls(self):
        self.radius_var = StringVar(value="round")
        self.radius_menu = CTkOptionMenu(
            self.frame,
            values=["small-round", "square", "round"],
            variable=self.radius_var,
            command=self._change_radius,
            fg_color=self.theme.button_color,
            font=("Segoe UI", 13),
        )
        self.radius_menu.pack(padx=10, pady=(5, 10), side="bottom")

        if not IS_WINDOWS_11:
            self.radius_menu.configure(state="disabled")

        self.copy_button = CodeCopyButton(
            self.frame,
            self.theme,
            self._get_copy_code(),
        )
        self.copy_button.pack(padx=10, pady=5, side="bottom")

        self.radius_var.trace_add("write", self._on_radius_change)

    def _get_copy_code(self) -> str:
        radius = self.radius_var.get()
        if radius == "small-round":
            return """from hPyT import *\ncorner_radius.set(window, "small-round")"""
        elif radius == "square":
            return """from hPyT import *\ncorner_radius.set(window, "square")"""
        else:
            return """from hPyT import *\ncorner_radius.set(window, "round")"""

    def _on_radius_change(self, *args):
        self.copy_button.code = self._get_copy_code()

    def _change_radius(self, radius: str):
        corner_radius.set(self.window, radius)


class RelativeCenterFeature(FeatureFrame):
    """Relative center feature"""

    def __init__(self, parent, theme: ThemeConfig, window: CTk):
        super().__init__(
            parent,
            theme,
            "Relative Center",
            "Center a secondary window with respect to the primary window",
        )
        self.window = window
        self._setup_controls()

    def _setup_controls(self):
        self.center_button = CTkButton(
            self.frame,
            text="Center",
            command=self._show_centered_window,
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            font=("Segoe UI", 13),
        )
        self.center_button.pack(padx=10, pady=(5, 10), side="bottom")

        self.copy_button = CodeCopyButton(
            self.frame,
            self.theme,
            """from hPyT import *\n\ntop = CTk()\ntop.title('Secondary Window')\ntop.geometry("400x200")\n\nwindow_frame.center_relative(window, top)\nwindow.bind('<Configure>', lambda e: window_frame.center_relative(window, top))\n\ntop.protocol("WM_DELETE_WINDOW", lambda: [top.destroy(), window.unbind('<Configure>')])""",
        )
        self.copy_button.pack(padx=10, pady=5, side="bottom")

    def _show_centered_window(self):
        top = CTk()
        top.title("Secondary Window")
        top.geometry("400x200")

        CTkLabel(
            top,
            text="Move the parent window to see the secondary window center",
            font=("Segoe UI", 13),
        ).pack(pady=10)

        window_frame.center_relative(self.window, top)
        self.window.bind(
            "<Configure>", lambda e: window_frame.center_relative(self.window, top)
        )

        top.protocol(
            "WM_DELETE_WINDOW",
            lambda: [top.destroy(), self.window.unbind("<Configure>")],
        )


class StylizedTextFeature(FeatureFrame):
    """Stylized text feature"""

    def __init__(self, parent, theme: ThemeConfig, window: CTk):
        super().__init__(
            parent, theme, "Stylized Title Text", "Stylize the title text of the window"
        )
        self.window = window
        self._setup_controls()

    def _setup_controls(self):
        self.style_var = StringVar(value="normal")
        self.style_menu = CTkOptionMenu(
            self.frame,
            values=[
                "normal",
                "style 1",
                "style 2",
                "style 3",
                "style 4",
                "style 5",
                "style 6",
                "style 7",
                "style 8",
                "style 9",
                "style 10",
            ],
            variable=self.style_var,
            command=self._change_style,
            fg_color=self.theme.button_color,
            font=("Segoe UI", 13),
        )
        self.style_menu.pack(padx=10, pady=(5, 10), side="bottom")

        self.copy_button = CodeCopyButton(
            self.frame,
            self.theme,
            self._get_copy_code(),
        )
        self.copy_button.pack(padx=10, pady=5, side="bottom")

        # Set up trace to update copy code when style changes
        self.style_var.trace_add("write", self._on_style_change)

    def _get_copy_code(self) -> str:
        style = self.style_var.get()
        if style == "normal":
            return """from hPyT import *\n\ntitle_text.reset(window) # to reset the title text to normal"""

        style_num = style.split(" ")[-1]
        return f"""from hPyT import *\n\ntitle_text.stylize(window, {style_num}) # {style_num} is the style number\n# title_text.reset(window) # to reset the title text to normal"""

    def _on_style_change(self, *args):
        self.copy_button.code = self._get_copy_code()

    def _change_style(self, style: str):
        if style == "normal":
            title_text.reset(self.window)
        else:
            title_text.stylize(self.window, int(style.split(" ")[-1]))


class TransitionsFeature(FeatureFrame):
    """Transitions feature"""

    def __init__(self, parent, theme: ThemeConfig, window: CTk, images: ImageManager):
        super().__init__(
            parent,
            theme,
            "Transitions",
            "Disable or enable window transitions",
        )
        self.window = window
        self.images = images
        self._setup_controls()

    def _setup_controls(self):
        self.toggle_button = CTkButton(
            self.frame,
            text="Disable",
            command=self._toggle_transitions,
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            font=("Segoe UI", 13),
            image=self.images.get("disable"),
            compound="right",
        )
        self.toggle_button.pack(padx=10, pady=(5, 10), side="bottom")

        self.copy_button = CodeCopyButton(
            self.frame,
            self.theme,
            self._get_copy_code(),
        )
        self.copy_button.pack(padx=10, pady=5, side="bottom")

    def _get_copy_code(self):
        transitions_enabled = not self.toggle_button.cget("text") == "Enable"
        return f"""from hPyT import *\n\nwindow_dwm.toggle_dwm_transitions(self.window, enabled={transitions_enabled})"""

    def _toggle_transitions(self):
        if self.toggle_button.cget("text") == "Enable":
            window_dwm.toggle_dwm_transitions(self.window, enabled=True)
            self.toggle_button.configure(
                text="Disable", image=self.images.get("disable")
            )
        else:
            window_dwm.toggle_dwm_transitions(self.window, enabled=False)
            self.toggle_button.configure(text="Enable", image=self.images.get("enable"))

        # Update code to copy
        self.copy_button.code = self._get_copy_code()


class ThemeManager:
    """Manages application theming"""

    def __init__(self, window: CTk, theme: ThemeConfig):
        self.window = window
        self.theme = theme
        self._setup_theme()

    def _setup_theme(self):
        try:
            if IS_WINDOWS_11:
                ApplyMica(
                    HWND=self.window.frame(), Theme=MicaTheme.DARK, Style=MicaStyle.ALT
                )
            else:
                self._apply_fallback_theme()
        except Exception:
            self._apply_fallback_theme()

    def _apply_fallback_theme(self):
        ThemeConfig.primary_color = "#202020"
        ThemeConfig.secondary_color = "#2F2F2F"
        ThemeConfig.button_color = "#414141"
        ThemeConfig.button_hover_color = "#494949"

        self.window.configure(fg_color=self.theme.fallback_bg_color)


class ReleaseHistoryFeature:
    """Release history popup feature"""

    def __init__(self, window: CTk, theme: ThemeConfig, images: ImageManager):
        self.window = window
        self.theme = theme
        self.images = images
        self.release_history_data = {
            "v1.4.0": [
                "Add new feature for customizing the corner radius of the window using window_dwm.set_corner_radius()",
                "Add new feature for manipulating the non-client area of the window using window_dwm.set_nonclient_area()",
                "Fix the issue with stylize text not looking for changes made by the user by implementing proper title change detection",
                "Fix the issue with title text not being consistent on older versions of Windows by adding fallback rendering",
                "Add support for x86/x32 python architecture by implementing proper pointer size handling",
            ],
            "v1.3.7": [
                "Fix color conversion issue which returned the wrong color when the windows accent color was set to a custom color",
                "Add handling for WM_NCACTIVATE and WM_NCPAINT messages to improve title bar rendering",
                "Add dynamic height adjustment to hide_titlebar method using the no_span parameter",
            ],
            "v1.3.6": ["Minor Bug Fixes"],
            "v1.3.5": [
                "Add feature for automatically changing the accent color of the titlebar and border",
                "Fix an issue which caused ImportError when used with a python version less than 3.9",
            ],
            "v1.3.4": [
                "Add method for applying the current windows accent color to the titlebar and border color",
                "Add method for getting the current windows accent color",
                "Add type annotations and docstrings to functions for better clarity and autocompletion",
            ],
            "v1.3.3": ["Fixed taskbar unhide/hide bug"],
            "v1.3.2": [
                "Add support for synchronizing the rainbow effect with other ui elements."
            ],
            "v1.3.1": [
                "Add support for UI libraries like Kivy, PySimpleGUI, PyGame, etc.",
                "Improve the rainbow titlebar & border effects.",
                "Improve the center_relative function & examples.",
            ],
            "v1.3.0": [
                "Add support for setting custom border color",
                "Add support for rainbow border color effect",
                "Add support for resetting the titleBar color and titleText color",
                "Fix an issue which caused the titleBar to appear black after the rainbow titleBar effect was stopped",
            ],
            "v1.2.1": ["Minor Bug Fixes"],
            "v1.2.0": [
                "Add support for rainbow titlebar",
                "Add support for styling title text",
                "Add support for vertical, horizontal shake and circle motion window animations",
                "Add support for centering a window on the screen",
                "Add support for centering a window relative to another window",
                "Add support for moving/resizing/maximizing/minimizing/restoring a window",
                "Add support for setting custom titlebar color",
                "Add support for setting custom titlebar text color",
            ],
            "v1.1.3": ["Add flashing interval support"],
            "v1.1.2": [
                "Add window flashing support",
                "Add window opacity support",
                "Add support for PyGTK",
            ],
            "v1.1.1": ["Add support for WxPython, PyQt and PySide"],
            "v1.1.0": ["Initial Release"],
        }

    def create_button(self, parent: CTkFrame) -> CTkButton:
        """Creates the release history button"""
        return CTkButton(
            parent,
            text="",
            image=self.images.get("history"),
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            font=("Segoe UI", 15),
            width=20,
            command=self.show_history,
        )

    def show_history(self):
        """Shows the release history popup"""
        top = CTkToplevel(self.window)
        top.geometry("500x500")
        top.title("")
        top.transient(self.window)
        self.window.wm_attributes("-disabled", True)
        top.configure(fg_color=self.theme.primary_color)
        top.withdraw()

        def on_close():
            self.window.wm_attributes("-disabled", False)
            top.destroy()

        CTkLabel(top, text="hPyT Release History", font=("Segoe UI", 25, "bold")).pack(
            pady=10
        )

        main_frame = CTkScrollableFrame(top, fg_color=self.theme.primary_color)
        main_frame.pack(pady=10, fill="both", expand=True)

        for version, changes in self.release_history_data.items():
            version_frame = CTkFrame(main_frame, fg_color=self.theme.secondary_color)
            version_frame.pack(pady=10, padx=10, fill="x")

            CTkLabel(
                version_frame,
                text=version,
                font=("Segoe UI", 22, "bold"),
                fg_color=self.theme.secondary_color,
            ).grid(row=0, column=0, sticky="w", padx=15, pady=(5, 0))

            changes_frame = CTkFrame(version_frame, fg_color=self.theme.secondary_color)
            changes_frame.grid(row=1, column=0, sticky="w", padx=15, pady=5)

            for change in changes:
                CTkLabel(
                    changes_frame,
                    text=f"• {change}",
                    font=("Segoe UI", 14),
                    fg_color=self.theme.secondary_color,
                    wraplength=420,
                    justify="left",
                ).pack(pady=2, anchor="w", padx=5)

        try:
            ApplyMica(HWND=top.frame(), Theme=MicaTheme.DARK, Style=MicaStyle.ALT)
        except Exception:
            top.configure(fg_color=self.theme.fallback_bg_color)
            main_frame.configure(fg_color=self.theme.fallback_bg_color)

        top.bind("<Escape>", lambda event: on_close())
        top.protocol("WM_DELETE_WINDOW", on_close)
        window_frame.center_relative(self.window, top)
        top.deiconify()
        top.focus_set()
        top.iconbitmap("assets/transparent.ico")


class HPyTPreview:
    """Main application class"""

    def __init__(self):
        self.theme = ThemeConfig()
        self.window = CTk()
        self.image_manager = ImageManager()
        self.theme_manager = ThemeManager(self.window, self.theme)
        self.release_history = ReleaseHistoryFeature(
            self.window, self.theme, self.image_manager
        )

        self.window.withdraw()
        self.setup_window()
        self.create_ui()

    def setup_window(self):
        self.window.title("hPyT - Preview")
        self.window.iconbitmap("assets/icon.ico")
        self.window.configure(fg_color=self.theme.primary_color)

    def create_ui(self):
        self.main_frame = CTkFrame(self.window, fg_color=self.theme.primary_color)

        self._create_top_frame()
        self._create_feature_frames()
        self._create_info_label()

        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.main_frame.update()

        self.window.geometry(
            f"{self.main_frame.winfo_reqwidth()}x{self.main_frame.winfo_reqheight()}"
        )

    def _create_top_frame(self):
        top_frame = CTkFrame(self.main_frame, fg_color=self.theme.primary_color)
        top_frame.grid(
            row=0, column=0, sticky="nsew", padx=10, pady=(0, 10), columnspan=6
        )

        # Add release history button
        release_history_button = self.release_history.create_button(top_frame)
        release_history_button.place(x=10, y=10)

        # Add GitHub button
        github_button = CTkButton(
            top_frame,
            text="",
            image=self.image_manager.get("github"),
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            font=("Segoe UI", 15),
            width=20,
            command=lambda: open_link("https://github.com/zingzy/hPyT"),
        )
        github_button.place(x=918, y=10)

        # Add PyPI button
        pypi_button = CTkButton(
            top_frame,
            text="",
            image=self.image_manager.get("pypi"),
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            font=("Segoe UI", 15),
            width=20,
            command=lambda: open_link("https://pypi.org/project/hPyT"),
        )
        pypi_button.place(x=964, y=10)

        CTkLabel(
            top_frame,
            text="hPyT - Hack Python Titlebar Preview",
            font=("Segoe UI", 25, "bold"),
        ).pack(padx=10, pady=10)

        CTkLabel(
            top_frame,
            text="A package for manipulating windows and titlebar of GUI applications made using Python.",
            wraplength=700,
            font=("Segoe UI", 13),
            justify="center",
            fg_color=self.theme.primary_color,
        ).pack(padx=10, pady=(0, 5))

    def _create_feature_frames(self):
        # Row 1
        self.title_bar_feature = TitleBarFeature(
            self.main_frame, self.theme, self.window, self.image_manager
        )
        self.title_bar_feature.grid(
            row=1, column=0, sticky="nsew", padx=(10, 0), pady=(10, 0)
        )

        self.rainbow_title_bar_feature = RainbowTitleBarFeature(
            self.main_frame, self.theme, self.window, self.image_manager
        )
        self.rainbow_title_bar_feature.grid(
            row=1, column=1, sticky="nsew", padx=(10, 0), pady=(10, 0)
        )

        self.rainbow_border_feature = RainbowBorderFeature(
            self.main_frame, self.theme, self.window, self.image_manager
        )
        self.rainbow_border_feature.grid(
            row=1, column=2, sticky="nsew", padx=(10, 0), pady=(10, 0)
        )

        self.maximize_minimize_feature = MaximizeMinimizeFeature(
            self.main_frame, self.theme, self.window, self.image_manager
        )
        self.maximize_minimize_feature.grid(
            row=1, column=3, sticky="nsew", padx=(10, 0), pady=(10, 0)
        )

        self.all_stuffs_feature = AllStuffsFeature(
            self.main_frame, self.theme, self.window, self.image_manager
        )
        self.all_stuffs_feature.grid(
            row=1, column=4, sticky="nsew", padx=(10, 0), pady=(10, 0)
        )

        self.accent_titlebar_feature = AccentTitlebarFeature(
            self.main_frame, self.theme, self.window, self.image_manager
        )
        self.accent_titlebar_feature.grid(
            row=1, column=5, sticky="nsew", padx=10, pady=(10, 0)
        )

        # Row 2
        self.relative_center_feature = RelativeCenterFeature(
            self.main_frame, self.theme, self.window
        )
        self.relative_center_feature.grid(
            row=2, column=0, sticky="nsew", padx=(10, 0), pady=(10, 5)
        )

        self.corner_radius_feature = CornerRadiusFeature(
            self.main_frame, self.theme, self.window
        )
        self.corner_radius_feature.grid(
            row=2, column=1, sticky="nsew", padx=(10, 0), pady=(10, 5)
        )

        self.flash_feature = WindowFlashFeature(
            self.main_frame, self.theme, self.window
        )
        self.flash_feature.grid(
            row=2, column=2, sticky="nsew", padx=(10, 0), pady=(10, 5)
        )

        self.opacity_feature = OpacityFeature(self.main_frame, self.theme, self.window)
        self.opacity_feature.grid(
            row=2, column=3, sticky="nsew", padx=(10, 0), pady=(10, 5)
        )

        self.transitions_feature = TransitionsFeature(
            self.main_frame, self.theme, self.window, self.image_manager
        )
        self.transitions_feature.grid(
            row=2, column=4, sticky="nsew", padx=(10, 0), pady=(10, 5)
        )

        self.stylized_text_feature = StylizedTextFeature(
            self.main_frame, self.theme, self.window
        )
        self.stylized_text_feature.grid(
            row=2, column=5, sticky="nsew", padx=10, pady=(10, 5)
        )

    def _create_info_label(self):
        CTkLabel(
            self.main_frame,
            text="Check out the documentation for more commands",
            font=("Segoe UI", 13),
            justify="center",
            fg_color=self.theme.primary_color,
        ).grid(row=3, column=0, columnspan=6, pady=(0, 5))

    def run(self):
        window_frame.center(self.window)
        self.window.deiconify()
        self.window.mainloop()


def main():
    app = HPyTPreview()
    app.run()
