## Execute JS code asynchronously


```python
import photongui

window = photongui.createWindow()

def main():
    window.execJsAsync("document.body.style.background = 'green'")

photongui.start(function=main)
```