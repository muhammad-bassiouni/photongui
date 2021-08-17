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