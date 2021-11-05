import photongui
import os


indexFile = os.path.join(os.path.dirname(__file__), "view/index.html")

settings = {
    "view":indexFile
}

window = photongui.createWindow(settings)

photongui.start(debug=True)