import toga
from toga.style import Pack
from toga.style.pack import COLUMN

class SettingsElement:
    
    def __init__(self):
        self.gui = toga.Box(style=Pack(direction=COLUMN, padding_bottom=5))
        pass

    def save(self):
        pass

    def load_settings(self):
        pass