"""
BSD 3-Clause License

Copyright (c) 2021, Muhammed Bassiouni
All rights reserved.
"""

code = """
/* global stuff */
var windowID = WINDOWID
pyEnv = {}

/* global utils */
function generate_random_id(){
   	var randomID = '';
	var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
	var charactersLength = characters.length;
	for ( var i = 0; i < 8; i++ ) {
	  randomID += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return randomID;
}

/*************** Py Js bridge ***************/
/* exec js code and handle return to python of from python */
function execJs(PyOrder){
    var action = PyOrder[0]

    if (action == "return"){
        var status = PyOrder[1]
        var operation_id = PyOrder[2]
        var pyReturn = PyOrder[3]
        if (status == 500){
            console.error("python error: " + pyReturn)
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
            if (jsReturn == undefined || jsReturn == null){
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

/* exec python code */
var execPyOperations = {};
window.execPy = function(envName, pyCode){
	var js_operation_id = generate_random_id()
	execPyOperations[js_operation_id] = null  
	envName._evaluatePyCode(windowID, js_operation_id, pyCode)
    return new Promise(function (resolve) {
        var execPyTimer = setInterval(function () {
            if (execPyOperations[js_operation_id] != null) {
                clearInterval(execPyTimer);

                var return_value = execPyOperations[js_operation_id]
                delete execPyOperations[js_operation_id]
                resolve(return_value);
            }
        }, 10);
    });
}
"""
