## Debugging

To allow debugging set `debug` parameter to `True`


```python
import photongui

window = photongui.createWindow()

photongui.start(debug=True)
```

Now right-click on the window and you can access **Developer Tools**.

You can also specify the logging level by passing `debug_level`

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