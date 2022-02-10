import tkinter as tk
import ctypes 
import platform
import time
import webbrowser
from threading import Event
from cefpython3 import cefpython as cef

from photongui.util import logger
from photongui.api import js, css


# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Global browser config #
bindings = cef.JavascriptBindings(bindToFrames=True, bindToPopups=True)

# windows window handler
set_window_pos = ctypes.windll.user32.SetWindowPos


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


class BrowserFrame(tk.Frame):
    def __init__(self, master_frame, window_view):
        self.master_frame = master_frame
        self.window_view = window_view
        self.closing = False
        self.browser = None
        self.isDocumentReady = Event()
        tk.Frame.__init__(self, self.master_frame)
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
        self.browser.SetClientHandler(LoadHandler(self, self.master_frame))
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
        self.browser_frame.isDocumentReady = Event() # if you have noticed any wiered behavior related to js executrion remove this line
        if not is_loading:
            injection = js.handleJs(self.windowFrame._windowid, self.windowFrame.flexibleDrag)
            injection += css.handleStyle(self.windowFrame.contentSelection)
            browser.ExecuteJavascript(injection) 
            time.sleep(0.1)
            self.browser_frame.isDocumentReady.set()

    def OnLoadStart(self, browser, **_):
        pass
    
    def OnLoadEnd(self, browser, **_):
        pass

    def OnLoadError(self, browser, **_):
        error_msg = "No internet connection OR incorrect file-path"
        logger.error(f'Window ID: {self.windowFrame.master.winfo_id()}' + f" | Error message: {error_msg}")
        