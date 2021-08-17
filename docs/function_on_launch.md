## The start function

To set function to work immediately after the app launches, use **function** parameter 

```python
import photongui

def main():
    window = photongui.createWindow()
    print("Window is created")

photongui.start(function=main)
```

To pass arguments to the function during launch, use **parameters**

```python
import photongui 

def main(text):
    window = photongui.createWindow()
    print("Window is created", text)

photongui.start(function=main, parameters=["LOL"])
```

**Note:** You have to pass the arguments inside a list like in the previous example