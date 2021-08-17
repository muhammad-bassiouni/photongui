from photongui import createWindow, Util
import mimetypes
import photongui 



mimetypes.add_type('application/javascript', ".mjs") 
 


settings = {
    "title": "PhotonPy",
    "view": "./photon/gui/html/welcome.html",
    "icon":r"gui\images\icon.png",
    "width":600,
    "height":600,
    "position":None,
    "resizable":(True, True),
    "disabled":False,
    "fullscreen":False,
    "minimized":True,
    "maximized":False,
    "min_size":None,
    "max_size":None,
    "hidden":False,
    "borderless":False,
    "border_color":None,
    "border_thickness":None,
    "padding":None,
    "toolwindow":False,
    "allow_minimize":True,
    "allow_maximize":True,
    "on_top":False,
    "movable":True,
    "background_color":"white",
    "transparency":1,
    "transparentcolor":None,
    "allow_text_selection":False,
    "flexible_drag":False,
}

# ./photon/gui/html/welcome.html  ----- https://www.youtube.com ------- ui/templates/index.html


expose = Util()
expose.exposeAll("pythonHere", locals())

Window1 = createWindow({"flexible_drag":True})

s = {"flexible_drag":True, "allow_text_selection":True}
s["title"] = "2"
Window2 = createWindow(s, parent=Window1)
s["title"] = "3"
Window3 = createWindow(s, parent=Window1)
s["title"] = "4"
Window4 = createWindow(s, parent=Window1)
s["title"] = "5"
Window5 = createWindow(s, parent=Window1)
s["title"] = "6"
Window6 = createWindow({"title":"6", "flexible_drag":True, "toolwindow":False, "transparentcolor":"green", "transparency":0.5}, parent=Window1)




jscode = r"""
        var h1 = document.createElement('h1')
        var text = document.createTextNode('Hello pywebview')
        h1.appendChild(text)
        document.body.appendChild(h1)

        document.body.style.backgroundColor = '#212121'
        document.body.style.color = '#f2f2f2'

        // Return user agent
        'User agent:\n' + navigator.userAgent;
        """

def main():
    #Window2.loadView(r"photon\gui\html\welcome.html")

    #print(MainWindow.execJsSync("document.readyState === 'complete'"))
    print("2   ########################################")
    print(Window2.execJsSync("document.body.innerText"))
        
    print("3   ########################################")
    print(Window3.execJsSync("document.body.innerText"))

    print("4   ########################################")
    print(Window4.execJsSync("document.body.innerText"))
    Window4.window.toggleFullscreen()
    print("5   ########################################")
    print(Window5.execJsSync("window.scrollTo(0, 500)"))
    print(Window5.execJsSync("document.body.style.background = 'green'"))
    

    #Window4.window.toggleFullscreen()
    print("This is all", Window4.execJsSync("var btns = document.querySelectorAll('.primary-btn'); for(btn of btns){btn.innerText}"))
    Window7 = createWindow({"title":"7", "flexible_drag":True})
    Window7.loadSnippet(".window-drag-area", "<p>this is injection</p>", "afterend")

def destroy():
    Window6.window.destroy()
def say():
    print("hi")
    return "done"
"""
execPy(window.pythonHere, "say()")
window.execPy(window.pythonHere, "sayy()").then(function(r){console.log(r)})
window.execPy(window.pythonHere, "destroy()").then(function(r){console.log(r)})
"""

if __name__ == "__main__":
    photongui.start(function=main , parameters= debug=True)



