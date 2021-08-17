## Parent window

To set the parent window, use **parent** parameter. inside **photongui.createWindow()**.



```python
import photongui

parentWindow = photongui.createWindow(window_settings={"title":"Parent window"})


childWindow = photongui.createWindow(window_settings={"title":"Modal window"}, parent=parentWindow)

photongui.start()
```