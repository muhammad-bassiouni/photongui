from .utils import py_js_bridge, drag, alert, dragExternalFile

photonGuiJs = """
/* |||||||||||||||||||||||
   | photonGUI Injection |
   |||||||||||||||||||||||
*/
"""
def handleJs(windowId, flexibleDrag=False):
    js = photonGuiJs + py_js_bridge.code.replace('WINDOWID', str(windowId)) + alert.code + dragExternalFile.code
    if flexibleDrag:
        js += drag.code
    return """
    var js = document.createElement("script");
    js.innerHTML = `%s`;
    document.head.appendChild(js);
    """% (js)
    