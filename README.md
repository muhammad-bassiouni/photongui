# PhotonGUI
**photongui** is a cross-platform tool that allows you to create Python programs with HTML, CSS, JS. You can use the web technologies in your desktop application. 

**photongui** uses tkinter, so you have all its functionnaliy and power. **photongui** is available only for Python 3.

**photongui** is created by *Muhammed Bassiouni*.

## Getting started

### Install
```bash
pip install photongui
```
### Example
```python
import photongui

window_settings = {
    "title" : "PhotonGUI",
    "view" : "https://github.com/Mohamed501258/photongui"
}

photongui.createWindow(window_settings)

photongui.start()
```
## More details
### Window settings
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

you can make dictionary and set your settings like in the previous example

### Run function right after the app launches

you can set function to run immediately after the app launches by passing the function name to **start** in **photongui.start()**

#### Example
```python
import photongui 

window = photongui.createWindow()

def main():
	body_content = window.execJsSync("document.body.innerText")
    print(body_content)
    
photongui.start(function=main, debug=True)
```
you can pass arguments to the function using **parameters** in **photongui.start()**, You have to put your arguments inside list

#### Example
```python
import photongui 

window = photongui.createWindow()

def main(text):
    body_content = window.execJsSync("document.body.innerText")
    print(body_content)
    
photongui.start(function=main, parameters=["This is text"], debug=True)
```

## Access tkinter features of the window

to access all tkinter features of the window use **window** attribute

### Example
```python
import photongui 

window1 = photongui.createWindow()

def main():
    window1.window.title("This is new title")
    
photongui.start(function=main, debug=True)
```