import tkinter as tk

from photongui.windowBlueprint import windowFrame


class createWindow(windowFrame):
    def __init__(self, windowSettings=None, parent=None, modal=False, confirmClose=False): 
        self.parent = parent.window if parent else None
        if self.parent:
            self.window = tk.Toplevel(self.parent)
        else:
            self.window = tk.Toplevel()
        super().__init__(window=self.window, window_settings=windowSettings, parent=self.parent, modal=modal, confirm_close=confirmClose)
        
    

    