baseStyle = """body {-webkit-print-color-adjust: exact; %s} img, a {user-drag: none; -webkit-user-drag: none;}"""
textSelectionDisabled = '-webkit-user-select: none; -khtml-user-select: none; -ms-user-select: none; user-select: none; cursor: default;'
#imgAnchorDragDisabled = 'img, a {user-drag: none; -webkit-user-drag: none;}'

def handleStyle(contentSelection=False):
    if contentSelection:
        style = baseStyle%("")
    else:
        style = baseStyle%(textSelectionDisabled)
    return  """
    var css = document.createElement("style");
    css.innerHTML = '%s';
    document.head.appendChild(css);
    """% (style)