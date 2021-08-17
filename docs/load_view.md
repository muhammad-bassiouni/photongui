## Load view to the window

**loadView(view)**

There are many options to change the current content (view) of the window. 

- Loading URL to the window
    ```python
    import photongui

    window = photongui.createWindow()

    def main():
        window.loadView("https://www.google.com")

    photongui.start(function=main)
    ```

- Loading html file to the window
    ```python
    import photongui

    window = photongui.createWindow()

    def main():
        window.loadView("<html file path>")

    photongui.start(function=main)
    ```

- Loading html text to the window.
  - **Note**: You have to include ***&lt;html&gt;*** tag in the text to work correctly
    ```python
    import photongui
    import time

    window = photongui.createWindow()

    html = """
    <html>
        <h1>This is new content</h>
    </html>
    """

    def main():
        time.sleep(3)
        window.loadView(html)

    photongui.start(function=main)
    ```