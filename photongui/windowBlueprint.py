"""
BSD 3-Clause License

Copyright (c) 2021, Muhammed Bassiouni
All rights reserved.
"""


import ctypes 
import tkinter as tk
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmessagebox
import os
import sys
import platform
import re
import string
import random
import time
import webbrowser
from cefpython3 import cefpython as cef

from photongui import threaded
from photongui.util import logger
from photongui.data import defaultIcon
from photongui.api import js, css
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

# Global browser config #
bindings = cef.JavascriptBindings(bindToFrames=True, bindToPopups=True)

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

BROWSER_SETTINGS = {
    "web_security_disabled": False,
    "file_access_from_file_urls_allowed": True,
    "universal_access_from_file_urls_allowed": True,
    "javascript_close_windows_disallowed":True,
    "dom_paste_disabled":False,
    "javascript_access_clipboard_disallowed":False,
    "tab_to_links_disabled":False,
    "webgl_disabled":False
}

# This function to recieve the return from js to handle and store it in python
def _pyCallBack(action, finalReturn): 
    if action == "execJs":
        execJsOperations[finalReturn[0]] = finalReturn[1] # finalReturn = [operationID, operationResult]
    if action == "dragWindow": 
        allWindows[finalReturn[0]].window.geometry(f"+{finalReturn[1][0]}+{finalReturn[1][1]}") # finalReturn = [windowID, [x, y]]
    if action == "msg":
        logger.info(finalReturn)

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
        def _evaluatePyCode(self,windowid, operationid, pyCode):
            try:
                return_value = eval(pyCode, self.environ)
                status = 200
            except Exception as e:
                return_value = str(e)
                status = 500
            allWindows[windowid].execJsFunctionAsync("execJs", ["return", status, operationid, return_value])


bindings.SetFunction("customAlert", _customAlert)
bindings.SetFunction("pyCallBack", _pyCallBack)


class windowFrame(tk.Frame):
    windowCount = 0
    def __init__(self, window, window_settings=None, parent=None, modal=None, confirm_close=None):
        windowFrame.windowCount+=1
        self.window = window 
        self.__settings = WINDOW_SETTINGS if not window_settings else window_settings
        self.__parent = parent if parent else None
        self.__modal = modal
        self.__confirm_close = confirm_close

        self._windowid = self.window.winfo_id()

        self.__browser_frame = None
        self.__centerTheWindowByDefault = True

        self._windowAndBrowserExist = False
        self._loadingTimesThreshold = 0

        self.__windowFrame_attributes_generator() # This generates attributes of this class from "WINDOW_SETTINGS" dynamically

        self.__view = self.__handle_view(self.view)

        # New methods to the defualt tkinter window methods
        self.window.centerWindow = self.__centerWindow
        self.window.setIcon = self.__setIcon
        self.window.toggleFullscreen = self.__toggleFullscreen
        self.window.minimizeMaximize = self.__handle_minimize_maximize

        self.fileDialog = _filedialog(self.window)

        self.__set_default_window_settings() # after generating the required attributes to initiate the window, now we structure the window based on them

        tk.Frame.__init__(self, self.window, highlightbackground=self.borderColor, highlightthickness=self.borderThickness, padx=self.padding[0], pady=self.padding[1])
        self.master.protocol("WM_DELETE_WINDOW", self.__on_close)
        self.master.bind("<Destroy>", self.__on_destroy)
        self.master.bind("<Configure>", self.__on_window_configure)
        self.master.bind("<Escape>", self.__on_escape)
        # parent window -> child frame
        self.bind("<Configure>", self.__on_configure)
        self.bind("<FocusIn>", self.__on_focus_in)
        self.bind("<FocusOut>", self.__on_focus_out)

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
        self.window.title(self.title)
        self.window.after(20, self.__setIcon, self.icon)
        self.window.attributes('-fullscreen', self.fullscreen, '-topmost',self.onTop, '-alpha',self.transparency, '-disabled',self.disabled)
        self.window.configure(bg=self.backgroundColor)
        self.window.resizable(self.resizable[0], self.resizable[1])
        
        if self.showOnReady:
            self.window.withdraw()
        if self.__modal:
            if self.__parent:
                self.setWindowAsModal(self.__parent)
            else:
                logger.warn("The modal window mode will not work unless you set the parent window!")
        if self.transparentColor:
            self.window.attributes('-transparentcolor',self.transparentColor)
        if self.maximized:
            self.window.state('zoomed')
        if self.minimized:
            self.window.iconify()
        if self.minSize:
            self.window.minsize(self.minSize[0], self.minSize[1])
        if self.maxSize:
            self.window.maxsize(self.maxSize[0], self.maxSize[1])
        if self.hidden:
            self.window.withdraw()
        if not self.toolwindow:
            self.window.attributes('-toolwindow', True)
        if self.position:
            self.__centerTheWindowByDefault = False
            self.window.geometry(f"{self.width}x{self.height}+{self.position[0]}+{self.position[1]}")
        if not self.position:
            self.__centerWindow()
        if self.borderless:
            self.window.overrideredirect(self.borderless)
            if WINDOWS:
                self.window.after(100, self.__set_taskbar_icon_for_borderless_window)

        self.window.after(100, lambda: self.__handle_minimize_maximize(maximizable=self.maximizable, minimizable=self.minimizable))

        self.__add_windowId_to_dict()

    def __setIcon(self, iconPath):
        icon_path = iconPath
        if os.path.exists(icon_path) and (icon_path.endswith(".png") or icon_path.endswith(".pgm") or icon_path.endswith(".ppm") or icon_path.endswith(".gif")):
            try:
                icon = tk.PhotoImage(file=icon_path)
                self.window.tk.call('wm', 'iconphoto', self.window._w, icon)
            except:
                logger.warn("The icon couldn't be set due to unknown problem. Try to use another one and make sure you put the correct path and the image is of type '.png'")
        else:
            logger.info("If you are trying to set icon and it doesn't show, Check the icon-path and icon-extenstion to be '.png or .pgm or .ppm or .gif'")
            icon = tk.PhotoImage(data=defaultIcon)
            self.window.tk.call('wm', 'iconphoto', self.window._w, icon)  

    def __set_taskbar_icon_for_borderless_window(self):
        hwnd = get_parent(self.window.winfo_id())
        stylew = get_window_long(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        set_window_long(hwnd, GWL_EXSTYLE, stylew)
        self.window.wm_withdraw()
        self.window.wm_deiconify()

    def __handle_minimize_maximize(self, minimizable=True, maximizable=True):
        if WINDOWS:
            hwnd = get_parent(self.window.winfo_id())
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
                self.window.resizable(False, False)
            if not maximizable and not minimizable:
                logger.warning("disabling 'minimizable' and 'maximizable' is only available for windows!")
    
    def __centerWindow(self):
        if self.__centerTheWindowByDefault:
            windowWidth, windowHeight = self.width, self.height
        else:
            windowWidth, windowHeight = map(int, self.window.geometry().split("+")[0].split("x")[0:2])
        position_x = int(self.window.winfo_screenwidth()/2 - windowWidth/2)
        position_y = int(self.window.winfo_screenheight()/2 - windowHeight/2)
        center = (position_x, position_y)
        self.window.geometry(f"{self.width}x{self.height}+{center[0]}+{center[1]}")

    def __fixWindowPosition(self, event): # This method doesn't work correctly
        X = self.window.winfo_geometry().split("+")[1]
        Y = self.window.winfo_geometry().split("+")[2]
        self.window.geometry("+{}+{}".format(X,Y))

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
        if self.window.attributes('-fullscreen'):
            self.window.attributes('-fullscreen', False)
        else:
            self.window.attributes('-fullscreen', True)
    
    def __add_windowId_to_dict(self):
        allWindows[self.window.winfo_id()] = self

    def _check_window_and_dom(func):
        def wrapper(self, *arg, **kw):
            try:
                if self.master.winfo_exists():
                    while not self.__browser_frame.isDocumentReady:
                        continue
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
    def setWindowAsModal(self, parent):
        try:
            parent.attributes('-disabled', True)
            self.__parent = parent
        except:
            parent = parent.window # In case this method is called from outside 
            self.__parent = parent
            parent.attributes('-disabled', True)
        self.window.wm_transient(parent)
    
    def messagebox(self, action, title=None, message=None):
        if action == "warning":
            return tkmessagebox.showwarning(title, message, parent=self.window)
        if action == "error":
            return tkmessagebox.showerror(title, message, parent=self.window)
        if action == "info":
            return tkmessagebox.showinfo(title, message, parent=self.window)
        if action == "question":
            return tkmessagebox.askquestion(title, message, parent=self.window)
        if action == "okcancel":
            return tkmessagebox.askokcancel(title, message, parent=self.window)
        if action == "yesnocancel":
            return tkmessagebox.askyesnocancel(title, message, parent=self.window)
        if action == "yesno":
            return tkmessagebox.askyesno(title, message, parent=self.window)

    @_check_window_and_dom
    def loadView(self, view):
        view = self.__handle_view(view)
        self.__browser_frame.isDocumentReady = False
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
        execJsOperations[operation_id] = None   
        self.__browser_frame.browser.ExecuteFunction("execJs", ["exec", operation_id, js_code])
        while not execJsOperations[operation_id]:
            time.sleep(0.01)
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
            windowFrame.windowCount-=1
            del allWindows[self._windowid]
            if windowFrame.windowCount == 0:
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

class _filedialog():
    def __init__(self, parentwindow):
        self.parentwindow = parentwindow 

    def _set_parent_window(func):
        def wrapper(self, **kw):
            kw['parent'] = self.parentwindow
            return func(self, **kw)     
        return wrapper

    @_set_parent_window
    def askopenfile(self, **kwargs):
        return tkfiledialog.askopenfilename(**kwargs)   
    @_set_parent_window
    def askopenfiles(self, **kwargs):
        return tkfiledialog.askopenfiles(**kwargs)    
    @_set_parent_window
    def asksaveasfile(self, **kwargs):
        return tkfiledialog.asksaveasfile(**kwargs)  
    @_set_parent_window
    def askopenfilename(self, **kwargs):
        return tkfiledialog.askopenfilename(**kwargs)    
    @_set_parent_window
    def askopenfilenames(self, **kwargs):
        return tkfiledialog.askopenfilenames(**kwargs)                            
    @_set_parent_window
    def asksaveasfilename(self, **kwargs):
        return tkfiledialog.asksaveasfilename(**kwargs)
    @_set_parent_window
    def askdirectory(self, **kwargs):
        return tkfiledialog.askdirectory(**kwargs)   
    @_set_parent_window
    def open(self, **kwargs):
        return tkfiledialog.Open(**kwargs)             
  

class BrowserFrame(tk.Frame):
    def __init__(self, frame, window_view):
        self.frame = frame
        self.window_view = window_view
        self.closing = False
        self.browser = None
        self.isDocumentReady = False
        tk.Frame.__init__(self, frame)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Configure>", self.on_configure)
        self.after(5, self.embed_browser)
        self.focus_set()
        self.master.master.focus_force() # <- added

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info,
                                             url=self.window_view,
                                             settings=BROWSER_SETTINGS)
        assert self.browser
        self.browser.SetClientHandler(LoadHandler(self, self.frame))
        self.browser.SetClientHandler(FocusHandler(self))
        self.browser.SetClientHandler(DisplayHandler())
        self.browser.SetJavascriptBindings(bindings)

        self.message_loop_work()

    def get_window_handle(self):
        if MAC:
            # noinspection PyUnresolvedReferences
            from AppKit import NSApp
            # noinspection PyUnresolvedReferences
            import objc
            logger.info("winfo_id={}".format(self.winfo_id()))
            # noinspection PyUnresolvedReferences
            content_view = objc.pyobjc_id(NSApp.windows()[-1].contentView())
            logger.info("content_view={}".format(content_view))
            return content_view
        elif self.winfo_id() > 0:
            return self.winfo_id()
        else:
            raise Exception("Couldn't obtain window handle")

    def message_loop_work(self):
        cef.MessageLoopWork()
        self.after(10, self.message_loop_work)

    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()

    def on_window_configure(self):
        # Root <Configure> event will be called when top window is moved
        if self.browser:
            self.browser.NotifyMoveOrResizeStarted()

    def on_mainframe_configure(self, width, height):
        if self.browser:
            if WINDOWS: # This makes stupid crashes and resizing problems
                set_window_pos(self.browser.GetWindowHandle(),
                               0, 0, 0, width, height, 0x0002)
            elif LINUX:
                self.browser.SetBounds(0, 0, width, height)
            self.browser.NotifyMoveOrResizeStarted()

    def on_focus_in(self, _):
        if self.browser:
            self.browser.SetFocus(True)
    
    def on_focus_out(self, _):
        if LINUX and self.browser:
            self.browser.SetFocus(False)

    def on_root_close(self):
        if self.browser:
            self.browser.CloseBrowser(True)
            self.browser = None
        else:
            self.destroy()


class FocusHandler(object):
    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnTakeFocus(self, next_component=None, **_):
        logger.debug("FocusHandler.OnTakeFocus, next={next}"
                     .format(next=next_component))

    def OnSetFocus(self, source, **_):
        logger.debug("FocusHandler.OnSetFocus, source={source}"
                     .format(source=source))
        if LINUX:
            return False
        else:
            return True

    def OnGotFocus(self, **_):
        if LINUX:
            self.browser_frame.focus_set()

class RenderHandler ():
    def OnTextSelectionChanged(self, **kwargs):
        selected_text = kwargs["selected_text"]
        selected_range = kwargs["selected_range"]
        logger.info(f"Text selected:\n1] Selected Text: {selected_text}\n2] Selected Range: {selected_range}")
    
    def StartDragging(self, **kwargs):
        drag_data = kwargs["drag_data"]
        allowed_ops = kwargs["allowed_ops"]
        x = kwargs["x"]
        y = kwargs["y"]
        logger.debug(f"Dragging data on the window: {drag_data}")

class DisplayHandler():
    def OnAddressChange(self, browser, frame, url):
        logger.debug(f"window address changed: {url}")

    def OnLoadingProgressChange(self, browser, progress):
        logger.debug(f"window loading progress: {progress}")

    def OnStatusMessage(self, browser, value):
        if value:
            logger.debug(f"window status message recieved: {value}")


class LoadHandler():
    def __init__(self, browser_frame, windowFrame):
        self.browser_frame = browser_frame
        self.windowFrame = windowFrame

    def OnBeforePopup(self, **kwargs): # To open target="_blank" in external browser
        target_url = kwargs['target_url']
        user_gesture = kwargs['user_gesture']
        if user_gesture:
            webbrowser.open(target_url)
        return True

    def OnLoadingStateChange(self, browser, is_loading, **_):
        if self.windowFrame._loadingTimesThreshold==0: 
            self.windowFrame._loadingTimesThreshold=1
            if not self.windowFrame.hidden and not self.windowFrame.minimized:
                self.windowFrame.master.deiconify()
        self.browser_frame.isDocumentReady = False # if you have noticed any wiered behavior related to js executrion remove this line
        if not is_loading:
            injection = js.handleJs(self.windowFrame._windowid, self.windowFrame.flexibleDrag)
            injection += css.handleStyle(self.windowFrame.contentSelection)
            browser.ExecuteJavascript(injection) 
            time.sleep(0.1)
            self.browser_frame.isDocumentReady = True

    def OnLoadStart(self, browser, **_):
        pass
    
    def OnLoadEnd(self, browser, **_):
        pass

    def OnLoadError(self, browser, **_):
        error_msg = "No internet connection OR incorrect file-path"
        logger.error(f'Window ID: {self.windowFrame.master.winfo_id()}' + f" | Error message: {error_msg}")
        


  