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