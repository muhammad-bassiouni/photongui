## Debugging

To allow debugging set **debug** parameter to **True**


```python
import photongui

window = photongui.createWindow()

photongui.start(debug=True)
```

By activating this option, you can open devtools and access the console by right click on the window.

### You can also specify the logging level by passing **debug_level**

```python
import photongui

window = photongui.createWindow()

photongui.start(debug=True, debug_level="WARNING")
```

The default **debug_level** value is **INFO**

levels you can use:
- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL