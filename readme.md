# hPyT - Hide Python Titlebar

A package to manipulate window titlebar in GUI applications.
**Supports Both Windows 11 and 10**

## Supported Libraries

- Tkinter & CustomTkinter
- PyQt
- PySide
- WxPython
- support for more libraries soon...

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

![Hidden Title Bar](https://github.com/Zingzy/hPyT/assets/90309290/c6422973-59ad-40b4-bcfe-01a99d423e6c)

## Hide/Unhide both Maximize and Minimize Buttons (Completely Hides both buttons)

```python
maximize_minimize_button.hide(window) # hides both maximize and minimize button
# maximize_minimize_button.unhide(window)
```

![Hidden Maximize and Minimize Buttons](https://github.com/Zingzy/hPyT/assets/90309290/080c1f8c-905a-4a4d-aa20-30956aae91d0)

## Hide/Unhide All Buttons or Stuffs

```python
all_stuffs.hide(window) # hides close button
# all_stuffs.unhide(window)
```

![Hide Everything](https://github.com/Zingzy/hPyT/assets/90309290/f6afa5ed-c82d-460a-8a37-77cfc50f9aa5)

_**Tip:** to hide the text set the window title to ''_

## Enable/Disable Maximize Button

```python
maximize_button.disable(window) # hides maximize button
# MaximizeButton.enable(window)
```

![Disabled Maximize Button](https://github.com/Zingzy/hPyT/assets/90309290/c25cffea-8e9b-484d-9dec-0f0453161ad8)

## Enable/Disable Minimize Button

```python
minimize_button.disable(window) # hides minimize button
# MinimizeButton.enable(window)
```

![Disabled Minimize Button](https://github.com/Zingzy/hPyT/assets/90309290/c49e3ff9-3367-4101-b99e-43f05bd2c6f4)
