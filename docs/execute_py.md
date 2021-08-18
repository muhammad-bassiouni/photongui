## Execute Python code from window

To execute Python code from window, you have to set somethings first.

- You have to expose local variables and functions to the window

```python
import photongui
from photongui import Util

util = Util()
util.exposeAll(name="mainApp", environ=locals())

window = photongui.createWindow()

def main():
    currentUrl = window.getUrl()
    print(currentUrl)

photongui.start(function=main, debug=True)
```
In the previous example we have imported **Util** from **photongui**, we are going to use it to expose all local functions and variables to the window

```python
util = Util()
util.exposeAll(name="mainApp", environ=locals())
```

### using method **exposeAll** to expose locals. 
  - **name**: giving all locals single name to make it easy for accessing them from the window
  - **environ**: you have to set its value to be **locals()**

after doing that, now you are ready to go and get value of any variable or execute any function and get its return value in this environment.

In your JS code, you can execute python code using **window.execPy**
```javascript
window.execPy(window.mainApp, "main()").then(function(r){console.log(r)})
```
**window.execPy(environ, pythonCode)**

- **environ**: is envrion we have exposed in python
    ```python
    util = Util()
    util.exposeAll(name="mainApp", environ=locals())
    ```
    you can access it by typing **window.&lt;The name you have set in python&gt;** which is **mainApp** in the previous example

- **pythonCode**: python code you want to execute, it has to be string.
  
You notice, **window.mainApp** is the same name we used to expose things in python.

### Full example to demonstrate 

```python
import photongui
from photongui import Util

util = Util()
util.exposeAll("math", locals())

def calculate(x, y):
    return x + y

html = """
<html>
    <h1>This is a simple text</h1>
    <p class='x'>5</p>
    <p class='y'>10</p>

    <h1 class='result'>This will be replaced with the result from python</h1>
    <button class="show-result" onclick="calculate()">Calculate</button>
    <script>
        var x = parseInt(document.querySelector('.x').innerText)
        var y = parseInt(document.querySelector('.y').innerText)

        var result_holder = document.querySelector('.result')

        function calculate(){
            window.execPy(window.math, `calculate(${x}, ${y})`)
            .then(function(r){
                    result_holder.innerText = r
                }
            )
        }
    </script>
</html>
"""
settings = {
    "view":html
}

window = photongui.createWindow(window_settings=settings)


photongui.start()
```