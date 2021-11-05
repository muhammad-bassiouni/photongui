
"""
BSD 3-Clause License

Copyright (c) 2021, Muhammed Bassiouni
All rights reserved.
"""

import sys
import platform
import os
import shutil
import tkinter as tk
from cefpython3 import cefpython as cef
from threading import Thread

from photongui.util import logger, threaded
from photongui.window import createWindow
from photongui.windowBlueprint import windowFrame, allWindows, Util


__all__ = ["createWindow"]


# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Settings
CEF_SETTINGS = {
    "context_menu":{"enabled": False},
    "debug":False,
    "net_security_expiration_enabled":True,
    "remote_debugging_port":-1,
    "downloads_enabled":True,
    "ignore_certificate_errors":True,
    #"multi_threaded_message_loop":True         
}


CEF_SWITCHES = {
    "enable-media-stream":"",
    "enable-speech-input":"",
    "proxy-server":"direct://",
    #"enable-usermedia-screen-capturing":"",
    #"auto-select-desktop-capture-source":"",
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
    cef.DpiAware.EnableHighDpiSupport()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.MessageLoopWork()

# start related functions
def run_function_on_thread(function, args=None):
    if args:
        t= Thread(target=function, args=(args,))
    else:
        t= Thread(target=function)
    t.daemon = True
    t.start()

def start(function=None, args=None, debug=False, logLevel="INFO", userAgent='', locale="en-US", stringEncoding="utf-8", proxy=None):  
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
    windowCount = windowFrame.windowCount
    if windowCount == 0:
        raise Exception("You have to create window first!")
    if debug:
        logger.disabled = False
        logger.setLevel(logLevel.upper())
        CEF_SETTINGS["debug"] = True
        CEF_SETTINGS["remote_debugging_port"] = 0 # set it to 0 if you want any random one  
        CEF_SETTINGS["context_menu"]["enabled"]=True
    if userAgent:
        CEF_SETTINGS["user_agent"] = userAgent
    if proxy:
        CEF_SWITCHES["proxy-server"] = proxy
    CEF_SETTINGS["locale"] = locale
    CEF_SETTINGS["string_encoding"] = stringEncoding
    if function:
        if args:
            root.after(10, run_function_on_thread, function, *args)
        else:
            root.after(10, run_function_on_thread, function)
        
    init_cef()
    root.mainloop()
    cef.Shutdown()
    clearLogs()

def getAllWindows():
    return allWindows

