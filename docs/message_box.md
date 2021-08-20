## Message box

**messagebox(action, title, message)**

- **action**:
  #### Available actions:
  - **warning**
  - **info**
  - **error**
  - **question**
  - **okcancel**
  - **yesnocancel**
  - **yesno**

- **title**: Title of the message box

- **message**: Message box content

```python
import photongui
from photongui import Util

util = Util()
util.exposeAll("closeWindow", locals())


html = """
<html>
    <h1>Click button below to close the window</h1>
    <button title='click to close window'>X</button>

    <script>
        document.querySelector("button").addEventListener("click", close);
        function close(){
            window.execPy(window.closeWindow, "closeWindow()")
        }
    </script>
</html>
"""

settings = {
    "view":html
}

window = photongui.createWindow(settings)

def closeWindow():
    answer = window.messagebox("yesno", "Close window", "Do you want to close the window?") 
    if answer == True:
        window.window.destroy()
    else:
        pass

photongui.start()
```