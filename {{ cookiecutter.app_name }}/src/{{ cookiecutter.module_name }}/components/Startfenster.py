from __future__ import annotations
import datetime
import re
from time import sleep
from typing import TYPE_CHECKING, List


import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from toga.widgets.multilinetextinput import MultilineTextInput

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
        
        self.excelDatei = toga.MultilineTextInput(
            placeholder="Excel Datei hier ablegen",
            style=StandardStyling.standard_input_style(),
        )
        self.standardeingabe_box.add(self.excelDatei)

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
        self.excelDatei.value = start_values["excelDatei"]

    def next_step(self, widget=None):

        try:
            
            print("STUFF")

        # Erzeuge einen Fake Fehler um das Fehlerfenster zu testen
        # raise ValueError("Dies ist eine Fake-Fehlermeldung.")  
        
        
        except Exception as e:
            print(f"Fehler: {str(e)}")
            fehlermeldung = Fehlermeldung(
                            self.app,
                            retry_function=lambda: self.next_step(),
                            fehlermeldung=e,
                        )
            self.fehlermeldung_widget = fehlermeldung
            self.standardeingabe_box.add(self.fehlermeldung_widget)
        finally:
            
            pass
        
            try:
                print("Aufräumen was bei einem Fehler mit dem Programm über ist")
            except Exception as e:
                print(f"EFehler der dabei möglicherweise aufgetreten ist: {str(e)}")