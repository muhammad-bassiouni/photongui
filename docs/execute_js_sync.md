## Execute JS code synchronously and get return back


```python
import photongui

window = photongui.createWindow()

def main():
    body = window.execJsSync("document.body.innerText")
    print(body)

photongui.start(function=main)
```