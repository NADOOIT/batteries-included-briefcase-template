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

import pandas as pd
from openpyxl.worksheet.worksheet import Worksheet
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


def create_test_run_copy(file_path):
    # Pfad zum "Testlauf" Ordner in "~/Library/Containers/com.microsoft.Excel/Data" erstellen
    test_run_folder = os.path.expanduser("~/Library/Containers/com.microsoft.Excel/Data/Testlauf")
    
    # Überprüfen, ob der "Testlauf" Ordner bereits existiert, ansonsten erstellen
    if not os.path.exists(test_run_folder):
        os.makedirs(test_run_folder)
    
    # Dateiname und Erweiterung der Exceldatei extrahieren
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))
    
    # Überprüfen, ob bereits Testlauf Dateien existieren
    test_run_files = [f for f in os.listdir(test_run_folder) if f.startswith("Testlauf_")]
    
    if test_run_files:
        # Letzte Testlauf Datei finden und Nummer extrahieren
        last_test_run_file = max(test_run_files)
        last_test_run_number = int(last_test_run_file.split("_")[1].split(".")[0])
        
        # Neue Testlauf Nummer generieren
        new_test_run_number = last_test_run_number + 1
    else:
        # Wenn keine Testlauf Dateien existieren, mit Nummer 001 beginnen
        new_test_run_number = 1
    
    # Neuen Dateinamen für den Testlauf erstellen
    new_test_run_file_name = f"Testlauf_{new_test_run_number:03d}{file_extension}"
    
    # Pfad zur neuen Testlauf Datei erstellen
    new_test_run_file_path = os.path.join(test_run_folder, new_test_run_file_name)
    
    # Kopie der Exceldatei im "Testlauf" Ordner erstellen
    shutil.copy2(file_path, new_test_run_file_path)
    
    return new_test_run_file_path


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



        self.datei_auswaehlen_button = toga.Button(
            "Datei auswählen",
            on_press=self.datei_auswaehlen,
            style=StandardStyling.standard_button_style(),
        )
        
        
        
        self.next_button = toga.Button(
            "Datei verarbeiten",
            on_press=self.next_step,
            style=StandardStyling.standard_button_style(),
        )

        self.gui_output = GUIOutputStream(self.console_output)
        sys.stdout = self.gui_output
        self.add(self.console_output)
        self.add(self.standardeingabe_box)
        self.add(self.datei_auswaehlen_button)
        self.add(self.next_button)
        
        #self.next_step(self)
        
    async def datei_auswaehlen(self, widget):
        dateipfad = await self.app.main_window.open_file_dialog(
            title="Datei auswählen",
        )
        if dateipfad is not None:
            self.standardeingabe_box.excelDatei.value = dateipfad

    
    def setup_input_fields(self, start_values):
        self.standardeingabe_box.excelDatei.value = start_values["excelDatei"]

    def next_step(self, widget=None):
        file_path = self.standardeingabe_box.excelDatei.value
        print(file_path)
        try:
            


            # um iterativ arbeiten zu können aber die Vorlage nicht zu ändern werden wir zunächst eine kopie der Excepliste anfertigen
            # Der Name ist "Testlauf_001" wobei die Nummer der Datei inkrementiert wird
            # Die Datei werden im Ordner "Testlauf" abgelegt, der neben der Exceldatei im Projektordner platziert ist
            # Überprüfe das Verzeichnis auf bereits existierende Testlauf Datein, teile den Namen auf, und erzeuge den neuen Namen
            
            pfad_zur_temp_datei_in_ordner_mit_zugriffrechten = create_test_run_copy(file_path)
            print(pfad_zur_temp_datei_in_ordner_mit_zugriffrechten)


            wb = load_workbook(pfad_zur_temp_datei_in_ordner_mit_zugriffrechten)

            print(wb.sheetnames)
            print(wb.worksheets[0].title)
            print(wb.worksheets[0].cell(row=1, column=1).value)

            # Get the first sheet in the workbook
            #print(wb.sheet_names)

            # Die Excel Datei hat mehrere Blätter 
            # Bsp. 'Statuskürzel', 'freie Termine', 'WV März 2024', 'WV April 2024', 
            # 'WV Folgemonate', 'NICHT erreichbar', 'KI D etc', 'Mails', 'Termine', 'Auffüller'
            
            # WV steht für Wiedervorlage
            # Diese Blätter haben die folgenden Spalten:
            # 'Stadt', 'Associated Company', 'Vorname Ansprechpartner', 'Name Ansprechpartner', 'Position / Titel',
            # 'Straße Hausnr.', 'PLZ', 'Ort ', 'Bundesland', 'Webseite', 'E-Mail', 'Ansprechpartner AP', 'E-Mail AP',
            # 'Telefon primär', 'Telefon Zentrale', 'Telefon Mobil', 'Bemerkung (Kontakt besteht, Kaltakquise etc.)',
            # 'Gesprächsnotiz TM ', 'WV Datum', 'Status'
            
            # Was mit den Datenreihen passieren soll wird bestimmt durch WV Datum und Status
            """
            Status	Bedeutung	                                kopieren	verschieben	                                ins Tabellenblatt	                verbleibt in oder wird verschoben
            Info	Bitte Infos per E-Mail versenden	        ja, bei WV	ja, bei Selbstmelder oder WV Folgemonate	Mails (alle); WV, WV Folgemonate	Mails (alle); Selbstmelder oder WV
            S	    Selbstmelder	                            nein	    ja	                                        WV Folgemonate	                    nach Zeitspanne X in WV
            D	    Doppelte Adresse	                        nein	    ja	                                        KI KK D etc	                        KI KK D etc
            KI	    Kein Interesse	                            nein	    ja	                                        KI KK D etc	                        KI KK D etc
            KK	    Kein Kontakt möglich, nicht erreichbar	    nein	    ja	                                        KI KK D etc	                        KI KK D etc
            T	    Termin	                                    nein	    ja	                                        Termine	                            Termine
            
            TS	    Terminstorno	                            nein	    ja	                                        Termine	                            je nach Fall in Termine oder WV
            TV	    Terminverlegung, in Bearbeitung	            nein	    ja	                                        WV	                                WV, dann wieder Termine
            WA	    Wiederanruf	                                nein	    nein		                                WV
            WAI	    Wiederanruf, Infomail verschickt	        nein	    nein		                                WV
            WV	    Wiedervorlage Monat x	                    nein	    ja	                                        WV Folgemonate	                    WV Folgemonate
            WVI	    Wiedervorlage Monat x, Infomail verschickt	nein	    ja	                                        WV Folgemonate	                    WV Folgemonate
            ES	    Entscheider-Sekretärin				
            FA	    falscher Ansprechpartner				
            KL	    keine Leitungsposition hinterlegt				
            R	    Registrierung für Testphase				
            """
                    
            # Finde das Blatt mit dem aktuellen Monat
            
            aktuelles_monat_blatt:Worksheet = None
            Excel_Blatt_WV_Folgemonate:Worksheet = None
            Excel_Blatt_Mails:Worksheet = None
            Excel_Blatt_KI_D_etc:Worksheet = None
            Excel_Blatt_NICHT_erreichbar:Worksheet = None
            Excel_Blatt_Termine:Worksheet = None
                            
            aktueller_monat_deutsch = "März"
            #print(f"Aktueller Monat: {aktueller_monat_deutsch}")
            
            for blatt in wb.worksheets:
                blatt: Worksheet
                
                #print(blatt.title)
                
                if aktueller_monat_deutsch in blatt.title:
                    aktuelles_monat_blatt = blatt
                    
                if "WV Folgemonate" in blatt.title or "WV Folgemonate" == blatt.title:
                    Excel_Blatt_WV_Folgemonate = blatt
                    
                if "Mails" in blatt.title or "Mails" == blatt.title:
                    Excel_Blatt_Mails = blatt
                    
                if "KI D etc" in blatt.title or "KI D etc" == blatt.title:
                    Excel_Blatt_KI_D_etc = blatt
                    
                if "NICHT erreichbar" in blatt.title or "NICHT erreichbar" == blatt.title:
                    Excel_Blatt_NICHT_erreichbar = blatt
                    
                if "Termine" in blatt.title or "Termine" == blatt.title:
                    Excel_Blatt_Termine = blatt
                    
            
            print(f"Akuelles Monatsblatt: {aktuelles_monat_blatt.title}")
            print(f"Folge Monatsblatt: {Excel_Blatt_WV_Folgemonate.title}")

            
            # Finde die Spaltenbezeichner (A1, B1, C1 ...) mit den Namen Gesprächsnotiz TM, WV Datum und Status
            spaltenbezeichner_gesprächsnotiz_tm = None
            spaltenbezeichner_wv_datum = None
            spaltenbezeichner_status = None

            # Entferne Leerzeichen am Ende der Spaltenüberschriften
            for spalte in aktuelles_monat_blatt.columns:
                #print(f"Spalte: {spalte}")
                #print(f"Spalte[0]: {spalte[0]}")
                print(f"Spalte[0].value: {spalte[0].value}")
                
                if spalte[0].value is not None:
                    spalte[0].value = spalte[0].value.strip()
                else:       
                    break
            # Finde die Spaltenbezeichner basierend auf den bereinigten Spaltenüberschriften
            for spalte in aktuelles_monat_blatt.columns:
                if spalte[0].value == "Gesprächsnotiz TM":
                    spaltenbezeichner_gesprächsnotiz_tm = spalte
                elif spalte[0].value == "WV Datum":
                    spaltenbezeichner_wv_datum = spalte
                elif spalte[0].value == "Status":
                    spaltenbezeichner_status = spalte
                    break
            #print(f"Gesprächsnotiz TM: {spaltenbezeichner_gesprächsnotiz_tm}")
            #print(f"WV Datum: {spaltenbezeichner_wv_datum}")
            #print(f"Status: {spaltenbezeichner_status}")

            
            #print(f"Gesprächsnotiz Tm: {spaltenbezeichner_gesprächsnotiz_tm}")
            #print(f"WV Datum: {spaltenbezeichner_wv_datum}")
            #print(f"Status: {spaltenbezeichner_status}")
            
            # Da noch unklar ist in welcher spalte alle zeilen einen Wert haben suchen wir den höchsten.
            # Dadurch wir die letzte Zeile
            # Der Weg ist, dass wir in spalte 1 anfangen bis zur letzten gefüllten Zeile zu springen
            # Die Anzahl der reihen wird gespeichert
            # danach wird die selbe Anzahl von Reihen bei allen Spalten die bis Status vorhanden sind durchgeführt
            # Hierbei gehen wir wieder von links nach rechts und speichern den höchsten Wert
            # Wichtig ist aber das wir sollten in den späteren Spalten nicht mehr Zeilen haben als in der ersten
            # Werden dennoch weitere Reihen geprüft. Ist in allen Spalten in der gefundenen Reihe kein Wert ist anzunehmen, dass es die letzte Reihe war
            # So wird verhindert, dass ein einzelner fehlender Wert die überprüfung stoppt
            # Es wird also geprüft ob in allen Spalten einer Reihe None ist und wenn ja war die vorherige die letzte
            

                
            """                        
            max_rows_aktueller_monat_blatt = finde_letzte_zeile_in_excel_blatt(aktuelles_monat_blatt)

            # Jetzt da wir wissen wo die Tabelle liegt ist es Zeit die Daten zu laden und dann im Speicher zu verarbeiten.
            # Lade die Daten aus dem aktuellen Monatsblatt in ein DataFrame
            Tabelle_mit_allen_Daten_von_Excel_Blatt_Aktueller_Monat = aktuelles_monat_blatt.range((1, 1), 
                                                                                                (max_rows_aktueller_monat_blatt, spaltenbezeichner_status.column)).options(pd.DataFrame).value
            Dataframe_aller_Daten_vom_aktuellen_Monat = pd.DataFrame(Tabelle_mit_allen_Daten_von_Excel_Blatt_Aktueller_Monat[1:],
                                                                    columns=Tabelle_mit_allen_Daten_von_Excel_Blatt_Aktueller_Monat.columns)

            """
            Dataframe_aller_Daten_vom_aktuellen_Monat = lade_daten_aus_excel_blatt_als_DataFrame(aktuelles_monat_blatt)
            
            Dataframe_aller_Daten_vom_aktuellen_Monat.reset_index(drop=False, inplace=True)
            
            #print(Dataframe_aller_Daten_vom_aktuellen_Monat)
                            
            # -------------------------------- Datenbereinigung --------------------------------#
           
            def korrigiere_tippfehler(text):
                text = str(text)  # Konvertiere den Wert in eine Zeichenkette
                text = text.replace('Selbmelder', 'Selbstmelder')
                # Füge hier weitere häufige Tippfehler und ihre Korrekturen hinzu
                return text

            # Korrigiere Tippfehler in der Spalte 'Status'
            Dataframe_aller_Daten_vom_aktuellen_Monat['Status'] = Dataframe_aller_Daten_vom_aktuellen_Monat['Status'].apply(korrigiere_tippfehler)

            # Ersetze fehlende Werte in der Spalte 'Status' durch einen leeren String
            Dataframe_aller_Daten_vom_aktuellen_Monat['Status'] = Dataframe_aller_Daten_vom_aktuellen_Monat['Status'].fillna('')

            # Ersetze fehlende Werte in der Spalte 'Gesprächsnotiz TM' durch einen leeren String
            Dataframe_aller_Daten_vom_aktuellen_Monat['Gesprächsnotiz TM'] = Dataframe_aller_Daten_vom_aktuellen_Monat['Gesprächsnotiz TM'].fillna('')
            
            print(Dataframe_aller_Daten_vom_aktuellen_Monat)
            # ----------------------------------------------------------------------------------- #                

            # Erfasse Datensätze mit Bezug zu Infomail und Selbstmelder
            status_info = Dataframe_aller_Daten_vom_aktuellen_Monat[Dataframe_aller_Daten_vom_aktuellen_Monat['Status'] == 'Info']

            # Übertrage die Daten aus dem DataFrame in das Excel Blatt
            uebertrage_daten_in_excel_blatt(Excel_Blatt_Mails, status_info)           

            # Passe den Status der übertragenen Positionen mit dem Wert 'Info' auf 'WAI' an
            status_info.loc[status_info['Status'] == 'Info', 'Status'] = 'WAI'

            # Aktualisiere die Werte in Dataframe_aller_Daten_vom_aktuellen_Monat basierend auf den Indexwerten von status_info
            for index, row in status_info.iterrows():
                Dataframe_aller_Daten_vom_aktuellen_Monat.loc[index, 'Status'] = row['Status']

            #print(Dataframe_aller_Daten_vom_aktuellen_Monat)
            
            # ----------------------------------------------------------------------------------- #    
            # Erfasse Datensätze mit Bezug zu Infomail und Selbstmelder. Ein Beispielstatus wäre hier Info / Selbstmelder
            status_s = Dataframe_aller_Daten_vom_aktuellen_Monat[
                                                                    Dataframe_aller_Daten_vom_aktuellen_Monat['Status'].str.contains('Info') &
                                                                    Dataframe_aller_Daten_vom_aktuellen_Monat['Status'].str.contains('Selbstmelder')
                                                                ]

            print(status_s)
            
            # Übertrage die Daten aus dem DataFrame in das Excel Blatt
            print("Übertrage Daten in Excel Blatt Mails")
            uebertrage_daten_in_excel_blatt(Excel_Blatt_Mails, status_s)
            print("Übertrage Daten in Excel Blatt WV Folgemonate")
            uebertrage_daten_in_excel_blatt(Excel_Blatt_WV_Folgemonate, status_s)

            
            
            # Entferne die Zeilen aus dem Ursprungsdataframe
            print("Entferne Zeilen aus Dataframe_aller_Daten_vom_aktuellen_Monat")
            Dataframe_aller_Daten_vom_aktuellen_Monat.drop(status_s.index, inplace=True)

            print(Dataframe_aller_Daten_vom_aktuellen_Monat)
            
            # ----------------------------------------------------------------------------------- #   
            status_values = ['D', 'KI', 'KK']
            status_result = Dataframe_aller_Daten_vom_aktuellen_Monat[Dataframe_aller_Daten_vom_aktuellen_Monat['Status'].isin(status_values)]
            uebertrage_daten_in_excel_blatt(Excel_Blatt_KI_D_etc, status_result)
            print("Nach Übertragung und vor Entfernen:")
            print(Dataframe_aller_Daten_vom_aktuellen_Monat)
            
            Dataframe_aller_Daten_vom_aktuellen_Monat.drop(status_result.index, inplace=True)

            print("Nach Entfernen:")
            print(Dataframe_aller_Daten_vom_aktuellen_Monat)
            
            # ----------------------------------------------------------------------------------- #   
            
            status_values = ['nicht erreichbar']
            status_result = Dataframe_aller_Daten_vom_aktuellen_Monat[Dataframe_aller_Daten_vom_aktuellen_Monat['Status'].isin(status_values)]
            uebertrage_daten_in_excel_blatt(Excel_Blatt_NICHT_erreichbar, status_result)
            print("Nach Übertragung und vor Entfernen:")
            print(Dataframe_aller_Daten_vom_aktuellen_Monat)
            
            Dataframe_aller_Daten_vom_aktuellen_Monat.drop(status_result.index, inplace=True)

            print("Nach Entfernen:")
            print(Dataframe_aller_Daten_vom_aktuellen_Monat)
            
            # ----------------------------------------------------------------------------------- #   
                            

            status_result = Dataframe_aller_Daten_vom_aktuellen_Monat[
                Dataframe_aller_Daten_vom_aktuellen_Monat['Status'].str.contains(r'^(?:T|Telefontermin) am \d{2}\.\d{2}\.\d{4}(?: um \d{2}:\d{2})?', regex=True)
            ]
            uebertrage_daten_in_excel_blatt(Excel_Blatt_Termine, status_result)
            print("Nach Übertragung und vor Entfernen:")
            print(Dataframe_aller_Daten_vom_aktuellen_Monat)

            Dataframe_aller_Daten_vom_aktuellen_Monat.drop(status_result.index, inplace=True)

            print("Nach Entfernen:")
            print(Dataframe_aller_Daten_vom_aktuellen_Monat)
            # ----------------------------------------------------------------------------------- #   

            Dataframe_aller_Daten_vom_aktuellen_Monat['WV Datum'] = pd.to_datetime(Dataframe_aller_Daten_vom_aktuellen_Monat['WV Datum'])
            Dataframe_aller_Daten_vom_aktuellen_Monat.sort_values(by='WV Datum', ascending=True, na_position='first', inplace=True)

            print(Dataframe_aller_Daten_vom_aktuellen_Monat)

            
            
            
            

            
            status_wa = Dataframe_aller_Daten_vom_aktuellen_Monat[Dataframe_aller_Daten_vom_aktuellen_Monat['Status'] == 'WA']
            status_ts = Dataframe_aller_Daten_vom_aktuellen_Monat[Dataframe_aller_Daten_vom_aktuellen_Monat['Status'] == 'TS']
            status_tv = Dataframe_aller_Daten_vom_aktuellen_Monat[Dataframe_aller_Daten_vom_aktuellen_Monat['Status'] == 'TV']
            status_wai = Dataframe_aller_Daten_vom_aktuellen_Monat[Dataframe_aller_Daten_vom_aktuellen_Monat['Status'] == 'WAI']
            status_wv = Dataframe_aller_Daten_vom_aktuellen_Monat[Dataframe_aller_Daten_vom_aktuellen_Monat['Status'] == 'WV']
            status_wvi = Dataframe_aller_Daten_vom_aktuellen_Monat[Dataframe_aller_Daten_vom_aktuellen_Monat['Status'] == 'WVI']


            
            loesche_alle_daten_von_blatt(aktuelles_monat_blatt)
            
            
            
            # füge die nun bereinigte und geordnete Liste wieder ein
            # Füge die bereinigten und geordneten DataFrames wieder in das Excel-Blatt ein
            uebertrage_daten_in_excel_blatt(aktuelles_monat_blatt, Dataframe_aller_Daten_vom_aktuellen_Monat)
            
                    
                

            # Die Blätter mit der Bezeichnung WV beinhalten die Daten der Telefonisten
            # Die Datensätze werden wie folgt verteilt:
            # Die Datensätze von WV März usw. werden überprüft.

            # Get the first 10 rows and columns of the sheet
            #Tabelle_mit_allen_Daten_von_Excel_Blatt_Aktueller_Monat = sheet.range("A1:T1").value
            
            
            #print(Tabelle_mit_allen_Daten_von_Excel_Blatt_Aktueller_Monat)
        
                                        
            # Pfad der Quelldatei
            quelldatei = self.standardeingabe_box.excelDatei.value

            print(f"Die Quelldatei ist {quelldatei}")

            # Überprüfe, ob die Quelldatei existiert
            if not os.path.exists(quelldatei):
                print(f"Die Quelldatei {quelldatei} existiert nicht.")
            else:
                # Pfad und Name der Zieldatei
                zielordner = os.path.dirname(quelldatei)
                print(f"Der Zielordner ist {zielordner}")
                print(f"Der Dateiname ist {pfad_zur_temp_datei_in_ordner_mit_zugriffrechten}")

                # Trenne Dateiname und Erweiterung
                dateiname, erweiterung = os.path.splitext(os.path.basename(quelldatei))

                # Füge "_ueberarbeitet" zum Dateinamen hinzu
                neuer_dateiname = f"{dateiname}_ueberarbeitet{erweiterung}"

                zieldatei = os.path.join(zielordner, neuer_dateiname)

                # Überprüfe, ob die Zieldatei bereits existiert
                if os.path.exists(zieldatei):
                    # Wenn die Zieldatei bereits existiert, füge eine fortlaufende Nummer hinzu
                    i = 1
                    while True:
                        neuer_dateiname = f"{dateiname}_ueberarbeitet_{i}{erweiterung}"
                        zieldatei = os.path.join(zielordner, neuer_dateiname)
                        if not os.path.exists(zieldatei):
                            break
                        i += 1

                print(f"Die Zieldatei ist {zieldatei}")

                # Überprüfe, ob die Datei pfad_zur_temp_datei_in_ordner_mit_zugriffrechten im aktuellen Verzeichnis existiert
                if not os.path.exists(pfad_zur_temp_datei_in_ordner_mit_zugriffrechten):
                    print(f"Die Datei {pfad_zur_temp_datei_in_ordner_mit_zugriffrechten} existiert nicht im aktuellen Verzeichnis.")
                else:
                    try:
                        # Änderungen speichern
                        wb.save(pfad_zur_temp_datei_in_ordner_mit_zugriffrechten)
                        wb.close()
                        self.zieldatei = zieldatei
                        # Button zum Öffnen der neuen Excel-Datei
                        open_file_button = toga.Button("Neue Excel-Datei öffnen", on_press=lambda btn: open_file(self.zieldatei))
                        self.add(open_file_button)
                        
                        shutil.move(pfad_zur_temp_datei_in_ordner_mit_zugriffrechten, zieldatei)
                        print(f"Die Datei {pfad_zur_temp_datei_in_ordner_mit_zugriffrechten} wurde erfolgreich nach {zieldatei} verschoben.")
                    except Exception as e:
                        print(f"Fehler beim Verschieben der Datei: {str(e)}")
            
        except Exception as e:
            print(f"Fehler beim Verarbeiten der Datei: {str(e)}")
            fehlermeldung_componente = Fehlermeldung(self,fehlermeldung=e)
            self.add(fehlermeldung_componente)