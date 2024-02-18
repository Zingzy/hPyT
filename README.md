# hPyT - Hack Python Titlebar

A package to manipulate window titlebar in GUI applications.
**Supports Both Windows 11 and 10**

https://github.com/Zingzy/hPyT/assets/90309290/8e7bd413-0673-4986-866b-31aace04e9db

**You can download the above app from the [github releases](https://github.com/Zingzy/hPyT/releases/tag/v1.1.0/) to test out the package before installing/using it in your projects**

## Supported Libraries

- Tkinter & CustomTkinter
- PyQt
- PySide
- WxPython
- support for more libraries soon...

## Installing

```powershell
pip install hPyT==1.1.3
```

## Importing

```python
from hPyT import *
from customtkinter import * # you can use any other library from the above mentioned list

window = CTk()
```

## Hide/Unhide Title Bar

```python
title_bar.hide(window) # hides full titlebar
# title_bar.unhide(window)
```

![Hidden Title Bar](https://raw.githubusercontent.com/zingzy/hPyT/main/assets/titlebar.png)


## Hide/Unhide both Maximize and Minimize Buttons (Completely Hides both buttons)

```python
maximize_minimize_button.hide(window) # hides both maximize and minimize button
# maximize_minimize_button.unhide(window)
```

![Hidden Maximize and Minimize Buttons](https://raw.githubusercontent.com/zingzy/hPyT/main/assets/maximize_minimize.png)

## Hide/Unhide All Buttons or Stuffs

```python
all_stuffs.hide(window) # hides close button
# all_stuffs.unhide(window)
```

![Hide Everything](https://raw.githubusercontent.com/zingzy/hPyT/main/assets/all_stuffs.png)

_**Tip:** to hide the text set the window title to ''_

## Enable/Disable Maximize Button

```python
maximize_button.disable(window) # hides maximize button
# MaximizeButton.enable(window)
```

![Disabled Maximize Button](https://raw.githubusercontent.com/zingzy/hPyT/main/assets/maximize.png)

## Enable/Disable Minimize Button

```python
minimize_button.disable(window) # hides minimize button
# MinimizeButton.enable(window)
```

![Disabled Minimize Button](https://raw.githubusercontent.com/zingzy/hPyT/main/assets/minimize.png)


## Opacity

```python
opacity.set(window, 0.5) # sets the window opacity to 50%
# opacity.set(window, 1) # resets the window opacity to 100%
```

![Opacity 0.5 preview](https://raw.githubusercontent.com/zingzy/hPyT/main/assets/opacity.png)


## Flashing Window

```python
window_flash.flash(window, 10, 100) # flashes the window 10 times with 50ms interval
# window_flash.stop(window) # stops the flashing immediately
```

*Flashing Interval starts from 10ms, **default 1000ms***

![Flashing Window](https://raw.githubusercontent.com/zingzy/hPyT/main/assets/flashing.gif)

<br>

## hPyT Changelog

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

---

<h6 align="center">
© zingzy . 2024

All Rights Reserved</h6>

<p align="center">
	<a href="https://github.com/zingzy/hPyT/blob/master/LICENSE"><img src="https://img.shields.io/static/v1.svg?style=for-the-badge&label=License&message=MIT&logoColor=d9e0ee&colorA=363a4f&colorB=b7bdf8"/></a>
</p>
