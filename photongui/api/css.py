style = 'body {-webkit-user-select: none; -khtml-user-select: none; -ms-user-select: none; user-select: none; cursor: default;}'

src = """
var cssTimer = setInterval(function() {
        if (document.readyState === "complete") {
            clearInterval(cssTimer);

            var css = document.createElement("style");
            css.innerHTML = '%s';
            document.head.appendChild(css);
        }
}, 10); 
"""% (style)