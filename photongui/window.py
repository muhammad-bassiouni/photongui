import tkinter as tk

from photongui.windowBlueprint import windowFrame




class createWindow(windowFrame):
    def __init__(self, window_settings=None, parent=None, modal=None, confirm_close=None): 
        self.parent = parent.window if parent else None

        if self.parent:
            self.window = tk.Toplevel(self.parent)
        else:
            self.window = tk.Toplevel()
        super().__init__(window=self.window, window_settings=window_settings, parent=self.parent, modal=modal, confirm_close=confirm_close)
        
    

    