js = """
window.alert = function(r){
	window.customAlert(r, windowID)
}
"""

src = """
var Alert = document.createElement("script");
Alert.innerHTML = `%s`;
document.head.appendChild(Alert);
""" % (js)