# hPyT - Hack Python Titlebar

A package to manipulate window titlebar in GUI applications.
**Supports Both Windows 11 and 10**

https://github.com/Zingzy/hPyT/assets/90309290/cf361814-dacc-4704-8828-3d1ad83c6485

**You can download the above app from the [github releases](https://github.com/Zingzy/hPyT/releases) to test out the package before installing/using it in your projects**

## Supported Libraries

- Tkinter & CustomTkinter
- PyQt
- PySide
- WxPython
- support for more libraries soon...

## Installing

```powershell
pip install hPyT==1.1.1
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

![Hidden Title Bar](https://github.com/Zingzy/hPyT/assets/90309290/c7d44243-e5d7-4b84-9872-40b4ea1d562c)


## Hide/Unhide both Maximize and Minimize Buttons (Completely Hides both buttons)

```python
maximize_minimize_button.hide(window) # hides both maximize and minimize button
# maximize_minimize_button.unhide(window)
```

![Hidden Maximize and Minimize Buttons](https://github.com/Zingzy/hPyT/assets/90309290/adb56ede-7362-4972-83ac-9b07e85b6ba9)

## Hide/Unhide All Buttons or Stuffs

```python
all_stuffs.hide(window) # hides close button
# all_stuffs.unhide(window)
```

![Hide Everything](https://github.com/Zingzy/hPyT/assets/90309290/9cf14a6d-e432-4610-a90b-3d9918a9a925)

_**Tip:** to hide the text set the window title to ''_

## Enable/Disable Maximize Button

```python
maximize_button.disable(window) # hides maximize button
# MaximizeButton.enable(window)
```

![Disabled Maximize Button](https://github.com/Zingzy/hPyT/assets/90309290/f61fae95-2514-42fd-b765-ec2935ca576d)

## Enable/Disable Minimize Button

```python
minimize_button.disable(window) # hides minimize button
# MinimizeButton.enable(window)
```

![Disabled Minimize Button](https://github.com/Zingzy/hPyT/assets/90309290/2aa0f412-1510-463c-b280-c3389b513405)

