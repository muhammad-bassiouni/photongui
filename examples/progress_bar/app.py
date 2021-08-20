import photongui
import random
import time

import os

indexFile = os.path.join(os.path.dirname(__file__), "view/index.html")

settings = {
    "view":indexFile
}

window = photongui.createWindow(settings)

progress = 0
def main():
    def update_progress_bar():
        time.sleep(random.randint(1, 3))
        global progress
        progress+=5
        if progress <= 100:
            window.execJsAsync(f"document.querySelector('.bar').style.width = '{progress}%'; document.querySelector('.percent').innerText = '{progress}%'")
            time.sleep(1) 
            update_progress_bar()
    update_progress_bar()

photongui.start(function=main)