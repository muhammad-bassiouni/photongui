
drag_area_class = ".window-drag-area"
js = """
var startX = 0;
var startY = 0;

function onMouseMove(ev) {
    var x = ev.screenX - startX;
    var y = ev.screenY - startY;
    window.pyCallBack('moveWindow', [windowID, [x, y]]);
}

function onMouseUp() {
    window.removeEventListener('mousemove', onMouseMove);
}

function onMouseDown(ev) {
    startX = ev.clientX;
    startY = ev.clientY;
    window.addEventListener('mouseup', onMouseUp);
    window.addEventListener('mousemove', onMouseMove);
}
var dragTimer = setInterval(function() {
        if (document.querySelector('%(element)s') != null) {
            clearInterval(dragTimer);

            var dragAreas = document.querySelectorAll('%(element)s');
            for(var i=0; i < dragAreas.length; i++) {
                dragAreas[i].addEventListener('mousedown', onMouseDown);
            }
        }
}, 10); 
"""% {"element":drag_area_class}

src = f"""
var js_drag = document.createElement("script");
js_drag.innerHTML = `{js}`;
document.head.appendChild(js_drag);
"""