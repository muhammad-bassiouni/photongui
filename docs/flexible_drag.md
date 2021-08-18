## Flexible drag

**Flexible drag** allows you to drag the window from specific element, this is usually helpful when you set **borderless** to be True.

In order to make flexible drag work:
- You have to activate **flexible_drag** in window settings
- You have to set element class name to be **window-drag-area**

```python
import photongui


html = """
<html>
    <h1 class='window-drag-area'>This is the drag area</h1>
</html>
"""

settings = {
    "flexible_drag":True,
    "view":html
}

window = photongui.createWindow(window_settings=settings)


photongui.start()
```

Here is another example but with borderless window

```python
import photongui


html = """
<html>
    <h1 class='window-drag-area'>This is the drag area</h1>
</html>
"""

settings = {
    "borderless":True,
    "flexible_drag":True,
    "view":html
}

window = photongui.createWindow(window_settings=settings)


photongui.start()
```

Here is another example with borderless window and button to close the window

```python
import photongui
from photongui import Util

util = Util()
util.exposeAll("closeWindow", locals())


html = """
<html>
    <h1 class='window-drag-area'>This is the drag area</h1>
    
    <h1>Click button below to close the window</h1>
    <button title='click to close window'>X</button>

    <script>
        document.querySelector("button").addEventListener("click", close);
        function close(){
            window.execPy(window.closeWindow, "MainWindow.window.destroy()")
        }
    </script>
</html>
"""

settings = {
    "borderless":True,
    "flexible_drag":True,
    "view":html
}

MainWindow = photongui.createWindow(window_settings=settings)


photongui.start()
```