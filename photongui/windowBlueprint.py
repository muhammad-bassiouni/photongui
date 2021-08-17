from cefpython3 import cefpython as cef
import ctypes 
try:
    import tkinter as tk
except ImportError:
    import tkinter as tk
import tkinter.filedialog as tkfiledialog
from tkinter.messagebox import askyesno
import os
import threading
import platform
import re
import string
import random
import time

import photongui

from photongui.api import py_js_bridge, css, drag, loadSnippet
import photongui.window

# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Global Variables
execJsOperations = {}
windowsId = {}
evt = threading.Event()

# Global stuff
default_html_code = os.path.join(os.getcwd(), "photongui/gui/html/welcome.html")


# Global config
bindings = cef.JavascriptBindings(bindToFrames=True, bindToPopups=True)

WINDOW_SETTINGS = {
    "title": "PhotonGUI",
    "view": "<html><h1 class='window-drag-area'>Welcome To PhotonPy</h1></html>",
    "icon":r"gui\images\icon.png",
    "width":600,
    "height":600,
    "position":None,
    "resizable":(True, True),
    "disabled":False,
    "fullscreen":False,
    "minimized":False,
    "maximized":False,
    "min_size":None,
    "max_size":None,
    "hidden":False,
    "borderless":False,
    "border_color":None,
    "border_thickness":None,
    "padding":None,
    "toolwindow":True,
    "allow_minimize":True,
    "allow_maximize":True,
    "on_top":False,
    "movable":True,
    "background_color":"#FFFFFF",
    "transparency":1,
    "transparentcolor":None,
    "allow_text_selection":False,
    "flexible_drag":False,
}

BROWSER_SETTINGS = {
    "web_security_disabled": True,
    "file_access_from_file_urls_allowed": True,
    "universal_access_from_file_urls_allowed": True,
    "javascript_close_windows_disallowed":True,
    "dom_paste_disabled":False,
    "javascript_access_clipboard_disallowed":False,
    "tab_to_links_disabled":False,
    "webgl_disabled":False
}

# This function to recieve the return from js to handle and store it in python
def pyCallBack(action, finalReturn):
    if action == "execJs":
        operation_id = finalReturn[0]
        operation_result = finalReturn[1]
        execJsOperations[operation_id] = operation_result
    if action == "moveWindow": # in order to set the drag area, you have to set the element class name to be "window-drag-area"
        windowId = finalReturn[0]
        x = finalReturn[1][0]
        y = finalReturn[1][1]
        windowsId[windowId].window.geometry(f"+{x}+{y}")
    if action == "msg":
        print(finalReturn)

# This class gives some utilites, like expose all variables and functions of the current working file to browser
class Util:
    name = None
    eviron = None
    def exposeAll(self, name, environ=None):
        self.name = name
        self.environ = environ
        bindings.SetObject(name, self)

    # Note: Don't use the following method, to avoid problems, this method is used by js inside browser to exec py code and handle return back
    def evaluatePyCode(self,windowid, operationid, pyCode):
        windowid = windowid
        operationid = operationid
        try:
            return_value = eval(pyCode, self.environ)
            status = 200
        except Exception as e:
            return_value = str(e)
            status = 500
        windowsId[windowid].execJsFunctionAsync("execJs", ["return", status, operationid, return_value])
        

bindings.SetFunction("pyCallBack", pyCallBack)


class windowFrame(tk.Frame):
    windowCount = 0
    def __init__(self, window, window_settings=None, parent=None, modal=None, confirm_close=None):
        windowFrame.windowCount+=1
        self.window = window # you can access all tkinter window features through this attri
        self.__settings = WINDOW_SETTINGS if not window_settings else window_settings
        self.__parent = parent if parent else None
        self.__modal = modal
        self.__confirm_close = confirm_close

        self._windowid = self.window.winfo_id()

        self.__browser_frame = None
        self.__centerTheWindowByDefault = True

        self.__windowFrame_attributes_generator() # This generates attributes of this class from "WINDOW_SETTINGS" dynamically

        self.__view = self.__handle_view(self.view)

        # adding new method to the defualt tkinter window methods
        self.window.centerWindow = self.__centerWindow
        self.window.setIcon = self.__setIcon
        self.window.toggleFullscreen = self.__toggleFullscreen

        self.__set_default_window_settings() # after generating the required attributes to initiate the window, now we structure the window based on them

        tk.Frame.__init__(self, self.window, highlightbackground=self.border_color, highlightthickness=self.border_thickness, bd=self.padding)
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
        self.__browser_frame.grid(row=1, column=0,
                                sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

        # Pack WindowFrame
        self.pack(fill=tk.BOTH, expand=tk.YES)

      
    ## private methods
    def __windowFrame_attributes_generator(self):
        for key, value in WINDOW_SETTINGS.items():
            setattr(self, key, self.__settings.get(key, value))

    def __set_default_window_settings(self):
        self.window.title(self.title)
        self.window.after(20, self.__setIcon, self.icon)
        self.window.attributes('-fullscreen', self.fullscreen, '-topmost',self.on_top, '-alpha',self.transparency, '-disabled',self.disabled)
        self.window.configure(bg=self.background_color)
        self.window.overrideredirect(self.borderless)
        self.window.resizable(self.resizable[0], self.resizable[1])
        # start window in minimized mode
        """ this integration cause the following issue: related to cef -> it freezes the whole browser
        if self.minimized:
            self.window.iconify()
        """
        if self.__modal:
            if self.__parent:
                self.setWindowAsModal(self.__parent)
            else:
                photongui.logger.warn("The modal window mode will not work unless you set the parent window!")
        if self.transparentcolor:
            self.window.attributes('-transparentcolor',self.transparentcolor)
        if self.maximized:
            self.window.state('zoomed')
        if self.min_size:
            self.window.minsize(self.min_size[0], self.min_size[1])
        if self.max_size:
            self.window.maxsize(self.max_size[0], self.max_size[1])
        if self.hidden:
            self.window.withdraw()
        if not self.allow_maximize:
            self.window.resizable(False, False)
        if not self.toolwindow:
            self.window.attributes('-toolwindow', True)
        if self.position:
            self.__centerTheWindowByDefault = False
            self.window.geometry(f"{self.width}x{self.height}+{self.width}+{self.height}")
        if not self.position:
            self.__centerWindow()
        if not self.movable:
            #self.window.bind_all('<Configure>', self.__fixWindowPosition)
            pass
        
        self.__add_windowId_to_dict()

    def __setIcon(self, iconPath):
        icon_path = iconPath
        if os.path.exists(icon_path) and icon_path.endswith(".png"):
            try:
                icon = tk.PhotoImage(file=icon_path)
                self.window.tk.call('wm', 'iconphoto', self.window._w, icon)
            except:
                photongui.logger.warn("The icon couldn't be set due to unknown problem. Try to use another one and make sure you put the correct path and the image is of type '.png'")
        else:
            photongui.logger.info("If you are trying to set icon and it doesn't show, Check icon path and icon extenstion to be '.png'")
            icon_path = os.path.join(os.path.dirname(__file__), "gui\images\icon.png")
            icon = tk.PhotoImage(file=icon_path)
            self.window.tk.call('wm', 'iconphoto', self.window._w, icon)  

    def __centerWindow(self):
        if self.__centerTheWindowByDefault:
            windowWidth, windowHeight = self.width, self.height
        else:
            windowWidth, windowHeight = map(int, self.window.geometry().split("+")[0].split("x")[0:2])
        position_x = int(self.window.winfo_screenwidth()/2 - windowWidth/2)
        position_y = int(self.window.winfo_screenheight()/2 - windowHeight/2)
        center = (position_x, position_y)
        self.window.geometry(f"{self.width}x{self.height}+{center[0]}+{center[1]}")

    def __fixWindowPosition(self, event): # This function needs some work to make it work correctly
        X = self.window.winfo_geometry().split("+")[1]
        Y = self.window.winfo_geometry().split("+")[2]
        self.window.geometry("+{}+{}".format(X,Y))

    def __handle_view(self, view):
        """this function handle what will be viewed on the browser based on the input:
        * if the view starts with "htmlcode:" then it will be treated as pure html input
        * if the view starts with "http" then it will treated as link
        * if the view is not one of the previous, then it will be treated as local .html file
        """
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
        windowsId[self.window.winfo_id()] = self

    def __does_window_exist(self):
        if not self.master.winfo_exists(): # we check if window exists or not to avoid creshes
            photongui.logger.error("The window doesn't exist!")
            return False
        else:
            return True

    # public methods    
    def setWindowAsModal(self, parent):
        try:
            parent.attributes('-disabled', True)
        except:
            parent = parent.window # in case this method is called from outside this file
            parent.attributes('-disabled', True)
        #self.window.grab_set() # this causes other windows to be not closed correctly
        self.window.wm_transient(parent)

    def fileDialog(self, action, title=None, default_extenxion=None, file_types=None, initial_dir=None, initial_file=None, allow_multiple=False):
        """
        * available actions:\n
            \t- "saveasfilename"\n
            \t- "saveasfile"\n
            \t- "openfilename"\n
            \t- "openfile"\n
            \t- "selectdirectory"\n
            \t- "openfilenames"\n
            \t- "openfiles"

        * Example of setting the file types:\n
            \tfiletypes = (("Text files", "*.txt")
                    ,("HTML files", "*.html;*.htm")
                    ,("All files", "*.*") )
        """
        self.window.update_idletasks() # adding this here fixes the focus issue
        options = {}
        if title:
            options['title'] = title
        if initial_file:
            options["initialfile"] = initial_file
        options["parent"] = self.window
        options['defaultextension'] = '.*' if not default_extenxion else default_extenxion
        options['filetypes'] = [('All Files', '.*')] if not file_types else file_types
        options['initialdir'] = '/' if not initial_dir else initial_dir
        options["multiple"] = allow_multiple
        """trying to add the ability to show or hide hidden files with openfiledialog
        try:
            self.window.tk.call('tk_getOpenFile', '-foobarbaz')
        except:
            pass
        self.window.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
        self.window.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
        """
        if action == "saveasfilename": return tkfiledialog.asksaveasfilename(**options)
        if action == "saveasfile": return tkfiledialog.asksaveasfile(**options)
        if action == "openfilename": return tkfiledialog.askopenfilename(**options)
        if action == "openfile": return tkfiledialog.askopenfile(**options)
        if action == "selectdirectory": return tkfiledialog.askdirectory(**options)
        if action == "openfilenames": return tkfiledialog.askopenfilenames(**options)
        if action == "openfiles": return tkfiledialog.askopenfiles(**options)

    # Change the current view of the window, may be: new url or new html text or new html file
    def loadView(self, view):
        view = self.__handle_view(view)
        time.sleep(0.1)
        self.__browser_frame.initialized = False # This is important to make sure that any next execution wait till the initialized status of browser become True again through "OnLoadStateChange" of browser
        self.__browser_frame.browser.LoadUrl(view)

    def loadSnippet(self, elementSelector, snippet, position):
        """ You can use this method to inject html code into the current view.
        
        ### How to use it:
        * elementSelector [str]: specify element by css selector, e.g. for class you put '.' befor element class name and so on.
        * snippet [str]: the html code or whatever you want to inject.
        * position [str]: the position where the code will be injected, the available options are:\n
            [1] 'beforebegin': Before the element itself.\n
            [2] 'afterbegin': Just inside the element, before its first child. \n
            [3] 'beforeend': Just inside the element, after its last child.\n
            [4] 'afterend': After the element itself.\n
        
        """
        inject = loadSnippet.src % {"elementSelector":elementSelector, "snippet":snippet, "position":position}
        while not self.__browser_frame.initialized:
            time.sleep(0.5)  
        self.__browser_frame.browser.ExecuteJavascript(inject)
    
    def execJsAsync(self, js_code): # execute js code asynchronously
        if not self.__does_window_exist(): # we check if window exists or not to avoid creshes
            return 

        while not self.__browser_frame.initialized:
            time.sleep(0.5)  
        self.__browser_frame.browser.ExecuteJavascript(js_code)

    def execJsSync(self, js_code): # execute js code synchronously
        if not self.__does_window_exist(): # we check if window exists or not to avoid creshes
            return 

        operation_id = self.__create_random_id()
        execJsOperations[operation_id] = None   
        while not self.__browser_frame.initialized:
            time.sleep(0.5)  
        self.__browser_frame.browser.ExecuteFunction("execJs", ["exec", operation_id, js_code])
        while not execJsOperations[operation_id]:
            time.sleep(0.5)
        return_value = execJsOperations[operation_id]
        del execJsOperations[operation_id] # To free memory
        return return_value

    def execJsFunctionAsync(self, function_name, function_parameres=[]):
        if not self.__does_window_exist():
            return

        while not self.__browser_frame.initialized:
            time.sleep(0.5)  
        
        self.__browser_frame.browser.ExecuteFunction(function_name, function_parameres)

    def getUrl(self):
        return self.__browser_frame.browser.GetUrl() 
 
    def getZoomLevel(self):
        return self.__browser_frame.browser.GetZoomLevel()
    
    def setZoomLevel(self, zoom_level=0):
        self.__browser_frame.browser.SetZoomLevel(zoom_level)

    def canGoForward(self):
        return self.__browser_frame.browser.CanGoForward()

    def goForward(self):
        self.__browser_frame.browser.GoForward()
    
    def canGoBack(self):
        return self.__browser_frame.browser.CanGoBack()

    def goBack(self):
        self.__browser_frame.browser.GoBack()
   
    def findInBrowser(self, search_id=None, search_text="", forward=False, match_case=False, find_next=False):
        self.__browser_frame.browser.Find(search_id, search_text, forward, match_case, find_next)

    def stopFinding(self, clear_selection=True):
        self.__browser_frame.browser.StopFinding(clear_selection)

    def downloadFromURL(self, url=None):
        self.__browser_frame.browser.StartDownload(url)
    
    def reloadWindow(self): # Reload the current page without ignoring any cached data.
        self.__browser_frame.browser.Reload()
    
    def reloadWindoInogreCache(self): # Reload the current page ignoring any cached data.
        self.__browser_frame.browser.ReloadIgnoreCache()

    def isWindowLoaded(self):
        return self.__browser_frame.browser.HasDocument()
    
    def stopLoadingPage(self):
        self.__browser_frame.browser.StopLoad()

    def printWindowContent(self):
        return self.__browser_frame.browser.Print()
    
    def sendKeyEvent(self, key_event=None):
        self.__browser_frame.browser.SendKeyEvent(key_event)

    def sendMouseMoveEvent(self,x=0, y=0, mouse_leave=False):
        self.__browser_frame.browser.SendMouseMoveEvent(x, y, mouse_leave)

    def sendMouseClickEvent(self, x=0, y=0, mouseButtonType=1, mouseUp=True, clickCount=1, modifiers=1):
        """ How to use it:
        - x [int]
        - y [int]
        - mouseButtonType [int] may be one of:\n
            \t1] MOUSEBUTTON_LEFT \n
            \t2] MOUSEBUTTON_MIDDLE\n
            \t3] MOUSEBUTTON_RIGHT\n
        - modifiers flags [int]:\n
            \t1] EVENTFLAG_NONE\n
            \t2] EVENTFLAG_CAPS_LOCK_ON\n
            \t3] EVENTFLAG_SHIFT_DOWN\n
            \t4] EVENTFLAG_CONTROL_DOWN\n
            \t5] EVENTFLAG_ALT_DOWN\n
            \t6] EVENTFLAG_LEFT_MOUSE_BUTTON\n
            \t7] EVENTFLAG_MIDDLE_MOUSE_BUTTON\n
            \t8] EVENTFLAG_RIGHT_MOUSE_BUTTON\n
            \t9] EVENTFLAG_COMMAND_DOWN (Mac)\n
            \t10] EVENTFLAG_NUM_LOCK_ON (Mac)\n
            \t11] EVENTFLAG_IS_KEY_PAD (Mac)\n
            \t12] EVENTFLAG_IS_LEFT (Mac)\n
            \t13] EVENTFLAG_IS_RIGHT (Mac)\n
        - mouseUp [bool]
        - clickCount [int]
        """
        self.__browser_frame.browser.SendMouseClickEvent(x, y, mouseButtonType, mouseUp, clickCount, modifiers)
    
    def sendMouseWheelEvent(self, x=0, y=0, deltaX=0, deltaY=0, modifiers=1):
        """ How to use it:
        - x [int]
        - y [int]
        - deltaX [int]
        - deltaY [int]

        - modifiers flags [int]:\n
            \t1] EVENTFLAG_NONE\n
            \t2] EVENTFLAG_CAPS_LOCK_ON\n
            \t3] EVENTFLAG_SHIFT_DOWN\n
            \t4] EVENTFLAG_CONTROL_DOWN\n
            \t5] EVENTFLAG_ALT_DOWN\n
            \t6] EVENTFLAG_LEFT_MOUSE_BUTTON\n
            \t7] EVENTFLAG_MIDDLE_MOUSE_BUTTON\n
            \t8] EVENTFLAG_RIGHT_MOUSE_BUTTON\n
            \t9] EVENTFLAG_COMMAND_DOWN (Mac)\n
            \t10] EVENTFLAG_NUM_LOCK_ON (Mac)\n
            \t11] EVENTFLAG_IS_KEY_PAD (Mac)\n
            \t12] EVENTFLAG_IS_LEFT (Mac)\n
            \t13] EVENTFLAG_IS_RIGHT (Mac)\n

        - mouseUp [bool]

        - clickCount [int]
        """
        self.__browser_frame.browser.SendMouseWheelEvent(x, y, deltaX, deltaY, modifiers)

    def setAccessibilityState(self, state="default"):
        """Available state:
        - default
        - enabled
        - disabled
        """
        states = {"default":1, "enabled":2, "disabled":3}
        if state not in states.keys():
            photongui.logger.error(f"You have to set the state value to be on of the following {states.keys()}")
        else:
            self.__browser_frame.browser.SetAccessibilityState(states[state])

    ## static methods
    @staticmethod
    def __create_random_id():
        characters = string.ascii_letters + string.digits
        id = ''.join(random.choice(characters) for i in range(8))
        return id

    ## Window sensors of to handle the browser frame 
    def __on_window_configure(self, _):
        photongui.logger.debug(f"MainFrame: {self}.on_window_configure")
        if self.__browser_frame:
            self.__browser_frame.on_window_configure()

    def __on_configure(self, event):
        photongui.logger.debug(f"MainFrame: {self}.on_configure")
        if self.__browser_frame:
            width = event.width
            height = event.height

            self.__browser_frame.on_mainframe_configure(width, height)

    def __on_focus_in(self, _):
        photongui.logger.debug(f"MainFrame: {self}.on_focus_in")

    def __on_focus_out(self, _):
        photongui.logger.debug(f"MainFrame: {self}.on_focus_out")
        self.master.focus_force() # <- added

    def __on_destroy(self, event):
        if event.widget == self.master:
            windowFrame.windowCount-=1
            
            if windowFrame.windowCount == 0:
                photongui.root.destroy()

    def __on_close(self):
        if self.__confirm_close:
            if askyesno(title="Close window", message="Are you sure that you want to exit?", parent=self.window):
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
            # you have to set focus on the window to make escape key works
            self.window.focus_set()
            self.window.attributes("-fullscreen", False)


class BrowserFrame(tk.Frame):

    def __init__(self, frame, window_view):
        self.frame = frame
        self.window_view = window_view
        self.closing = False
        self.browser = None
        self.initialized = False
        tk.Frame.__init__(self, frame)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Configure>", self.on_configure)

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
        self.browser.SetJavascriptBindings(bindings) # This step is important to expose python things to js

        self.message_loop_work()

    def get_window_handle(self):
        if MAC:
            # noinspection PyUnresolvedReferences
            from AppKit import NSApp
            # noinspection PyUnresolvedReferences
            import objc
            photongui.logger.info("winfo_id={}".format(self.winfo_id()))
            # noinspection PyUnresolvedReferences
            content_view = objc.pyobjc_id(NSApp.windows()[-1].contentView())
            photongui.logger.info("content_view={}".format(content_view))
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
            if WINDOWS:
                ctypes.windll.user32.SetWindowPos(
                    self.browser.GetWindowHandle(), 0,
                    0, 0, width, height, 0x0002)
            elif LINUX:
                self.browser.SetBounds(0, 0, width, height)
            self.browser.NotifyMoveOrResizeStarted()

    def on_focus_in(self, _):
        photongui.logger.debug(f"BrowserFrame: {self.frame}.on_focus_in")
        if self.browser:
            self.browser.SetFocus(True)
    
    def on_focus_out(self, _):
        photongui.logger.debug(f"BrowserFrame: {self.frame}.on_focus_out")
        """For focus problems see Issue #255 and Issue #535. """
        if LINUX and self.browser:
            self.browser.SetFocus(False)

    def on_root_close(self):
        photongui.logger.debug(f"BrowserFrame: {self.frame}.on_root_close")
        if self.browser:
            photongui.logger.debug(f"CloseBrowserOf: {self.frame}")
            self.browser.CloseBrowser(True)
            # Clear browser references that you keep anywhere in your
            # code. All references must be cleared for CEF to shutdown cleanly.
            self.browser = None
        else:
            photongui.logger.debug(f"tk.Frame: {self.frame}.destroy")
            self.destroy()


class FocusHandler(object):

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnTakeFocus(self, next_component, **_):
        photongui.logger.debug("FocusHandler.OnTakeFocus, next={next}"
                     .format(next=next_component))

    def OnSetFocus(self, source, **_):
        photongui.logger.debug("FocusHandler.OnSetFocus, source={source}"
                     .format(source=source))
        if LINUX:
            return False
        else:
            return True

    def OnGotFocus(self, **_):
        photongui.logger.debug("FocusHandler.OnGotFocus")
        #self.browser_frame.focus_set() # <- back to the reference implementation: this implementation causes the app to freeze
        if LINUX:
            self.browser_frame.focus_set()


class LoadHandler():

    def __init__(self, browser_frame, windowFrame):
        self.browser_frame = browser_frame
        self.windowFrame = windowFrame

    def OnLoadingStateChange(self, browser, is_loading, **_):
        self.browser_frame.initialized = False # if you have noticed any wiered behavior related to js executrion remove this line
        if not is_loading:
            # injection of default code to take control of browser, you have to wait till browser is loaded 
            # to make sure that js code execution works fine without problems
            injection = py_js_bridge.src.replace("WINDOWID", str(self.windowFrame._windowid))
            if not self.windowFrame.allow_text_selection:
                injection += css.src
            if self.windowFrame.flexible_drag:
                injection += drag.src
  
            browser.ExecuteJavascript(injection) 
            time.sleep(0.1)
            self.browser_frame.initialized = True

    def OnLoadStart(self, browser, **_):
        pass
    
    def OnLoadEnd(self, browser, **_):
        pass

    def OnLoadError(self, browser, **_):
        error_msg = "Please check your internet connection or the right file path"
        msg_js = f"console.error('{error_msg}'); window.pyCallBack('msg', 'Window: {self.windowFrame.title} {error_msg}')"
        photongui.logger.error(f'Window: {self.windowFrame.title} ' + error_msg)
        browser.ExecuteJavascript(msg_js)
        
        