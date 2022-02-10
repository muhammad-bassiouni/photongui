"""
BSD 3-Clause License

Copyright (c) 2021, Muhammed Bassiouni
All rights reserved.
"""


import ctypes 
import tkinter as tk
import tkinter.messagebox as tkmessagebox
import os
import sys
import platform
import re
import string
import random
from cefpython3 import cefpython as cef
from threading import Event

from photongui import threaded
from photongui.browser import BrowserFrame, bindings
from photongui.util import logger
from photongui.data import defaultIcon
from photongui.api.utils import loadSnippet, loadCssFile



# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Global Variables
execJsOperations = {}
allWindows = {} # access the window by its ID
envsName = []

# Global stuff #
# WindowsOS styles:
GWL_EXSTYLE = -20
GWL_STYLE = -16
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080

WS_MINIMIZEBOX = 131072
WS_MAXIMIZEBOX = 65536

SWP_NOZORDER = 4
SWP_NOMOVE = 2
SWP_NOSIZE = 1
SWP_FRAMECHANGED = 32

set_window_pos = ctypes.windll.user32.SetWindowPos
set_window_long = ctypes.windll.user32.SetWindowLongPtrW
get_window_long = ctypes.windll.user32.GetWindowLongPtrW
get_parent = ctypes.windll.user32.GetParent

# Path:
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)



# App info #
#TODO 

# Window general settings #
WINDOW_SETTINGS = {
    "title": "PhotonGUI",
    "view": "<html><body><h1 class='window-drag-area'>Welcome To PhotonGUI</h1></body></html>",
    "icon": os.path.join(application_path, r"gui\images\icon.png"),
    "width":600,
    "height":600,
    "position":None,
    "resizable":(True, True),
    "disabled":False,
    "fullscreen":False,
    "minimized":False,
    "maximized":False,
    "minSize":None,
    "maxSize":None,
    "hidden":False,
    "borderless":False,
    "borderColor":None,
    "borderThickness":None,
    "padding":(0,0),
    "toolwindow":True,
    "minimizable":True,
    "maximizable":True,
    "onTop":False,
    "backgroundColor":"#FFFFFF",
    "transparency":1,
    "transparentColor":None,
    "contentSelection":False,
    "flexibleDrag":False,
    "closable":True,
    "showOnReady":True
}


# This function to recieve the return from js to handle and store it in python
def _pyCallbackOfExecJs(jsReturn): 
    execJsOperations[jsReturn[0]].set()
    execJsOperations[jsReturn[0]] = jsReturn[1] # finalReturn = [operationID, operationResult]
    
def _pyCallbackOfDrag(windowId, x, y): 
    allWindows[windowId].window.geometry(f"+{x}+{y}") # finalReturn = [windowID, [x, y]]


def _customAlert(message, windowid):
    tkmessagebox.showinfo(title=allWindows[windowid].title, message=message, parent=allWindows[windowid])

# This class gives some utilites, like exposing python environment to all browsers
class Util: 
    name = None
    eviron = None
    class exposeAll:
        def __init__(self, name, environ=None):
            self.name = name
            self.environ = environ
            envsName.append(name)
            bindings.SetObject(name, self)
            
        @threaded
        def _execPy(self, windowid, operationid, pyCode):
            try:
                return_value = eval(pyCode, self.environ)
                status = 200
            except Exception as e:
                return_value = str(e)
                status = 500
            allWindows[windowid].execJsFunctionAsync("_jsCallbackOfExecPy", [status, operationid, return_value])


bindings.SetFunction("customAlert", _customAlert)
bindings.SetFunction("_pyCallbackOfExecJs", _pyCallbackOfExecJs)
bindings.SetFunction("_pyCallbackOfDrag", _pyCallbackOfDrag)



class Frame(tk.Frame, tk.Toplevel):
    windowCount = 0
    def __init__(self, window_settings=None, parent=None, modal=None, confirm_close=None):
        Frame.windowCount+=1
        self.window = tk.Toplevel() 
        self.__settings = WINDOW_SETTINGS if not window_settings else window_settings
        self.__parent = parent if parent else None
        self.__modal = modal
        self.__confirm_close = confirm_close


        self.__browser_frame = None
        self.__centerTheWindowByDefault = True

        self._windowAndBrowserExist = False
        self._loadingTimesThreshold = 0

        self.__windowFrame_attributes_generator() # This generates attributes of this class from "WINDOW_SETTINGS" dynamically

        self.__view = self.__handle_view(self.view)

        tk.Frame.__init__(self, self.window, highlightbackground=self.borderColor, highlightthickness=self.borderThickness, padx=self.padding[0], pady=self.padding[1])
        self._windowid = self.master.winfo_id()
        self.master.protocol("WM_DELETE_WINDOW", self.__on_close)
        self.master.bind("<Destroy>", self.__on_destroy)
        self.master.bind("<Configure>", self.__on_window_configure)
        self.master.bind("<Escape>", self.__on_escape)
        
        # parent window -> child frame
        self.bind("<Configure>", self.__on_configure)
        self.bind("<FocusIn>", self.__on_focus_in)
        self.bind("<FocusOut>", self.__on_focus_out)

        # New methods to the defualt tkinter window methods
        self.master.center = self.__centerWindow
        self.master.setIcon = self.__setIcon
        self.master.toggleFullscreen = self.__toggleFullscreen
        self.master.minimizeMaximize = self.__handle_minimize_maximize

        self.__set_default_window_settings() # after generating the required attributes to initiate the window, now we structure the window based on them


        ## BrowserFrame
        self.__browser_frame = BrowserFrame(self, self.__view)
        self.__browser_frame.grid(row=0, column=0,
                                sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        self.pack(fill=tk.BOTH, expand=tk.YES)

    ## private methods
    def __windowFrame_attributes_generator(self):
        for key, value in WINDOW_SETTINGS.items():
            setattr(self, key, self.__settings.get(key, value))

    def __set_default_window_settings(self):
        self.master.title(self.title)
        self.master.after(20, self.__setIcon, self.icon)
        self.master.attributes('-fullscreen', self.fullscreen, '-topmost',self.onTop, '-alpha',self.transparency, '-disabled',self.disabled)
        self.master.configure(bg=self.backgroundColor)
        self.master.resizable(self.resizable[0], self.resizable[1])
        
        if self.showOnReady:
            self.master.withdraw()
        if self.__modal:
            if self.__parent:
                self.setAsModal(self.__parent)
            else:
                logger.warn("The modal window mode will not work unless you set the parent window!")
        if self.transparentColor:
            self.master.attributes('-transparentcolor',self.transparentColor)
        if self.maximized:
            self.master.state('zoomed')
        if self.minimized:
            self.master.iconify()
        if self.minSize:
            self.master.minsize(self.minSize[0], self.minSize[1])
        if self.maxSize:
            self.master.maxsize(self.maxSize[0], self.maxSize[1])
        if self.hidden:
            self.master.withdraw()
        if not self.toolwindow:
            self.master.attributes('-toolwindow', True)
        if self.position:
            self.__centerTheWindowByDefault = False
            self.master.geometry(f"{self.width}x{self.height}+{self.position[0]}+{self.position[1]}")
        if not self.position:
            self.__centerWindow()
        if self.borderless:
            self.master.overrideredirect(self.borderless)
            if WINDOWS:
                self.master.after(100, self.__set_taskbar_icon_for_borderless_window)

        self.master.after(100, lambda: self.__handle_minimize_maximize(maximizable=self.maximizable, minimizable=self.minimizable))

        self.__add_windowId_to_dict()

    def __setIcon(self, iconPath):
        icon_path = iconPath
        if os.path.exists(icon_path) and (icon_path.endswith(".png") or icon_path.endswith(".pgm") or icon_path.endswith(".ppm") or icon_path.endswith(".gif")):
            try:
                icon = tk.PhotoImage(file=icon_path)
                self.master.tk.call('wm', 'iconphoto', self.master._w, icon)
            except:
                logger.warn("The icon couldn't be set due to unknown problem. Try to use another one and make sure you put the correct path and the image is of type '.png'")
        else:
            logger.info("If you are trying to set icon and it doesn't show, Check the icon-path and icon-extenstion to be '.png or .pgm or .ppm or .gif'")
            icon = tk.PhotoImage(data=defaultIcon)
            self.master.tk.call('wm', 'iconphoto', self.master._w, icon)  

    def __set_taskbar_icon_for_borderless_window(self):
        hwnd = get_parent(self.master.winfo_id())
        stylew = get_window_long(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        set_window_long(hwnd, GWL_EXSTYLE, stylew)
        self.master.wm_withdraw()
        self.master.wm_deiconify()

    def __handle_minimize_maximize(self, minimizable=True, maximizable=True):
        if WINDOWS:
            hwnd = get_parent(self.master.winfo_id())
            new_style = old_style = get_window_long(hwnd, GWL_STYLE)
            if not minimizable:
                new_style = old_style & ~ WS_MINIMIZEBOX
            if not maximizable:
                new_style = old_style & ~ WS_MAXIMIZEBOX
            if not maximizable and not minimizable:
                new_style = old_style & ~ WS_MINIMIZEBOX & ~ WS_MAXIMIZEBOX
            set_window_long(hwnd, GWL_STYLE, new_style)
            set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
        
        if not WINDOWS:
            if not minimizable:
                logger.warning("disabling 'minimizable' is only available for windows!")
            if not maximizable:
                self.master.resizable(False, False)
            if not maximizable and not minimizable:
                logger.warning("disabling 'minimizable' and 'maximizable' is only available for windows!")
    
    def __centerWindow(self):
        if self.__centerTheWindowByDefault:
            windowWidth, windowHeight = self.width, self.height
        else:
            windowWidth, windowHeight = map(int, self.master.geometry().split("+")[0].split("x")[0:2])
        position_x = int(self.master.winfo_screenwidth()/2 - windowWidth/2)
        position_y = int(self.master.winfo_screenheight()/2 - windowHeight/2)
        center = (position_x, position_y)
        self.master.geometry(f"{self.width}x{self.height}+{center[0]}+{center[1]}")

    def __fixWindowPosition(self, event): # This method doesn't work correctly
        X = self.master.winfo_geometry().split("+")[1]
        Y = self.master.winfo_geometry().split("+")[2]
        self.master.geometry("+{}+{}".format(X,Y))

    def __handle_view(self, view):
        view = view.strip()
        if ("<html>") in view:
            view = f'data:text/html,{view}'
        elif re.match("^https*://", view):
            pass
        else:
            view = "file:///" + view
        return view  

    def __toggleFullscreen(self):
        if self.master.attributes('-fullscreen'):
            self.master.attributes('-fullscreen', False)
        else:
            self.master.attributes('-fullscreen', True)
    
    def __add_windowId_to_dict(self):
        allWindows[self.master.winfo_id()] = self

    def _check_window_and_dom(func):
        def wrapper(self, *arg, **kw):
            try:
                if self.master.winfo_exists():
                    self.__browser_frame.isDocumentReady.wait()
                    try:
                        return func(self, *arg, **kw)
                    except Exception as e:
                        logger.error(f"Error during executing the function! >> {e}")
                        return None
                logger.error("The window doesn't exist!")
                return False
            except:
                logger.error("Can't check window or browser")
                return False
        return wrapper
            
    ## public methods    
    def setAsModal(self, parent):
        try:
            parent.attributes('-disabled', True)
            self.__parent = parent
        except:
            parent = parent.window # In case this method is called from outside 
            self.__parent = parent
            parent.attributes('-disabled', True)
        self.master.wm_transient(parent)

    @_check_window_and_dom
    def loadView(self, view):
        view = self.__handle_view(view)
        self.__browser_frame.isDocumentReady = Event()
        self.__browser_frame.browser.LoadUrl(view)

    @_check_window_and_dom
    def loadSnippet(self, elementSelector, snippet, position):
        inject = loadSnippet.src % {"elementSelector":elementSelector, "snippet":snippet, "position":position}
        self.__browser_frame.browser.ExecuteJavascript(inject)
    
    @_check_window_and_dom
    def loadCssFile(self, filePath):
        inject = loadCssFile.src(filePath)
        self.__browser_frame.browser.ExecuteJavascript(inject)

    @_check_window_and_dom
    def execJsAsync(self, js_code): # execute js code asynchronously 
        self.__browser_frame.browser.ExecuteJavascript(js_code)

    @_check_window_and_dom
    def execJsSync(self, js_code): # execute js code synchronously
        operation_id = self.__create_random_id()
        execJsOperations[operation_id] = Event()   
        self.__browser_frame.browser.ExecuteFunction("execJs", [operation_id, js_code])
        execJsOperations[operation_id].wait()
        return_value = execJsOperations[operation_id]
        del execJsOperations[operation_id] # free memory
        return return_value

    @_check_window_and_dom
    def execJsFunctionAsync(self, function_name, function_parameters=[]):
        self.__browser_frame.browser.ExecuteFunction(function_name, function_parameters)

    @_check_window_and_dom
    def getUrl(self):
        return self.__browser_frame.browser.GetUrl() 
    
    @_check_window_and_dom
    def getZoomLevel(self):
        return self.__browser_frame.browser.GetZoomLevel()
    
    @_check_window_and_dom
    def setZoomLevel(self, zoom_level=0):
        self.__browser_frame.browser.SetZoomLevel(zoom_level)

    @_check_window_and_dom
    def canGoForward(self):
        return self.__browser_frame.browser.CanGoForward()

    @_check_window_and_dom
    def goForward(self):
        self.__browser_frame.browser.GoForward()
    
    @_check_window_and_dom
    def canGoBack(self):        
        return self.__browser_frame.browser.CanGoBack()

    @_check_window_and_dom
    def goBack(self):      
        self.__browser_frame.browser.GoBack()
    
    @_check_window_and_dom
    def find(self, searchId=0, searchText="", forward=False, matchCase=False, findNext=False):       
        self.__browser_frame.browser.Find(searchId, searchText, forward, matchCase, findNext)
    
    @_check_window_and_dom
    def stopFinding(self, clearSelection=False):     
        self.__browser_frame.browser.StopFinding(clearSelection)
    
    @_check_window_and_dom
    def downloadFromURL(self, url=None):      
        self.__browser_frame.browser.StartDownload(url)
        
    @_check_window_and_dom
    def reload(self): 
        self.__browser_frame.browser.Reload()
    
    @_check_window_and_dom
    def reloadInogreCache(self): 
        self.__browser_frame.browser.ReloadIgnoreCache()

    def isDocumentReady(self):     
        return self.__browser_frame.isDocumentReady
    
    @_check_window_and_dom
    def stopLoad(self):      
        return self.__browser_frame.browser.StopLoad()

    @_check_window_and_dom
    def print(self):       
        return self.__browser_frame.browser.Print()
    
    @_check_window_and_dom
    def sendKeyEvent(self, event=None):      
        self.__browser_frame.browser.SendKeyEvent(event)

    @_check_window_and_dom
    def sendMouseMoveEvent(self,x=0, y=0, mouseLeave=False, modifiers=None):       
        self.__browser_frame.browser.SendMouseMoveEvent(x, y, mouseLeave, modifiers)

    @_check_window_and_dom
    def sendMouseClickEvent(self, x=0, y=0, mouseButtonType=1, mouseUp=True, clickCount=1, modifiers=1):       
        self.__browser_frame.browser.SendMouseClickEvent(x, y, mouseButtonType, mouseUp, clickCount, modifiers)
    
    @_check_window_and_dom
    def sendMouseWheelEvent(self, x=0, y=0, deltaX=0, deltaY=0, modifiers=1):         
        self.__browser_frame.browser.SendMouseWheelEvent(x, y, deltaX, deltaY, modifiers)

    ## static methods
    @staticmethod
    def __create_random_id():
        characters = string.ascii_letters + string.digits
        id = ''.join(random.choice(characters) for i in range(8))
        return id

    # Window sensors to handle the browser frame 
    def __on_window_configure(self, _):
        if self.__browser_frame:
            self.__browser_frame.on_window_configure()

    def __on_configure(self, event):
        if self.__browser_frame:
            self.__browser_frame.on_mainframe_configure(event.width, event.height)

    def __on_focus_in(self, _):
        logger.debug(f"MainFrame: {self}.on_focus_in")

    def __on_focus_out(self, _):
        self.master.master.focus_force() # <- added

    def __on_destroy(self, event):
        if event.widget == self.master:
            Frame.windowCount-=1
            del allWindows[self._windowid]
            if Frame.windowCount == 0:
                from photongui import root
                root.destroy()

    def __on_close(self):
        if not self.closable:
            return
        if self.__confirm_close:
            if tkmessagebox.askyesno(title="Close window", message="Are you sure that you want to exit?", parent=self.window):
                pass
            else:
                return
        if self.__parent: # in case the window in modal mode
            self.__parent.attributes('-disabled', False)
            self.window.grab_release()
        if self.__browser_frame:
            self.__browser_frame.on_root_close()
            self.__browser_frame = None 
        self.master.destroy()
        
    def __on_escape(self, event):
        if self.window.attributes("-fullscreen"):
            #self.window.focus_set()
            self.window.attributes("-fullscreen", False)






  