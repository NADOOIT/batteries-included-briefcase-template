import os
import json
from typing import List, Optional
import toga
from toga.style import Pack
from toga.style.pack import COLUMN

from {{ cookiecutter.module_name }}.services import get_settings,set_user_code, set_api_key
from {{ cookiecutter.module_name }}.SettingsElement import SettingsElement



class SettingsWindow(toga.Window):
    def __init__(self, title, settings_elemente:Optional[List[SettingsElement]] = None, width=400, height=400):
        super().__init__(title, size=(width, height))

        self.settings_elemente = settings_elemente or []

        self.content = self.build()
       
    def build(self):
        # Hauptcontainer für den Inhalt erstellen
        box = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
        

        for elemnt in self.settings_elemente:
            box.add(elemnt.gui)

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

        for settings_element in self.settings_elemente:
            settings_element.save()
