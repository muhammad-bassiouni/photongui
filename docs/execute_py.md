## Execute Python code from window

```python
import photongui
from photongui import Util

util = Util()
util.exposeAll(name="mainApp", environ=locals())

window = photongui.createWindow()

def print_url():
    currentUrl = window.getUrl()
    print(currentUrl)

photongui.start(debug=True)
```

To execute Python code from JS:

- You have to expose local variables and functions to the window.
  
    In the previous example we have imported **Util** from **photongui**, we are going to use it to expose all local functions and variables to the window.

    ```python
    util = Util()
    util.exposeAll(name="mainApp", environ=locals())
    ```
    **exposeAll()**
    | Parameters | Details |
    |---|---|
    | name       | the exposed environment name that you will use to access it later |
    | environ    | you have to set its value to be **locals()** |


Now you are ready to go and get value of any variable or execute any function and get its return value from this environment.

- In your JS code, you can execute python code using `window.execPy`
    ```javascript
    window.execPy(window.mainApp, "print_url()")
    ```
   
    **window.execPy()**
    | Parameters | Details |
    |---|---|
    | environ       | is the environment name we have exposed in python. You can access it by typing **window.&lt;The name you have set in python&gt;** which is **mainApp** in the previous example |
    | pythonCode    | python code you want to execute, it has to be string |

  
You notice **mainApp** in **window.mainApp** is the same name we used to expose things in python.

---

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