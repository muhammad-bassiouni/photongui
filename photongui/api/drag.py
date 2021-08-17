
drag_area_class = ".window-drag-area"
js = """
var initialX = 0;
var initialY = 0;

function onMouseMove(ev) {
    var x = ev.screenX - initialX;
    var y = ev.screenY - initialY;
    window.pyCallBack('moveWindow', [windowID, [x, y]]);
}

function onMouseUp() {
    window.removeEventListener('mousemove', onMouseMove);
}

function onMouseDown(ev) {
    initialX = ev.clientX;
    initialY = ev.clientY;
    window.addEventListener('mouseup', onMouseUp);
    window.addEventListener('mousemove', onMouseMove);
}
var dragTimer = setInterval(function() {
        if (document.querySelector('%(element)s') != null) {
            clearInterval(dragTimer);

            var dragBlocks = document.querySelectorAll('%(element)s');
            for(var i=0; i < dragBlocks.length; i++) {
                dragBlocks[i].addEventListener('mousedown', onMouseDown);
            }
        }
}, 10); 
"""% {"element":drag_area_class}

src = f"""
var js_drag = document.createElement("script");
js_drag.innerHTML = `{js}`;
document.head.appendChild(js_drag);
"""