js = """
// exec js code and handle return to python of from python
function execJs(PyOrder){
    var action = PyOrder[0]

    if (action == "return"){
        var status = PyOrder[1]
        var operation_id = PyOrder[2]
        var pyReturn = PyOrder[3]

        if (status == 500){
            console.error(pyReturn)
            return 
        }

        if(pyReturn == null){
            pyReturn = "None"
        }
        execPyOperations[operation_id] = pyReturn
    }
    else if(action == "exec"){
        var operation_id = PyOrder[1]
        var jsCode = PyOrder[2]

        try {
            jsReturn = eval(jsCode)
            if (jsReturn == undefined){
                jsReturn = "None"
            }
            finalReturn = [operation_id, jsReturn]
        }
        catch (e) {
            console.error(e.stack);
            finalReturn = [operation_id, e.stack]
        }
        finally {
            window.pyCallBack("execJs", finalReturn)
        }
    }
    
}

// exec python code
function generate_random_id(){
   	var result = '';
	var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
	var charactersLength = characters.length;
	for ( var i = 0; i < 8; i++ ) {
	  result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

var execPyOperations = {};
window.execPy = function(ExposedEnvironName, pyCode){
	var js_operation_id = generate_random_id()
	execPyOperations[js_operation_id] = null  
	ExposedEnvironName.evaluatePyCode(windowID, js_operation_id, pyCode)
    return new Promise(function (resolve) {
        var execPyTimer = setInterval(function () {
            if (execPyOperations[js_operation_id] != null) {
                clearInterval(execPyTimer);

                var return_value = execPyOperations[js_operation_id]
                delete execPyOperations[js_operation_id]
                resolve(return_value);
            }
        }, 500);
    });
}

"""

src = """
var js_bridge = document.createElement("script");
js_bridge.innerHTML = %(js)s;
js_bridge.innerHTML += 'var windowID = WINDOWID'
document.head.appendChild(js_bridge);
"""% {"js":js}