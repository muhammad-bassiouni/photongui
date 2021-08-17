## Getting the view URL


```python
import photongui

window = photongui.createWindow()

def main():
    currentUrl = window.getUrl()
    print(currentUrl)

photongui.start(function=main)
```