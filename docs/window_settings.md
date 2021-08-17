## Window settings
You can set window settings by passing dictionary of the settings you want to apply on the window

**photongui** supports many window features:

- "title": window title
- "view": local html file OR url of website OR raw html in text format
- "icon": window icon > you pass the icon path and should be .png
- "width": window width
- "height": windo height
- "position": window position on the screen
- "resizable": allow window to be resizable or not
- "disabled": disable window
- "fullscreen": make window satart in fullscreen mode
- "minimized": make window start in minimized mode
- "maximized": make window start in maximized mode
- "min_size": setting the minimum window size
- "max_size": setting the maximum window size
- "hidden": start window in hidden mode
- "borderless": make window without borders "framless"
- "border_color": window border color
- "border_thickness": window border thickness
- "padding": window internal padding
- "toolwindow": to show or hide window maximize, minimze buttons and window icon
- "allow_minimize": allow window minimizing
- "allow_maximize": allow window maximizing
- "on_top": make window on top of all other windows
- "movable": make window movable or not
- "background_color": the window background color of the original tkinter window, my be useful during loading window view
- "transparency": set window transparency from 0 to 1
- "transparentcolor": set the transparency color
- "allow_text_selection": allow the user to select the text of the window content
- "flexible_drag": make easy drag of the window, this is helpful in the borderless window
  
```python
import photongui

settings = {
    "title" : "First window",
    "position" : (500, 500) # if not specified, the window will be centered by default
}


window = photongui.createWindow(window_settings=settings)

photongui.start()
```