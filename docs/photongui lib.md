# Lib

* photongui
    * [createWindow()](#createwindow)
        * [window](#window)
        * [fileDialog](#filedialog)
        * [setWindowAsModal()](#setwindowasmodal)
        * [messagebox()](#messagebox)
        * [loadView()](#loadview)
        * [loadSnippet()](#loadsnippet)
        * [loadCssFile()](#loadcssfile)
        * [execJsAsync()](#execjsasync)
        * [execJsSync()](#execjssync)
        * [execJsFunctionAsync()](#execjsfunctionasync)
        * [getUrl()](#geturl)
        * [getZoomLevel()](#getzoomlevel)
        * [setZoomLevel()](#setzoomlevel)
        * [canGoForward()](#cangoforward)
        * [goForward()](#goforward)
        * [canGoBack()](#cangoback)
        * [goBack()](#goback)
        * [find()](#find)
        * [stopFinding()](#stopfinding)
        * [downloadFromURL()](#downloadfromurl)
        * [reload()](#reload)
        * [reloadIgnoreCache()](#reloadinogrecache)
        * [isDocumentReady()](#isdocumentready)
        * [stopLoad()](#stopload)
        * [print()](#print)
        * [sendKeyEvent()](#sendkeyevent)
        * [sendMouseMoveEvent()](#sendmousemoveevent)
        * [sendMouseClickEvent()](#sendmouseclickevent)
        * [sendMouseWheelEvent()](#sendmousewheelevent)
        * 
    * [Util](#Util)
        * [exposeAll()](#exposeall)
    * [getAllWindows()](#getallwindows)
    * [start()](#start)


## createWindow

|Parameter|Type|Default value|
|---------|----|-------------|
|windowSettings|dict|see [windowSettings table](#windowsettings)|
|parent|obj|`None`|
|modal|bool|`False`|
|confirmClose|bool|`False`|

#### **windowSettings**

|Name|Description|Default value|OS support|Notes|
|----|-----------|-------------|----------|-----|
|title|window title. To make window without title set the value `""`|PhotonGUI|All|
|view|The content of the window. It may be `local html file` OR `url` OR `raw html in text format`. If you are going to use `raw html` you have to include `<html>` tag.|```<html><h1 class='window-drag-area'>Welcome To PhotonGUI</h1></html>```|All|
|icon|window icon. The icon should be one of the following formats `png`, `pgm`, `ppm`, `gif`|`.\gui\images\icon.png`|All|
|width|window width|`600`|All|
|height|window height|`600`|All|
|position|Initial window position on the screen. If left without value it will be centered automatically|`None`|All|
|resizable|Allow window to be resizable or not in both `X` and `Y`|`(True, True)`|All|
|disabled|To disable the window|`False`|All|
|fullscreen|Initialize the window in fullscreen mode|`False`|All|
|minimized|Initialize the window in minimized mode|`False`|All|
|maximized|Initialize the window in maximized mode|`False`|All|
|minSize|Minimum window size|`None`|All|
|maxSize|Maximum window size|`None`|All|
|hidden|Initialize window in hidden mode|`False`|All|
|borderless|To remove window borders and the title bar|`False`|All|
|borderColor|Window border color. This option will not work unless the `borderless` option is activated and the `borderThickness` has value|`None`|All|
|borderThickness|Window border thickness|`None`|All|
|padding|Window internal padding in both `X` and `Y`|`(0, 0)`|All|
|toolwindow|To show or hide window `maximize`, `minimize` buttons and `window icon`|`True`|All|
|minimizable|To allow minimizing the window or not|`True`|Windows|Implementation in other OSs|
|maximizable|To allow maximizing the window or not|`True`|All|
|onTop|Make the window on top of all other windows|`False`|All|
|backgroundColor|Initial window background color before loading the browser|`#FFFFFF`|All|
|transparency|Window transparency. From 0 to 1|`1`|All
|transparentColor|Window color when the window is transparent|`None`|All| 
|contentSelection|To allow the user to `select the text` OR `drag links` OR `drag images`|`False`|All|
|flexibleDrag|To set a specific part for the window drag. This may be helpful when the `borderless` option is activated. You have to set class name of the element to be `window-drag-area`. [Example](flexible_drag.md)|`False`|All|
|closable|To enable or disable the window close button|`True`|All|
|showOnReady|To make the window appear when the browser is ready|`True`|All|

#### Example
```python
import photongui

settings = {
    "title" : "Main window",
    "position" : (500, 500)
}

MainWindow = photongui.createWindow(windowSettings=settings)
ChildWindow = photongui.createWindow(parent=MainWindow, modal=True, confirmClose=True)

photongui.start()
```

### window
Gives you the full access to `tkinter window` methods and attributes.

#### Example
```python
import photongui
import time

settings = {
    "title" : "Main window",
    "position" : (500, 500)
}

MainWindow = photongui.createWindow(windowSettings=settings)

def changeWindowGeometry():
    time.sleep(3)
    MainWindow.window.geometry('100x100+0+0')

photongui.start(changeWindowGeometry)
```

Some extra methods have been added to `window`:
* centerWindow()

* SetIcon()
   |Parameter|Type|
   |----|---------|
   |iconPath|str|

* toggleFullscreen()

* minimizeMaximize()
   |Parameter|Type|OS|
   |----|---------|--|
   |minimizable|bool|`Windows`|
   |maximizable|bool|`All`|

#### Example
```python
import photongui
import time

settings = {
    "title" : "Main window",
    "position" : (0, 0)
}

MainWindow = photongui.createWindow(windowSettings=settings)

def changeWindow():
    time.sleep(3)
    MainWindow.window.centerWindow()

    time.sleep(3)
    MainWindow.window.toggleFullscreen()

    time.sleep(3)
    MainWindow.window.toggleFullscreen()
    
    time.sleep(3)
    MainWindow.window.minimizeMaximize(minimizable=False)
    
    time.sleep(3)
    MainWindow.window.minimizeMaximize(minimizable=True, maximizable=False)

    time.sleep(3)
    MainWindow.window.minimizeMaximize(minimizable=False, maximizable=False)

photongui.start(changeWindow)
```

### fileDialog
#### Methods
* askopenfile
* askopenfiles
* asksaveasfile
* askopenfilename
* askopenfilenames
* asksaveasfilename
* askdirectory
* open

#### Example
```python
import photongui
import time

settings = {
    "title" : "Main window",
    "position" : (500, 500)
}

MainWindow = photongui.createWindow(windowSettings=settings)

def openFileDialog():
    time.sleep(3)
    filePath = MainWindow.fileDialog.askopenfilename()
    print(filePath)

photongui.start(openFileDialog)
```

### setWindowAsModal
|Parameter|Type|
|--------|----|
|parent|obj|

#### Example
```python
import photongui
import time

settings = {
    "title" : "Main window",
    "position" : (500, 500)
}

MainWindow = photongui.createWindow(windowSettings=settings)

def setModal():
    time.sleep(2)
    ChildWindow = photongui.createWindow()
    
    time.sleep(3)
    ChildWindow.setWindowAsModal(parent=MainWindow)

photongui.start(setModal)
```

### messagebox
|Parameter|Type|
|--------|----|
|action|str|
|title|str|
|message|str|

* **action** may be one of the following values:
    * `warning`
    * `error`
    * `inofo`
    * `question`
    * `okcancel`
    * `yesnocancel`
    * `yesno`

#### Example
```python
import photongui
import time

settings = {
    "title" : "Main window",
    "position" : (500, 500)
}

MainWindow = photongui.createWindow(windowSettings=settings)

def showMessagebox():
    time.sleep(3)
    MainWindow.messagebox('warning', 'Warning message box', 'Something is going to explode, your mind')

photongui.start(showMessagebox)
```
### loadView
|Parameter|Type|
|--------|----|
|view|str|

To change the current window content

* **view** could be:
    * `html file path`
    * `raw html text`, must include `<html>` tag
    * `URL`, should start with `http://` or `https://`
    
#### Example
```python
import photongui
import time

settings = {
    "title" : "Main window",
    "position" : (500, 500)
}

html = """
  <html>
    <head></head>
    <body>
      <h2>From raw html text</h2>
    </body>
  </html>
"""

url = "https://www.github.com/mohamed501258/photongui"

MainWindow = photongui.createWindow(windowSettings=settings)

def changeView():
    time.sleep(3)
    MainWindow.loadView(html)

    time.sleep(3)
    MainWindow.loadView(url)

photongui.start(changeView)
```
### loadSnippet
|Parameter|Type|
|--------|----|
|elementSelector|str|
|snippet|str|
|position|str|

To inject `html` code into the current view

* **elementSelector** examples:
    * `.class-name`
    * `#id-name`
    * `h1`
* **position** could be one of the following:
    * `beforebegin` Before the element itself
    * `afterbegin` Just inside the element, before its first child
    * `beforeend` Just inside the element, after its last child
    * `afterend` After the element itself

#### Example
```python
import photongui
import time

html = """
  <html>
    <head></head>
    <body>
      <h2>This is h2</h2>
    </body>
  </html>
"""

settings = {
    "view" : html,
    "title" : "Main window",
    "position" : (500, 500)
}

snippet = '<p>This is a text injected here</p>'

MainWindow = photongui.createWindow(windowSettings=settings)

def loadHtml():
    time.sleep(3)
    MainWindow.loadSnippet('h2', snippet, 'beforebegin')

    time.sleep(3)
    MainWindow.loadSnippet('h2', snippet, 'afterend')

photongui.start(loadHtml)
```
### loadCssFile
|Parameter|Type|
|--------|----|
|filePath|str|

To add `css` file to the current view. The file will be added at the end of `head` tag automatically 

#### Example
```python
import photongui
import time

cssFilePath = "<css file path>"

settings = {
    "title" : "Main window",
    "position" : (500, 500)
}

MainWindow = photongui.createWindow(windowSettings=settings)

def loadCss():
    time.sleep(10)
    MainWindow.loadCssFile(filePath=cssFilePath)

photongui.start(loadCss)
```
### execJsAsync
|Parameter|Type|
|--------|----|
|js_code|str|

To execute `javascript` code asynchronously

#### Example
```python
import photongui
import time

settings = {
    "title" : "Main window",
    "position" : (500, 500)
}

MainWindow = photongui.createWindow(windowSettings=settings)

def execJs():
    time.sleep(3)
    MainWindow.execJsAsync("document.querySelector('h1').innerText = 'New content from js by python'")

photongui.start(execJs)
```
### execJsSync
|Parameter|Type|
|--------|----|
|js_code|str|

To execute `javascript` code synchronously 

#### Example
```python
import photongui
import time

settings = {
    "title" : "Main window",
    "position" : (500, 500)
}

MainWindow = photongui.createWindow(windowSettings=settings)

def execJs():
    time.sleep(3)
    body = MainWindow.execJsSync("document.body.innerHTML")
    print(body)

photongui.start(execJs)
```
### execJsFunctionAsync
|Parameter|Type|
|--------|----|
|function_name|str|
|function_parameters|list|

To execute `javascript function` asynchronously 

#### Example
```python
import photongui
import time

html = """
  <html>
    <head></head>
    <body>
      <h2>This is h2</h2>

      <script>
        function showMyName(name){
            document.querySelector('h2').innerText = `Your name is: ${name}`
        }
      </script>
    </body>
  </html>
"""

settings = {
    "view" : html,
    "title" : "Main window",
    "position" : (500, 500)
}

name = 'PhotonGUI'

MainWindow = photongui.createWindow(windowSettings=settings)

def execJsFunction():
    time.sleep(3)
    MainWindow.execJsFunctionAsync(function_name="showMyName", function_parameters=[name])

photongui.start(execJsFunction)
```

### getUrl

Returns the `URL` of the current view

#### Example
```python
import photongui
import time

url = 'https://www.google.com'

settings = {
    "view" : url,
    "title" : "Main window",
    "position" : (500, 500)
}

name = 'PhotonGUI'

MainWindow = photongui.createWindow(windowSettings=settings)

def showUrl():
    time.sleep(3)
    currentUrl = MainWindow.getUrl()
    print(currentUrl)

photongui.start(showUrl)
```

### getZoomLevel

Returns the current `zoom level` of the browser

#### Example
```python
import photongui
import time

html = """
  <html>
    <head></head>
    <body>
      <h2>This is h2</h2>
    </body>
  </html>
"""

settings = {
    "view" : html,
    "title" : "Main window",
    "position" : (500, 500)
}

MainWindow = photongui.createWindow(windowSettings=settings)

def showZoomLevel():
    time.sleep(3)
    zoomLevel = MainWindow.getZoomLevel()
    print(zoomLevel)

photongui.start(showZoomLevel)
```

### setZoomLevel
|Parameter|Type|
|--------|----|
|zoom_level|float|

To set a new `zoom level` of the browser

#### Example
```python
import photongui
import time

html = """
  <html>
    <head></head>
    <body>
      <h2>This is h2</h2>
    </body>
  </html>
"""

settings = {
    "view" : html,
    "title" : "Main window",
    "position" : (500, 500)
}

MainWindow = photongui.createWindow(windowSettings=settings)

levels = [0.2, 0.6, 1]
def changeZoomLevel():
    for level in levels:
        MainWindow.setZoomLevel(zoom_level=level)
        time.sleep(3)
    MainWindow.setZoomLevel(zoom_level=0)

photongui.start(changeZoomLevel)
```

### canGoForward
Returns `True` if the browser can navigate forwards

### goForward
Navigate forwards

### canGoBack
Returns `True` if the browser can navigate backwards

### goBack
Navigate backwards

### find
|Parameter|Type|Default value|Description|
|---------|----|-------------|-----------|
|searchId|int|`0`|Must be unique Id. Other wise leave it and it will be automatically generated|
|searchText|str|`""`|Text you want to find|
|forward|bool|`False`|Whether to search forward or backward|
|matchCase|bool|`False`|Whether the search is case-sensitive|
|findNext|bool|`False`|Whether this is the first request or a follow-up|

Search for text and highlight it. check this [link](https://github.com/cztomczak/cefpython/blob/master/api/Browser.md#find) for more details

#### Example
```python
import photongui

settings = {
    "title" : "Main window",
    "position" : (500, 500)
}

MainWindow = photongui.createWindow(windowSettings=settings)

def search():
    MainWindow.findInBrowser(searchId=1, searchText="h")

photongui.start(search)
```

### stopFinding
Stop searching for the text. It stops the `findInBrowseer` method.

### downloadFromURL
|Parameter|Type|
|---------|----|
|url|str|


### reload
To reload the window without ignoring the cached data

### reloadInogreCache
To reload the window ignoring any cached data

### isDocumentReady
Returns `True` when the **DOM** is ready

### stopLoad
Stop window loading

### print
print the window

### sendKeyEvent
|Parameter|Type|
|---------|----|
|event|keyEvent|


### sendMouseMoveEvent
|Parameter|Type|
|---------|----|
|x|int|
|y|int|
|mouseLeave|bool|
|modifiers|int|

**modifiers** flags are the same of [[sendMouseClickEvent](#sendmouseclickevent)]


### sendMouseClickEvent
|Parameter|Type|Options|
|---------|----|-------|
|x|int| |
|y|int| |
|mouseButtonType|int|`MOUSEBUTTON_LEFT`  - `MOUSEBUTTON_MIDDLE` - `MOUSEBUTTON_RIGHT`|
|mouseUp|bool| |
|clickCount|int| |
|modifiers|int|`EVENTFLAG_NONE` - `EVENTFLAG_CAPS_LOCK_ON` - `EVENTFLAG_SHIFT_DOWN` - `EVENTFLAG_CONTROL_DOWN` - `EVENTFLAG_ALT_DOWN` - `EVENTFLAG_LEFT_MOUSE_BUTTON` - `EVENTFLAG_MIDDLE_MOUSE_BUTTON` - `EVENTFLAG_RIGHT_MOUSE_BUTTON` - `EVENTFLAG_COMMAND_DOWN` (Mac) - `EVENTFLAG_NUM_LOCK_ON` (Mac) - `EVENTFLAG_IS_KEY_PAD` (Mac) - `EVENTFLAG_IS_LEFT` (Mac) - `EVENTFLAG_IS_RIGHT` (Mac)|

### sendMouseWheelEvent
|Parameter|Type|Options|
|---------|----|-------|
|x|int| |
|y|int| |
|deltaX|int| |
|deltaY|int| |
|modifiers|int|`EVENTFLAG_NONE` - `EVENTFLAG_CAPS_LOCK_ON` - `EVENTFLAG_SHIFT_DOWN` - `EVENTFLAG_CONTROL_DOWN` - `EVENTFLAG_ALT_DOWN` - `EVENTFLAG_LEFT_MOUSE_BUTTON` - `EVENTFLAG_MIDDLE_MOUSE_BUTTON` - `EVENTFLAG_RIGHT_MOUSE_BUTTON` - `EVENTFLAG_COMMAND_DOWN` (Mac) - `EVENTFLAG_NUM_LOCK_ON` (Mac) - `EVENTFLAG_IS_KEY_PAD` (Mac) - `EVENTFLAG_IS_LEFT` (Mac) - `EVENTFLAG_IS_RIGHT` (Mac)|



## Util

### exposeAll
|Parameter|Type|Notes|
|---------|----|-----|
|name|str||
|environ|dict|set to **`locals()`**|

To access the `python env` from `javascript` you have to expose it first.

To execute `python code` from `javascript` use `window.execPy(envName, pyCode)`

**window.execPy()**

|Parameter|Type|
|---------|----|
|envName|obj|
|pyCode|str|

#### Example
```python
import photongui
from photongui import Util

# Exposing this environment to js
util = Util()
# Note: we set the name of this environ to 'math' that we will use later in js
util.exposeAll("math", locals())

# We will run this function from js and get the return value
def calculate(x, y):
    return x + y

# window view
html = """
<html>
    <input type="number" class='x'></input>
    <span>+</span>
    <input type="number" class='y'></input>

    <h3 class='result'>This will be replaced with the result from python</h3>
    <button class="show-result" onclick="calculate()">Calculate</button>

    <script>
        var result = document.querySelector('.result')

        function calculate(){
            var x = parseInt(document.querySelector('.x').value)
            var y = parseInt(document.querySelector('.y').value)
            
            // we can access the python environ 'math' using `window.math`
            window.execPy(window.math, `calculate(${x}, ${y})`)
            .then(function(r){
                    result.innerText = "= " + r
                }
            )
        }
    </script>
</html>
"""
settings = {
    "view":html
}

window = photongui.createWindow(windowSettings=settings)

photongui.start()
```

## getAllWindows
Returns a `dict` of all created and active windows. Access the window by its ID

## start 
|Parameter|Type|Default value|
|---------|----|-------------|
|function|function| |
|args|list|`[]`|
|debug|bool|`False`|
|logLevel|str|`INFO`|
|userAgent|str|`''`|
|locale|str|`en-US`|
|stringEncoding|str|`utf-8`|
|proxy|str|`None`|
