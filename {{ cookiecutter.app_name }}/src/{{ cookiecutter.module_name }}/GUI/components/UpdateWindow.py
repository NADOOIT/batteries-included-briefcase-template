import json
import os
import shutil

import toga
from toga.style import Pack
from toga.style.pack import COLUMN

from {{ cookiecutter.app_name|lower|replace('-', '_') }}.services import get_updates_datei_user, get_updates_pdf_path, open_file, update_daten_laden_user, update_in_updates_ordner_uebertragen
from {{ cookiecutter.app_name|lower|replace('-', '_') }}.CONSTANTS import UPDATE_ORDNER_NAME_APP, UPDATE_ORDNER_NAME_USER
from {{ cookiecutter.app_name|lower|replace('-', '_') }}.utils import ensure_folder_exists
from {{ cookiecutter.app_name|lower|replace('-', '_') }}.styling import StandardStyling


class UpdateWindow(toga.Window):
    def __init__(self, title, size=(400, 400)):
        super().__init__(title, size=size)
        self.update_keys = []
        self.current_update_index = 0
        self.content = self.build()
        self.update_keys_berechnen()
        self.daten_in_felder_übertragen()

    def build(self):
        box = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
        self.patchnotes_inhalt = toga.MultilineTextInput(style=Pack(padding_bottom=10, height=100, flex=1), readonly=True)
        box.add(self.patchnotes_inhalt)
        pdf_oeffnen_button = toga.Button('Patchnote-PDF öffnen', style=StandardStyling.standard_button_style(), on_press=self.open_update_pdf)
        box.add(pdf_oeffnen_button)
        vorheriges_update_button = toga.Button('Vorheriges Update', style=StandardStyling.standard_button_style(), on_press=self.vorheriges_update)
        box.add(vorheriges_update_button)
        nächstes_update_button = toga.Button('Nächstes Update', style=StandardStyling.standard_button_style(), on_press=self.nächstes_update)
        box.add(nächstes_update_button)
        fenster_schliessen_button = toga.Button('Fenster schließen', style=StandardStyling.standard_button_style(), on_press=self.fenster_schließen)
        box.add(fenster_schliessen_button)

        return box

    

    
    def update_keys_berechnen(self):
        updates = update_daten_laden_user()['Updates']
        self.update_keys = list(updates.keys())  # Extrahiere alle Schlüssel
        self.current_update_index = len(self.update_keys) - 1

    def daten_in_felder_übertragen(self):
        if self.update_keys:
            update_id = self.update_keys[self.current_update_index]
            if update_id == "template":  # Überspringe das Template-Update
                return
            update_data = update_daten_laden_user()
            changes_data = update_data['Updates'][update_id]['changes']
            
            formatted_changes = "Bugfixes:\n- " + "\n- ".join(changes_data['bugfixes']) + "\n\n"
            formatted_changes += "Features:\n- " + "\n- ".join(changes_data['features']) + "\n\n"
            formatted_changes += "General Updates:\n- " + "\n- ".join(changes_data['general_updates'])
            
            self.patchnotes_inhalt.value = formatted_changes


    def nächstes_update(self, widget):
        if self.current_update_index < len(self.update_keys) - 1:
            self.current_update_index += 1
            self.daten_in_felder_übertragen()

    def vorheriges_update(self, widget):
        if self.current_update_index > 0:
            self.current_update_index -= 1
            self.daten_in_felder_übertragen()

    def open_update_pdf(self, widget):
        update_file_path = get_updates_pdf_path(self.app)
        if os.path.exists(update_file_path):
            open_file(update_file_path)

    def fenster_schließen(self, widget):
        self.close()
