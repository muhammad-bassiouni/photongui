import photongui
from photongui import createWindow, Util


expose = Util()
expose.exposeAll("pythonHere", locals())

Window = createWindow()

def main():
    print(Window.execJsSync("document.body.innerText"))
        
    Window.loadSnippet(".window-drag-area", "<p>this is injection</p>", "afterend")



if __name__ == "__main__":
    photongui.start(function=main , debug=True, )



