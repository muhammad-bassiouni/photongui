import photongui
from photongui import Util

import os
import time


util = Util()
util.exposeAll("textHighlight", locals())

index = os.path.join(os.path.dirname(__file__),"view/index.html")

settings = {
    "view": index
}

def generateText():
    subtitle = [
        [[['00:00:00', '00:00:02']], ['A wise old owl sat in an Oak.']], 
        [[['00:00:02', '00:00:06']], ['The more he saw, the less he spoke, the less he spoke, the']], 
        [[['00:00:06', '00:00:07']], ['more he heard.']], 
        [[['00:00:07', '00:00:10']], ["Why can't we be like that wise old bird."]], 
    ]
    print("subtitle is generated in python")
    return subtitle
    
window = photongui.createWindow(settings)

photongui.start()

