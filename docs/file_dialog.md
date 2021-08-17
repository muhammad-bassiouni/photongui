## File dialog

**fileDialog()** has the following parameters:
- **action**:
    ### available actions:
        - "saveasfilename"
        - "saveasfile"
        - "openfilename"
        - "openfile"
        - "selectdirectory"
        - "openfilenames"
        - "openfiles"
 - **title**: file dialog window title 
 - **default_extenxion**
 - **file_types**
    ### Example of setting file types
    ```
    filetypes = (("Text files", "*.txt")
                    ,("HTML files", "*.html;*.htm")
                    ,("All files", "*.*") )
    ```
- **initial_dir**
- **initial_file**
- **allow_multiple**
  
```python
import photongui
import time

window = photongui.createWindow()

filetypes = (
    ("Text files", "*.txt"),
    ("HTML files", "*.html;*.htm"),
    ("All files", "*.*")
)

def main():
    time.sleep(3)
    file_name = window.fileDialog(action="openfilename",
                      title="Choose file",
                      file_types=filetypes)
    print(file_name)

photongui.start(function=main)
```