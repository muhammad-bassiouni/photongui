
drag_area_class = ".window-drag-area"
code = """/*************** Flexible Drag ***************/
var startX = 0;
var startY = 0;

function onMouseMove(ev) {
    var x = ev.screenX - startX;
    var y = ev.screenY - startY;
    window.pyCallBack('dragWindow', [windowID, [x, y]]);
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
        if (document.querySelector('%(selector)s') != null) {
            clearInterval(dragTimer);

            var dragAreas = document.querySelectorAll('%(selector)s');
            for(var i=0; i < dragAreas.length; i++) {
                dragAreas[i].addEventListener('mousedown', onMouseDown);
            }
        }
}, 10); 
"""% {"selector":drag_area_class}

