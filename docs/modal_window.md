## Modal window

To make modal window, use *modal* parameter inside **photongui.createWindow()** and you have to pass the parent window using **parent** parameter.

Modal window disables the parent window.


```python
import photongui

parentWindow = photongui.createWindow(window_settings={"title":"Parent window"})


modalWindow = photongui.createWindow(window_settings={"title":"Modal window"}, parent=parentWindow, modal=True)

photongui.start()
```

To set window as modal later, use **setWindowAsModal()** and you has to pass the parent window

```python
import photongui
import time

parentWindow = photongui.createWindow(window_settings={"title":"Parent window"})
laterModalWindow = photongui.createWindow()

def main():
    time.sleep(3)
    laterModalWindow.setWindowAsModal(parent=parentWindow)

photongui.start(function=main)
```