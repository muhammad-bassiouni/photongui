def src(cssFilePath):
    cssFilePath = cssFilePath.replace('\\', '/')
    return f"""var element = document.querySelector('head');
element.insertAdjacentHTML('beforeend', "<link href='{cssFilePath}' rel='stylesheet'>");
"""