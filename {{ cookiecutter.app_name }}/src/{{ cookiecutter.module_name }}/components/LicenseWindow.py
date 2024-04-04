import os
import toga
from toga.style import Pack
from toga.style.pack import COLUMN


class LicenseWindow(toga.Window):
    def __init__(self, title, width=400, height=400):
        super().__init__(title, size=(width, height))
        self.content = self.build()

    def build(self):
        # Create the main content box
        box = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))

        license_text=""
        license_path = os.path.join(self.app.paths.app , "resources" , "lizenzen.txt")
        
        with open(license_path, "r") as f:
            license_text = f.read()

        # Create a label to display the license text
        license_textfield = toga.MultilineTextInput(value=license_text, style=Pack(padding_bottom=10, height=700, width=600), readonly=True)

        # Add the label to the box
        box.add(license_textfield)

        # Optionally, add a close button
        close_button = toga.Button('Close', on_press=self.close_window, style=Pack(padding_top=10))
        box.add(close_button)

        return box

    def close_window(self, widget):
        self.close()

    
