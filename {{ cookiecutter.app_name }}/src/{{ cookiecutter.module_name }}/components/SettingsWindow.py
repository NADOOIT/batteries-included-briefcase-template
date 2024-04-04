import os
import json
import toga
from toga.style import Pack
from toga.style.pack import COLUMN

from nadoo_telemarketing.services import set_settings, get_settings,set_user_code, set_api_key

class SettingsWindow(toga.Window):
    def __init__(self, title, width=400, height=400):
        super().__init__(title, size=(width, height))
        self.content = self.build()
        self.load_settings()
       
    def build(self):
        # Hauptcontainer für den Inhalt erstellen
        box = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))

        # Eingabefeld für den User Code erstellen
        self.user_code_input = toga.TextInput(
            placeholder="User Code",
            style=Pack(padding_bottom=10)
        )
        box.add(self.user_code_input)

        # Eingabefeld für den NADOO API Schlüssel erstellen
        self.api_key_input = toga.TextInput(
            placeholder="NADOO API Schlüssel",
            style=Pack(padding_bottom=10)
        )
        box.add(self.api_key_input)

        # Speichern-Button hinzufügen
        save_button = toga.Button(
            'Speichern',
            on_press=self.save_settings,
            style=Pack(padding_top=10)
        )
        box.add(save_button)

        # Schließen-Button hinzufügen
        close_button = toga.Button(
            'Schließen',
            on_press=self.close_window,
            style=Pack(padding_top=10)
        )
        box.add(close_button)

        return box
    
    def close_window(self, widget):
        self.close()
        
        
    def save_settings(self, widget):
        set_user_code(self.user_code_input.value)
        set_api_key(self.api_key_input.value)
        
    def load_settings(self):
        settings = get_settings()
        self.user_code_input.value = settings.get("user_code", "")
        self.api_key_input.value = settings.get("api_key", "")