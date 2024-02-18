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

<<<<<<< HEAD
![Hidden Title Bar](https://raw.githubusercontent.com/zingzy/hPyT/main/assets/titlebar.png)
=======
![Hidden Title Bar](https://github.com/Zingzy/hPyT/assets/90309290/c7d44243-e5d7-4b84-9872-40b4ea1d562c)
>>>>>>> 3eb02452bbb0fb16a95e03e2aed55c7f9e98d4c0


## Hide/Unhide both Maximize and Minimize Buttons (Completely Hides both buttons)

```python
maximize_minimize_button.hide(window) # hides both maximize and minimize button
# maximize_minimize_button.unhide(window)
```

<<<<<<< HEAD
![Hidden Maximize and Minimize Buttons](https://raw.githubusercontent.com/zingzy/hPyT/main/assets/maximize_minimize.png)
=======
![Hidden Maximize and Minimize Buttons](https://github.com/Zingzy/hPyT/assets/90309290/adb56ede-7362-4972-83ac-9b07e85b6ba9)
>>>>>>> 3eb02452bbb0fb16a95e03e2aed55c7f9e98d4c0

## Hide/Unhide All Buttons or Stuffs

```python
all_stuffs.hide(window) # hides close button
# all_stuffs.unhide(window)
```

<<<<<<< HEAD
![Hide Everything](https://raw.githubusercontent.com/zingzy/hPyT/main/assets/all_stuffs.png)
=======
![Hide Everything](https://github.com/Zingzy/hPyT/assets/90309290/9cf14a6d-e432-4610-a90b-3d9918a9a925)
>>>>>>> 3eb02452bbb0fb16a95e03e2aed55c7f9e98d4c0

_**Tip:** to hide the text set the window title to ''_

## Enable/Disable Maximize Button

```python
maximize_button.disable(window) # hides maximize button
# MaximizeButton.enable(window)
```

<<<<<<< HEAD
![Disabled Maximize Button](https://raw.githubusercontent.com/zingzy/hPyT/main/assets/maximize.png)
=======
![Disabled Maximize Button](https://github.com/Zingzy/hPyT/assets/90309290/f61fae95-2514-42fd-b765-ec2935ca576d)
>>>>>>> 3eb02452bbb0fb16a95e03e2aed55c7f9e98d4c0

## Enable/Disable Minimize Button

```python
minimize_button.disable(window) # hides minimize button
# MinimizeButton.enable(window)
```

<<<<<<< HEAD
![Disabled Minimize Button](https://raw.githubusercontent.com/zingzy/hPyT/main/assets/minimize.png)


## Opacity

```python
opacity.set(window, 0.5) # sets the window opacity to 50%
```

![Opacity 0.5 preview](https://raw.githubusercontent.com/zingzy/hPyT/main/assets/opacity.png)


## Flashing Window

```python
window_flash.flash(window, 10) # flashes the window 10 times
# window_flash.stop(window) # stops the flashing immediately
```

![Flashing Window](https://raw.githubusercontent.com/zingzy/hPyT/main/assets/flashing.gif)

<br>

## hPyT Changelog

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
=======
![Disabled Minimize Button](https://github.com/Zingzy/hPyT/assets/90309290/2aa0f412-1510-463c-b280-c3389b513405)

>>>>>>> 3eb02452bbb0fb16a95e03e2aed55c7f9e98d4c0
