## Load snippet

**loadSnippet(elementSelector, snippet, position)**

To update specific part of the current view without affecting the whole view.

- **elementSelector**: like *.drag-area* to select class, or *h1* to select **h1 tag**
- **snippet**: the snippet you want to load to the view
- **position**: the place where you want to load your snippet relative to the **elementSelector**
  
  ### Available positions
  - **'beforebegin'**: Before the element itself.
  - **'afterbegin'**: Just inside the element, before its first child. 
  - **'beforeend'**: Just inside the element, after its last child.
  - **'afterend'**: After the element itself.

```python
import photongui
import time

window = photongui.createWindow()

snippet = """
<p>This is injected snippet</p>
"""

def main():
    time.sleep(3)
    window.loadSnippet("h1", snippet, "afterend")

photongui.start(function=main)
```
