## Accessing tkinter window features

To access all tkinter features of the window, use **window** attribute of the created window object

```python
import photongui
import time

MainWindow = photongui.createWindow({"title":"This is the first title"})

def main():
    time.sleep(3)
    MainWindow.window.title("This is the second title") # This will change the window title
    MainWindow.window.geometry("+500+500") # This will change the window position

photongui.start(function=main)
```

There are some other methods that have been added to **window**, like:
- **setIcon()**: To change the window icon
    ```python
    import photongui
    import time

    window = photongui.createWindow()

    def main():
        time.sleep(3)
        window.window.setIcon("<The new icon file path>") 

    photongui.start(function=main)
    ```
- **centerWindow()**: To center the window
    ```python
    import photongui
    import time

    window = photongui.createWindow({"position":(0, 0)})

    def main():
        time.sleep(3)
        window.window.centerWindow() 

    photongui.start(function=main)
    ```

- **toggleFullscreen()**: To reverse the current fullscreen mode
    ```python
    import photongui
    import time

    window = photongui.createWindow({"position":(0, 0)})

    def main():
        time.sleep(3)
        window.window.toggleFullscreen() 

    photongui.start(function=main)
    ```
    To exit the fullscreen press **"Esc"** key

