src = """
var element = document.querySelector('%(elementSelector)s');
element.insertAdjacentHTML('%(position)s', '%(snippet)s');
"""