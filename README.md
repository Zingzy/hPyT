# hPyT - Hack Python Titlebar

A package to manipulate windows and titlebar of GUI applications made using python
**Supports Both Windows 11 and 10**

https://github.com/Zingzy/hPyT/assets/90309290/f86df1c7-b75b-4477-974a-eb34cc117df3

**You can download the above app from the [github releases](https://github.com/Zingzy/hPyT/releases/tag/hPyT-preview/) to test out the package before installing/using it in your projects**

<br>

<details>

<summary>📖 Table of Contents</summary>

- [hPyT - Hack Python Titlebar](#hpyt---hack-python-titlebar)
	- [📚 Supported Libraries](#-supported-libraries)
	- [📦 Installing](#-installing)
	- [📥 Importing](#-importing)
	- [Hide/Unhide TitleBar](#hideunhide-titlebar)
			- [**Understanding Window Geometry**](#understanding-window-geometry)
			- [**Impact of Hiding the Title Bar**](#impact-of-hiding-the-title-bar)
			- [**Potential Issues**](#potential-issues)
			- [**Solution**](#solution)
			- [Example Usage](#example-usage)
			- [Comparision of the dimensions with and without `no_span=True`:](#comparision-of-the-dimensions-with-and-without-no_spantrue)
			- [Visual Example:](#visual-example)
	- [🌈 Rainbow TitleBar](#-rainbow-titlebar)
	- [🌈 Rainbow Border](#-rainbow-border)
		- [🔄 Synchronizing the Rainbow Effect with other elements](#-synchronizing-the-rainbow-effect-with-other-elements)
	- [Hide/Unhide both Maximize and Minimize Buttons (Completely Hides both buttons)](#hideunhide-both-maximize-and-minimize-buttons-completely-hides-both-buttons)
	- [Hide/Unhide All Buttons or Stuffs](#hideunhide-all-buttons-or-stuffs)
	- [Enable/Disable Maximize Button](#enabledisable-maximize-button)
	- [Enable/Disable Minimize Button](#enabledisable-minimize-button)
	- [Opacity](#opacity)
	- [⚡ Flashing Window](#-flashing-window)
	- [🎨 Custom TitleBar Color](#-custom-titlebar-color)
		- [Set TitleBar Color to windows Accent Color](#set-titlebar-color-to-windows-accent-color)
	- [🖌️ Custom TitleBar Text Color](#️-custom-titlebar-text-color)
	- [🖌️ Custom Border Color](#️-custom-border-color)
		- [Set Border Color to windows Accent Color](#set-border-color-to-windows-accent-color)
	- [💻 Window Management](#-window-management)
		- [Center a window on the screen](#center-a-window-on-the-screen)
		- [Center a secondary window relative to the primary window](#center-a-secondary-window-relative-to-the-primary-window)
		- [Other basic window management functions](#other-basic-window-management-functions)
	- [✨ Window Animations](#-window-animations)
		- [Circle Motion](#circle-motion)
		- [Verical Shake](#verical-shake)
		- [Horizontal Shake](#horizontal-shake)
	- [✏️ Stylize text](#️-stylize-text)
	- [Miscellaneous](#miscellaneous)
	- [Get Windows Accent Color](#get-windows-accent-color)
	- [Stylize text](#stylize-text)
	- [Workaround for other libraries](#workaround-for-other-libraries)
	- [📜 hPyT Changelog](#-hpyt-changelog)
		- [v1.3.7](#v137)
		- [v1.3.6](#v136)
		- [v1.3.5](#v135)
		- [v1.3.4](#v134)
		- [v1.3.3](#v133)
		- [v1.3.2](#v132)
		- [v1.3.1](#v131)
		- [v1.3.0](#v130)
		- [v1.2.1](#v121)
		- [v1.2.0](#v120)
		- [v1.1.3](#v113)
		- [v1.1.2](#v112)
		- [v1.1.1](#v111)
		- [v1.1.0](#v110)
</details>

---

## 📚 Supported Libraries

- Tkinter & CustomTkinter
- PyQt
- PySide
- WxPython
- Kivy
- And many more

## 📦 Installing

```powershell
pip install hPyT==1.3.7
```

## 📥 Importing

```python
from hPyT import *
from customtkinter import * # you can use any other library from the above mentioned list

window = CTk() # creating a window using CustomTkinter
```

## Hide/Unhide TitleBar

```python
title_bar.hide(window, no_span = False) # hides full titlebar
# optional parameter : no_span, more details in the note below
# title_bar.unhide(window)
```

![Hide Titlebar preview](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/titlebar.png)

<details>
<summary><h3>❗Important Note when hiding the titlebar</h3></summary>

When hiding a title bar, the application window's total geometry and its content area geometry behave differently, which may introduce ambiguities. Here's a detailed explanation of the issue:

#### **Understanding Window Geometry**

1. **Full Window Dimensions**:
   - Includes the content area, title bar, and borders.
   - When the user specifies dimensions (e.g., `400x400`), it usually represents the **content area dimensions**. The total window height becomes `content height + title bar height + border width`.
   - The color of the `top border` and `title bar` is usually the same, making it appear as a single entity.

2. **Content Area Dimensions**:
   - Represents only the usable area inside the window, excluding the title bar and borders.

#### **Impact of Hiding the Title Bar**

When the title bar is hidden:
- The **content area height** expands to occupy the height previously used by the title bar. For example, a `400x400` content area might expand to `400x438` (assuming the visual title bar height is 38px).

Better illustrated in the following example:

```py
...

def show_window_dimensions():
    hwnd: int = ctypes.windll.user32.GetForegroundWindow()

    x_with_decorations: int = root.winfo_rootx()  # X position of the full window
    y_with_decorations: int = root.winfo_rooty()  # Y position of the full window

    x_without_decorations: int = root.winfo_x()  # X position of the content area
    y_without_decorations: int = root.winfo_y()  # Y position of the content area

    titlebar_height: int = y_with_decorations - y_without_decorations
    border_width: int = x_with_decorations - x_without_decorations

    window_rect: RECT = get_window_rect(hwnd)

    width: int = window_rect.right - window_rect.left
    height: int = window_rect.bottom - window_rect.top

    print(f"Title bar height: {titlebar_height}")
    print(f"Border width: {border_width}")
    print(f"Main window dimensions: {width}x{height}")
    print(
        f"Content window dimensions: {root.winfo_geometry()}"
    )  # This will return the dimensions of the content area only

...

def click(e=None):
    root.update_idletasks()

    print("------ Before hiding title bar ------")
    show_window_dimensions()

	title_bar.hide(root)
	is_hidden = True

    print("------ After hiding title bar ------")
    show_window_dimensions()


button = CTkButton(root, text="Click Me", command=click)
button.place(relx=0.5, rely=0.5, anchor="center")

root.mainloop()
```

Output:

```cmd
------ Before hiding title bar ------
Title bar height: 38
Border width: 9
Main window dimensions: 468x497
Content window dimensions: 450x450
------ After hiding title bar ------
Title bar height: 0
Border width: 9
Main window dimensions: 468x497
Content window dimensions: 450x488
```

By the above example, you can see that the content area height has increased from `450px` to `488px` after hiding the title bar.

#### **Potential Issues**
This automatic resizing may cause layout problems or unintended behavior in some applications. For instance:
- UI elements might **overlap** or **stretch**.
- Custom layouts may require recalibration.

#### **Solution**
To address this, a `no_span` parameter is introduced in the `hide` method. This parameter allows users to control whether the content area height should be adjusted dynamically to maintain its original size.

- **Default Behavior (`no_span=False`)**:
  The content area height will expand to occupy the title bar's space.
- **With `no_span=True`**:
  The content area will be resized dynamically to maintain its original dimensions.

#### Example Usage

```python
title_bar.hide(root, no_span=True)
```

#### Comparision of the dimensions with and without `no_span=True`:

```diff
- Content window dimensions: 450x488
+ Content window dimensions: 450x450

- Main window dimensions: 468x497
+ Main window dimensions: 468x459
```

#### Visual Example:

<table align="center">
  <thead>
    <tr>
      <th><code>no_span = False</code></th>
      <th><code>no_span = True</code></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center"><img src="https://raw.githubusercontent.com/Zingzy/hPyT/main/.github/assets/span.gif" alt="Height of the Content area changes when the no_span paramer is set to False by default" width=300></td>
      <td align="center"><img src="https://raw.githubusercontent.com/Zingzy/hPyT/main/.github/assets/no_span.gif" alt="Height of the Content area does not change when the no_span paramer is set to False by default" width=300></td>
    </tr>
  </tbody>
</table>

---

</details>

## 🌈 Rainbow TitleBar

```python
rainbow_title_bar.start(window, interval=5) # starts the rainbow titlebar
# rainbow_title_bar.stop(window) # stops the rainbow titlebar
```

> [!NOTE]
> *`interval` is the time in milliseconds in which the color would change*

![Rainbow TitleBar](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/rainbow_titlebar.gif)

## 🌈 Rainbow Border

```python
rainbow_border.start(window, interval=4) # starts the rainbow border
# rainbow_border.stop(window) # stops the rainbow border
```

![Rainbow Border](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/rainbow_border.gif)

### 🔄 Synchronizing the Rainbow Effect with other elements

```python
from hPyT import *

...

rainbow_title_bar.start(window, interval=30) # starts the rainbow titlebar
# rainbow_border.start(window, interval=30) # also works with rainbow border

current_color = rainbow_title_bar.get_current_color() # or rainbow_border.get_current_color()
# you can use this color to synchronize the color of other elements with the titlebar
```

![synchronization example](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/synchronization-example.gif)


**Code for the above illustration available in [`/examples/rainbow-synchronization-example.py`](https://github.com/Zingzy/hPyT/blob/main/examples/rainbow-synchronization-example.py)**


## Hide/Unhide both Maximize and Minimize Buttons (Completely Hides both buttons)

```python
maximize_minimize_button.hide(window) # hides both maximize and minimize button
# maximize_minimize_button.unhide(window)
```

![Hidden Maximize and Minimize Buttons](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/maximize_minimize.png)

## Hide/Unhide All Buttons or Stuffs

```python
all_stuffs.hide(window) # hides close button
# all_stuffs.unhide(window)
```

![Hide Everything](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/all_stuffs.png)

_**Tip:** to hide the text set the window title to `''`_

## Enable/Disable Maximize Button

```python
maximize_button.disable(window) # hides maximize button
# MaximizeButton.enable(window)
```

![Disabled Maximize Button](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/maximize.png)

## Enable/Disable Minimize Button

```python
minimize_button.disable(window) # hides minimize button
# MinimizeButton.enable(window)
```

![Disabled Minimize Button](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/minimize.png)

## Opacity

```python
opacity.set(window, 0.5) # sets the window opacity to 50%
# opacity.set(window, 1) # resets the window opacity to 100%
```

![Opacity 0.5 preview](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/opacity.png)

## ⚡ Flashing Window

```python
window_flash.flash(window, 10, 100) # flashes the window 10 times with 100ms interval
# window_flash.stop(window) # stops the flashing immediately
```

*Flashing Interval starts from 10ms, **default 1000ms***

![Flashing Window](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/flashing.gif)

## 🎨 Custom TitleBar Color

```python
title_bar_color.set(window, '#ff00ff') # sets the titlebar color to magenta
# title_bar_color.reset(window) # resets the titlebar color to default
```

> [!NOTE]
> *You can pass any valid color in `Hex` or `RGB` format*

![Custom TitleBar Color](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/titlebar_color.png)

### Set TitleBar Color to windows Accent Color

```python
title_bar_color.set_accent(window) # sets the titlebar color to the current windows accent color
```

![Accent TitleBar](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/accent_titlebar.png)

> [!NOTE]
> *The titlebar color will automatically change when the windows accent color changes*

## 🖌️ Custom TitleBar Text Color

```python
title_text_color.set(window, '#ff00ff') # sets the titlebar text color to magenta
# title_text_color.reset(window) # resets the titlebar text color to default
```

![Custom TitleBar Text Color](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/title_text_color.png)

## 🖌️ Custom Border Color

```python
border_color.set(window, '#ff00ff') # sets the border color to magenta
# border_color.reset(window) # resets the border color to default
```

![Custom Border Color](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/border_color.png)

### Set Border Color to windows Accent Color

```python
border_color.set_accent(window) # sets the border color to the current windows accent color
```

![Accent Border](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/accent_border.png)

> [!NOTE]
> *The border color will automatically change when the windows accent color changes*

## 💻 Window Management

### Center a window on the screen

```python
window_frame.center(window)
```

### Center a secondary window relative to the primary window

```python
window_frame.center_relative(window, child_window)
```

![Center Relative](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/center_relative.png)

**Example Usecase**

```python
window = CTk()
window.title("Primary Window")
window.geometry('600x300')
window_frame.center(window)

child_window = CTkToplevel()

window_frame.center_relative(window, child_window)

window.bind("<Configure>", lambda event: window_frame.center_relative(window, child_window))

def on_close():  # this is required to stop the window from centering the child window after the parent window is closed
	window.unbind("<Configure>")
	child_window.destroy()

child_window.protocol("WM_DELETE_WINDOW", on_close)

window.mainloop()
```

![Center Relative Example](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/center_relative_example.gif)

### Other basic window management functions

```python
window_frame.move(window, 100, 100) # moves the window to (100, 100)
window_frame.resize(window, 500, 500) # resizes the window to 500x500
window_frame.maximize(window) # maximizes the window
window_frame.minimize(window) # minimizes the window
window_frame.restore(window) # restores the window
```

## ✨ Window Animations

### Circle Motion

```python
window_animation.circle_motion(window, count=5, interval=5, radius=30)
# moves the window in a circular motion 5 times with 5ms interval and 30px radius
```

![Circle Motion](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/circle_motion.gif)

*The animation might appear a bit fasterer and rougher in the above preview gif than it is*

### Verical Shake

```python
window_animation.vertical_shake(window, count=5, interval=5, amplitude=20)
# shakes the window vertically 5 times with 5ms interval and 10px distance
```

### Horizontal Shake

```python
window_animation.horizontal_shake(window, count=5, interval=5, amplitude=20)
# shakes the window horizontally 5 times with 5ms interval and 10px distance
```

## ✏️ Stylize text

```python
title_text.stylize(window, style=1)
```

*Below is a gif demonstrating all of the available styles*

![Stylize Text](https://raw.githubusercontent.com/zingzy/hPyT/main/.github/assets/stylize_text.gif)

## Miscellaneous

## Get Windows Accent Color

```python
print(get_accent_color()) # prints the current windows accent color
>>> '#1b595a'
```

## Stylize text

```python
print(stylize_text("Your Custom Text", style=1)) # stylizes your text
# all of the styles shown on the above gif are available
>>> "𝔜𝔬𝔲𝔯 ℭ𝔲𝔰𝔱𝔬𝔪 𝔗𝔢𝔵𝔱"
```

## Workaround for other libraries

This menthod is applicable for any other UI library like <kbd>pygame</kbd> <kbd>pySimpleGUI</kbd>, etc. which are not mentioned in the [supported libraries list](#-supported-libraries). You just need to pass the `hwnd` of the window to the functions as demonstrated below.

```python
from hPyT import *
import ctypes

hwnd = ctypes.windll.user32.GetActiveWindow()
rainbow_border.start(hwnd)
```

<br>

## 📜 hPyT Changelog

### v1.3.7

- Fix color conversion issue which returned the wrong color when the windows accent color was set to a custom color
- Add handling for WM_NCACTIVATE and WM_NCPAINT messages to improve title bar rendering
- Add dynamic height adjustment to hide_titlebar method using the no_span parameter

### v1.3.6

- Minor Bug Fixes

### v1.3.5

- Add feature for automatically changing the accent color of the titlebar and border
- Fix an issue which caused ImportError when used with a python version less than 3.9

### v1.3.4

- Add method for applying the current windows accent color to the titlebar and border color
- Add method for getting the current windows accent color
- Add type annotations and docstrings to functions for better clarity and autocompletion

### v1.3.3

- Fixed taskbar unhide/hide bug

### v1.3.2

- Add support for synchronizing the rainbow effect with other ui elements.

### v1.3.1

- Add support for UI libraries like Kivy, PySimpleGUI, PyGame, etc.
- Improve the rainbow titlebar & border effects.
- Improve the center_relative function & examples.

### v1.3.0

- Add support for setting custom border color
- Add support for rainbow border color effect
- Add support for resetting the titleBar color and titleText color
- Fix an issue which caused the titleBar to appear black after the rainbow titleBar effect was stopped

### v1.2.1

- Minor Bug Fixes

### v1.2.0

- Add support for rainbow titlebar
- Add support for styling title text
- Add support for vertical, horizontal shake and circle motion window animations
- Add support for centering a window on the screen
- Add support for centering a window relative to another window
- Add support for moving/resizing/maximizing/minimizing/restoring a window
- Add support for setting custom titlebar color
- Add support for setting custom titlebar text color

### v1.1.3

- Add flashing inverval support

### v1.1.2

- Add window flashing support
- Add window opacity support
- Add support for PyGTK

### v1.1.1

- Add support for WxPython, PyQt and PySide

### v1.1.0

- Initial Release

<br>

![PyPI](https://img.shields.io/pypi/v/hPyT?style=flat-square)
![Python](https://img.shields.io/badge/python-3.6+-blue)
![Downloads](https://img.shields.io/pypi/dm/hPyT?style=flat-square)
![Stars](https://img.shields.io/github/stars/zingzy/hPyT?style=flat-square)
![Contributors](https://img.shields.io/github/contributors/zingzy/hPyT?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/zingzy/hPyT?style=flat-square)

---

<h6 align="center">
© zingzy . 2024

All Rights Reserved</h6>

<p align="center">
	<a href="https://github.com/zingzy/hPyT/blob/master/LICENSE"><img src="https://img.shields.io/static/v1.svg?style=for-the-badge&label=License&message=MIT&logoColor=d9e0ee&colorA=363a4f&colorB=b7bdf8"/></a>
</p>
