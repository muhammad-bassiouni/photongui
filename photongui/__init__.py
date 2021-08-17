
from cefpython3 import cefpython as cef
import logging
from functools import wraps
import threading 
import sys
import platform
import os
import shutil
import tkinter as tk

from photongui.window import createWindow
from photongui.windowBlueprint import windowFrame, Util


__all__ = ["createMainWindow", "createWindow"]

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")


# Logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(filename)s] %(levelname)s | %(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.disabled = True


CEF_SETTINGS = {
    "context_menu":{
                    "enabled":True,
                    "navigation":False,
                    "print":False,
                    "view_source":False,
                    "external_browser":False,
                    "devtools":False
                    },
    "debug":False,
    "net_security_expiration_enabled":True,
    "remote_debugging_port":-1
    #"multi_threaded_message_loop":True         
}


CEF_SWITCHES = {
    "enable-media-stream":True,
    "enable-speech-input":True
}  # full switches options can be found: https://peter.sh/experiments/chromium-command-line-switches/



def clearLogs():
    try:
        if os.path.exists('blob_storage'):
            shutil.rmtree('blob_storage')
        if os.path.exists('webrtc_event_logs'):
            shutil.rmtree('webrtc_event_logs')
        if os.path.exists('error.log'):
            os.remove('error.log')
    except:
        logger.error("Couldn't remove all/some log files during close the app!")

# Tk must be initialized before CEF otherwise fatal error 
root = tk.Tk()  
root.withdraw()

def init_cef():
    if MAC:
        CEF_SETTINGS["external_message_pump"] = True
    cef.Initialize(settings=CEF_SETTINGS, switches=CEF_SWITCHES)
    cef.DragData().GetLinkUrl()
    cef.DragData().GetLinkTitle()
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.MessageLoopWork()

def start(function=None, parameters=None, debug=False, debug_level="INFO", server=None, userAgent=None):  
    windowCount = windowFrame.windowCount
    if windowCount == 0:
        raise Exception("You have to create window first!")
    if debug:
        logger.disabled = False
        logger.setLevel(debug_level)

        CEF_SETTINGS["debug"] = True
        CEF_SETTINGS["context_menu"]["navigation"] = True
        CEF_SETTINGS["context_menu"]["print"] = True
        CEF_SETTINGS["context_menu"]["view_source"] = True
        CEF_SETTINGS["context_menu"]["external_browser"] = True
        CEF_SETTINGS["context_menu"]["devtools"] = True
        CEF_SETTINGS["remote_debugging_port"] = 0 # set it to 0 if you want any random one
    
    if userAgent:
        CEF_SETTINGS["user_agent"] = userAgent
    
    if function:
        def run(args=None):
            if args:
                t= threading.Thread(target=function, args=(args,))
            else:
                t= threading.Thread(target=function)
            t.start()

        if parameters:
            root.after(10, run, *parameters)
        else:
            root.after(10, run)

    if server:
        pass
        
    init_cef()
    root.mainloop()
    cef.Shutdown()
    clearLogs()


def threaded(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t_handler = threading.Thread(target=func, args=args, kwargs=kwargs)
        t_handler.daemon = True
        t_handler.start()
    return wrapper