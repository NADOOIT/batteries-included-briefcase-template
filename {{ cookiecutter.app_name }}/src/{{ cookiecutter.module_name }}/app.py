"""
{{ cookiecutter.description|escape_toml }}
"""
{% if cookiecutter.app_source %}
{{ cookiecutter.app_source }}
{% else %}

import os
import sys
import subprocess
from datetime import datetime

import toga
from toga.style.pack import COLUMN
from toga.style import Pack
from toga import Command, Group

from {{ cookiecutter.app_name|lower|replace('-', '_') }}.components.LicenseWindow import LicenseWindow
from {{ cookiecutter.app_name|lower|replace('-', '_') }}.components.UpdateWindow import UpdateWindow

from {{ cookiecutter.app_name|lower|replace('-', '_') }}.services import get_base_dir, open_file, get_help_file_path,update_in_updates_ordner_uebertragen
from screeninfo import get_monitors

class {{ cookiecutter.app_name|lower|replace('-', '_') }}(toga.App):
    
    # Define the action handlers for the commands
    def show_license(self, widget):
        # Instantiate the LicenseWindow
        license_window = LicenseWindow(title="Lizenzinformationen")

        # Show the license window
        license_window.show()
    
    def show_updates(self, *argv):
        # Instantiate the UpdateWindow
        update_window = UpdateWindow(title="Updateinformationen")

        # Show the update window
        update_window.show()

    def show_help(self, widget):
        help_file_path = get_help_file_path(self.app)
        if os.path.exists(help_file_path):
            open_file(help_file_path)
            
    def base_ordner_offnen(self, widget):
        # Retrieve the template folder path
        base_folder_path = get_base_dir()

        # Open the template folder in the system's file explorer
        if sys.platform == "win32":
            os.startfile(base_folder_path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", base_folder_path])
        else:  # 'linux', 'linux2', 'cygwin', 'os2', 'os2emx', 'riscos', 'atheos'
            subprocess.Popen(["xdg-open", base_folder_path])  
                  
    def aktualisierung_anzeigen(self):
        self.show_updates()
        
        def überprüfung_auf_erstausführung_nach_aktualisierung_oder_installation(self):
        #beim start ausführen
        update_daten = update_daten_laden_user()
        neues_update_wurde_installiert = update_daten.get("neues_update_wurde_installiert")
        if neues_update_wurde_installiert:
            return True
        else:
            return False

    def neues_update_existiert(self):
        updates_user = update_daten_laden_user()['Updates']
        update_keys_user = list(updates_user.keys())  # Extrahiere alle Schlüssel
        anzahl_update_user = len(update_keys_user)
        updates_app = update_daten_laden_app(self)['Updates']
        update_keys_app = list(updates_app.keys())  # Extrahiere alle Schlüssel
        anzahl_update_app = len(update_keys_app)
        if anzahl_update_app > anzahl_update_user:
            return True
        else:
            return False
        
    def startup(self):
    
        # Erstellen von Vorraussetung damit die App funktioniert.
        setup_folders()

        # Menü
        help_group = Group("Help", order=100)
        settings_group = Group("Settings", order=50)
        
        # Define commands
        license_command = Command(
            action=self.show_license,
            text="Lizenzinformationen",
            tooltip="Zeigt die Lizenzinformationen der verwendeten Pakete an",
            group=help_group,
        )
        open_help_file_command = Command(
            action=self.show_help,
            text="Hilfe öffnen",
            tooltip="Öffent die Hilfe PDF",
            group=help_group,
        )
        update_command = Command(
            action=self.show_updates,
            text="Updateinformationen",
            tooltip="Zeigt die Veränderung in der Software an",
            group=help_group,
        )
        basis_ordner_öffnen_command = Command(
            action=self.base_ordner_offnen,
            text="Basis Ordner öffnen",
            tooltip="Öffnet den Programmordner",
            group=settings_group,
        )
        
        # Menü
        help_group = Group("Help", order=100)
        settings_group = Group("Settings", order=50)
        
        # Define commands
        license_command = Command(
            action=self.show_license,
            text="Lizenzinformationen",
            tooltip="Zeigt die Lizenzinformationen der verwendeten Pakete an",
            group=help_group,
        )
        
        open_help_file_command = Command(
            action=self.show_help,
            text="Hilfe öffnen",
            tooltip="Öffent die Hilfe PDF",
            group=help_group,
        )
        
        update_command = Command(
            action=self.show_updates,
            text="Updateinformationen",
            tooltip="Zeigt die Veränderung in der Software an",
            group=help_group,
        )
        
        basis_ordner_öffnen_command = Command(
            action=self.base_ordner_offnen,
            text="Basis Ordner öffnen",
            tooltip="Öffnet den Programmordner",
            group=settings_group,
        )
        
        # Add commands to the app
        self.commands.add(
            license_command,
            open_help_file_command,
            basis_ordner_öffnen_command,
            update_command,
        ) 
        
        # Get the size of the primary monitor
        monitor = get_monitors()[0]
        screen_width, screen_height = monitor.width, monitor.height

        # Calculate half screen width and use full screen height
        half_screen_width = screen_width // 2

        # Main layout Box
        self.main_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding_left=30,
                padding_right=60,
                #width=half_screen_width * 0.95,
                flex=1,
            )
        )
        
        # ScrollContainer to allow infinite scrolling
        self.scroll_container = toga.ScrollContainer(
            content=self.main_box, style=Pack(direction=COLUMN, flex=1), vertical=True
        ) 
                self.main_window = toga.MainWindow(
            title=self.formal_name, size=(half_screen_width, screen_height * 80 / 100)
        )
        self.main_window.content = (
            self.scroll_container
        )  # Set the ScrollContainer as the main content

        # Set the window position to the right side of the screen
        self.main_window.position = (half_screen_width, 0)

        self.main_window.show()
        
        if not os.path.isfile(get_updates_datei_user()) or self.neues_update_existiert():
            update_in_updates_ordner_uebertragen(self.app)
            self.aktualisierung_anzeigen()
            
    def main(self):
        pass

    def exit(self):
        pass


def main():
    return {{ cookiecutter.app_name|lower|replace('-', '_') }}()

{% endif %}
