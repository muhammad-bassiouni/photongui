import photongui
from photongui import Util

util = Util()
util.exposeAll("fileDialog", locals())


html = """
<html>
    <button class="show-result" onclick="file_dialog()">Select file</button>

    <span class='result'>This will be replaced with the result from python</span>
    
    <script>
        var result_holder = document.querySelector('.result')

        function file_dialog(){
            window.execPy(window.fileDialog, `window.fileDialog.askopenfilename(title="File Dialog From JS")`)
            .then((r)=>{
                    result_holder.innerText = r
                }
            )
        }
    </script>
</html>
"""
settings = {
    "view":html
}

window = photongui.createWindow(settings)

photongui.start()
