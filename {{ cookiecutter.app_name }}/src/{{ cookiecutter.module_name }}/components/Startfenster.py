from __future__ import annotations
import datetime
import re
from time import sleep
from typing import TYPE_CHECKING, List
from openpyxl import load_workbook
import openpyxl

import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from toga.widgets.multilinetextinput import MultilineTextInput

from {{ cookiecutter.app_name|lower|replace('-', '_') }}.services import finde_letzte_zeile_in_excel_blatt, lade_daten_aus_excel_blatt_als_DataFrame, loesche_alle_daten_von_blatt, open_file, uebertrage_daten_in_excel_blatt
from {{ cookiecutter.app_name|lower|replace('-', '_') }}.utils import translate_date_to_german
from {{ cookiecutter.app_name|lower|replace('-', '_') }}.styling import StandardStyling

from {{ cookiecutter.app_name|lower|replace('-', '_') }}.components.Fehlermeldung import Fehlermeldung

if TYPE_CHECKING:
    from {{ cookiecutter.app_name|lower|replace('-', '_') }}.app import {{ cookiecutter.app_name|lower|replace('-', '_') }}
import os
import shutil
import io
import sys


class GUIOutputStream(io.StringIO):
    def __init__(self, console_output):
        super().__init__()
        self.console_output = console_output

    def write(self, text):
        self.console_output.value += text
        sys.__stdout__.write(text)

class Startfenster(toga.Box):
    def __init__(
        self,
        app: {{ cookiecutter.app_name|lower|replace('-', '_') }},
        id: str | None = None,
        start_values: dict | None = None
    ):
        style = Pack(direction=COLUMN)
        super().__init__(id=id, style=style)
        self.app = app

        self.standardeingabe_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        
        self.console_output = MultilineTextInput(id=id, style=Pack(flex=1), readonly=True)
        
        self.standardeingabe_box.excelDatei = toga.MultilineTextInput(
            placeholder="Excel Datei hier ablegen",
            style=StandardStyling.standard_input_style(),
        )
        self.standardeingabe_box.add(self.standardeingabe_box.excelDatei)

        #self.standardeingabe_box.dateiname = toga.TextInput(style=StandardStyling.standard_input_style())
        #self.standardeingabe_box.add(self.standardeingabe_box.dateiname)
        
        """ 
        start_values = {
            "excelDatei": "/Users/christophbackhaus/Documents/GitHub/NADOO-Telemarketing/Testdatei.xlsx",
            "dateiname": "test",
        }
        """

        if start_values is not None:
            self.setup_input_fields(start_values)




        
        
        
        self.next_button = toga.Button(
            "Nächster Schritt",
            on_press=self.next_step,
            style=StandardStyling.standard_button_style(),
        )

        self.gui_output = GUIOutputStream(self.console_output)
        sys.stdout = self.gui_output

        self.add(self.console_output)


        self.add(self.standardeingabe_box)
        self.add(self.next_button)
        
        #self.next_step(self)

    
    def setup_input_fields(self, start_values):
        self.standardeingabe_box.excelDatei.value = start_values["excelDatei"]

    def next_step(self, widget=None):

        try:
            
            print("STUFF")

        # Erzeuge einen Fake Fehler um das Fehlerfenster zu testen
        # raise ValueError("Dies ist eine Fake-Fehlermeldung.")  
        
        
        except Exception as e:
            print(f"Fehler beim Verarbeiten der Datei: {str(e)}")
            fehlermeldung = Fehlermeldung(
                            self.app,
                            retry_function=lambda: self.next_step(),
                            fehlermeldung=e,
                        )
            self.fehlermeldung_widget = fehlermeldung
            self.standardeingabe_box.add(self.fehlermeldung_widget)
        finally:
            # Lösche die Datei mit den Daten, die in die temporäre Datei geschrieben wurden
            dateipfade_der_zu_loeschenden_datei = self.pfad_zur_temp_datei_in_ordner_mit_zugriffrechten
            
            try:
                os.remove(dateipfade_der_zu_loeschenden_datei)
                print(f"Die temporäre Datei '{dateipfade_der_zu_loeschenden_datei}' wurde erfolgreich gelöscht.")
            except FileNotFoundError:
                print(f"Die temporäre Datei '{dateipfade_der_zu_loeschenden_datei}' konnte nicht gefunden werden.")
            except PermissionError:
                print(f"Keine ausreichenden Berechtigungen zum Löschen der temporären Datei '{dateipfade_der_zu_loeschenden_datei}'.")
            except Exception as e:
                print(f"Ein unerwarteter Fehler ist beim Löschen der temporären Datei aufgetreten: {str(e)}")