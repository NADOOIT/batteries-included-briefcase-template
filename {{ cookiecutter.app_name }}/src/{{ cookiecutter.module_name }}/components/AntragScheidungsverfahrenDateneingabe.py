from __future__ import annotations
from typing import List, TYPE_CHECKING
import os
import shutil
from uuid import uuid4

import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from datetime import datetime

from nadoo_law.services import (
    add_ausfuehrung,
    datenabfrage_datev_for_aktenzeichen,
    get_beweismittel_data_scheidung,
    get_lawyer_data,
    hinzufuegen_anwaltsdaten_zum_kontext,
    set_beweismittel_data_Scheidung,
    get_mandanten_folder
)
from nadoo_law.components.AntragDateiManager import AntragDateiManager
from nadoo_law.components.Fehlermeldung import Fehlermeldung
from nadoo_law.components.AntragVorlageDatenVerarbeitung import (
    AntragVorlageDatenVerarbeitung,
)
from nadoo_law.styling import StandardStyling


if TYPE_CHECKING:
    from nadoo_law.app import NadooLaw


class AntragScheidungsverfahrenDateneingabe(toga.Box):
    name_der_template_datei = "MUSTER_SCHEIDUNG.docx"
    formular_name = "Scheidungsverfahren"
    kategorie = "Familienrecht"
    kundenprogramm_ID = "03a547bd-2ae9-4c86-8ebf-2d881da11b8f"

    def __init__(
        self,
        app: NadooLaw,
        id: str | None = None,
        lawyer_details=None,
    ):
        style = Pack(direction=COLUMN)
        super().__init__(id=id, style=style)
        self.app = app
        
        self.lawyer_details = lawyer_details or {}

        # Initialize the fehlermeldung_widget and antrag_manager_widget attributes
        self.fehlermeldung_widget = None
        self.antrag_manager_widget = None

        self.standardeingabe_box = toga.Box(style=Pack(direction=COLUMN, flex= 1))
        self.umstaende_box = toga.Box(style=Pack(direction=COLUMN, flex= 1))
        self.kinder_box = Kindereingabe()

        """ 
        self.beweismittel_box = toga.Box(style=Pack(direction=COLUMN, padding=padding_value))
        self.beweismittel_edit_box = toga.Box(
            style=Pack(direction=COLUMN, padding=padding_value)
        )
        """

        self.footer_box = toga.Box(style=Pack(direction=COLUMN, flex= 1))
        self.setup_input_fields(lawyer_details)
        self.create_umstaende_section()
        # self.create_beweismittel_section()

        self.create_application_button = toga.Button(
            "Antrag erstellen",
            on_press=self.create_application,
            style=StandardStyling.standard_button_style(),
        )
        self.footer_box.add(self.create_application_button)

        self.add(self.standardeingabe_box)
        self.add(toga.Divider())
        self.add(toga.Label("Kindersektion", style=StandardStyling.standard_label_style()))
        self.add(self.kinder_box)
        self.add(toga.Divider())
        self.add(self.umstaende_box)
        # self.add(self.beweismittel_box)  # This will be switched with beweismittel_edit_box when editing
        self.add(self.footer_box)

        # HIER DEAKTIVIEREN ODER AKTIVIEREN UM TESTDATEN ZU LADEN
        #self.alle_formular_elemente_mit_test_daten_fuellen()

    def alle_formular_elemente_mit_test_daten_fuellen(self):
        """
        Diese Funktion füllt alle Formularfelder mit Testdaten auf.
        """
        # Testdaten
        test_daten = {
            "COURT_NAME": "Kreis Musterstadt",
            "COURT_DEPARTMENT": "Straßenverkehrsamt",
            "COURT_ADDRESS": "Musterstraße 5",
            "COURT_ZIP_CITY": "99999 Musterstadt",
            "LAWYER_NAME": "Sebastian Kutzner",
            "LAWYER_EMAIL": "sebastian.kutzner@procivis.koeln",
            "LAWYER_PHONE": "+49 (221) 99898-179",
            "LAWYER_FAX": "+49 (221) 99898-499",
            "LAWYER_CONTACT_DATE": "01. Januar 2024",
            "LAWYER_REF": "000001-23",
            "PROCEDURE_VALUE": "12.000,00",
            "APPLICANT_NAME": "Max Mustermann",
            "APPLICANT_GENDER": "Herr",
            "APPLICANT_BIRTH_DATE": "01.01.1975",
            "APPLICANT_BIRTH_NAME": None,
            "APPLICANT_ADDRESS": "Musterstraße 1, 99999 Musterstadt",
            "MARRIAGE_DATE": "01.01.2000",
            "MARRIAGE_LOCATION": "Musterstadt",
            "REGISTRATION_NUMBER": "E 11/2000",
            "MARRIAGE_OFFICE": "Standesamt in Musterstadt",
            "RESPONDENT_NAME": "Erika Mustermann",
            "RESPONDENT_GENDER": "Frau",
            "RESPONDENT_BIRTH_DATE": "12.08.1964",
            "RESPONDENT_BIRTH_NAME": "Musterfrau",
            "RESPONDENT_ADDRESS": "Musterstraße 1, 99999 Musterstadt",
            "SEPARATION_DATE": "01.01.2023",
            "AUSGEZOGEN": False,
            "SCHEIDUNGSFOLGEVEREINBARUNG": True,
            "VERFAHRENSKOSTENHILFE": True,
            "SCHEIDUNGSFOLGEVEREINBARUNG_ABSCHLUSSDATUM": "02.01.2001",
            "AGREEMENT_DATE_SIGNED": "02.01.2001",
            "APPLICANT_NET_INCOME": "3.000,00 €",
            "RESPONDENT_NET_INCOME": "1.000,00 €",
            "TOTAL_PROCEDURAL_VALUE": "12.000,00 €",
            "children": [
                {
                    "name": "Julia Mustermann",
                    "birth_date": "01.01.2014",
                    "custody": "Antragsgegner",
                },
                {
                    "name": "Dennis Mustermann",
                    "birth_date": "01.01.2014",
                    "custody": "Antragsgegnerin",
                },
                # Weitere Kinderdaten können hier hinzugefügt werden
            ],
        }

        # Zuweisen der Testdaten zu den Formularfeldern
        self.court_name_input.value = test_daten["COURT_NAME"]
        self.court_department_input.value = test_daten["COURT_DEPARTMENT"]
        self.court_address_input.value = test_daten["COURT_ADDRESS"]
        self.court_zip_city_input.value = test_daten["COURT_ZIP_CITY"]
        self.lawyer_name_input.value = test_daten["LAWYER_NAME"]
        self.lawyer_email_input.value = test_daten["LAWYER_EMAIL"]
        self.lawyer_phone_input.value = test_daten["LAWYER_PHONE"]
        self.lawyer_fax_input.value = test_daten["LAWYER_FAX"]
        self.lawyer_contact_date_input.value = test_daten["LAWYER_CONTACT_DATE"]
        self.reference_input.value = test_daten["LAWYER_REF"]
        self.verfahrenswert_eingabefeld.value = test_daten["PROCEDURE_VALUE"]
        applicant_name_parts = test_daten["APPLICANT_NAME"].split(" ")
        self.applicant_vorname_eingabefeld.value = applicant_name_parts[0]
        if len(applicant_name_parts) > 1:
            self.applicant_nachname_eingabefeld.value = " ".join(
                applicant_name_parts[1:]
            )
        else:
            self.applicant_nachname_eingabefeld.value = ""
        self.applicant_geschlecht_select.value = test_daten["APPLICANT_GENDER"]
        self.applicant_birthdate_eingabefeld.value = test_daten["APPLICANT_BIRTH_DATE"]
        self.applicant_geburtsname_eingabefeld.value = (
            test_daten["APPLICANT_BIRTH_NAME"]
            if test_daten["APPLICANT_BIRTH_NAME"]
            else ""
        )
        self.applicant_adress_eingabefeld.value = test_daten["APPLICANT_ADDRESS"]

        self.datum_eheschließung_eingabefeld.value = test_daten["MARRIAGE_DATE"]
        self.ort_eheschließung_eingabefeld.value = test_daten["MARRIAGE_LOCATION"]
        self.eheschließungsnummer_eingabefeld.value = test_daten["REGISTRATION_NUMBER"]
        self.standesamt_eingabefeld.value = test_daten["MARRIAGE_OFFICE"]
        respondent_name_parts = test_daten["RESPONDENT_NAME"].split(" ")
        self.respondent_vorname_eingabefeld.value = respondent_name_parts[0]
        if len(respondent_name_parts) > 1:
            self.respondent_nachname_eingabefeld.value = " ".join(
                respondent_name_parts[1:]
            )
        else:
            self.respondent_nachname_eingabefeld.value = ""
        self.respondent_geschlecht_select.value = test_daten["RESPONDENT_GENDER"]
        self.respondent_birthdate_eingabefeld.value = test_daten[
            "RESPONDENT_BIRTH_DATE"
        ]
        self.respondent_geburtsname_eingabefeld.value = (
            test_daten["RESPONDENT_BIRTH_NAME"]
            if test_daten["RESPONDENT_BIRTH_NAME"]
            else ""
        )
        self.respondent_adress_eingabefeld.value = test_daten["RESPONDENT_ADDRESS"]

        self.getrennt_seit_eingabefeld.value = test_daten["SEPARATION_DATE"]
        self.scheidungsfolgevereinbarung_existenz.value = test_daten[
            "SCHEIDUNGSFOLGEVEREINBARUNG"
        ]
        self.datum_scheidungsfolgevereinbarung_eingabefeld.value = (
            test_daten["SCHEIDUNGSFOLGEVEREINBARUNG_ABSCHLUSSDATUM"]
            if test_daten["SCHEIDUNGSFOLGEVEREINBARUNG"]
            else ""
        )
        self.applicant_nettoeinkommen_eingabefeld.value = test_daten[
            "APPLICANT_NET_INCOME"
        ]
        self.respondent_nettoeinkommen_eingabefeld.value = test_daten[
            "RESPONDENT_NET_INCOME"
        ]
        self.verfahrenswert_eingabefeld.value = test_daten["TOTAL_PROCEDURAL_VALUE"]
        self.verfahrenskostenhilfe.value = test_daten["VERFAHRENSKOSTENHILFE"]

        # Anpassung der Zuweisungslogik für das wohnort_dropdown
        custody_mapping = {
            "Antragsgegner": "Antraggegner*in",
            "Antragsgegnerin": "Antraggegner*in",
            # Fügen Sie weitere Zuordnungen hinzu, falls nötig
        }

        # Behandlung der Kinderdaten
        for kid_data in test_daten["children"]:
            # Füge ein neues Kind hinzu
            self.kinder_box.add_child_entity(
                None
            )  # None, weil das Event-Argument hier irrelevant ist

            # Das zuletzt hinzugefügte Kindeingabe-Objekt erhalten
            new_kid = self.kinder_box.kindeingabe_list[-1]

            # Aufspalten des Namens in Vor- und Nachname
            kid_name_parts = kid_data["name"].split()
            kid_vorname = kid_name_parts[0] if len(kid_name_parts) > 0 else ""
            kid_nachname = (
                " ".join(kid_name_parts[1:]) if len(kid_name_parts) > 1 else ""
            )

            # Zuweisen der Daten zum zuletzt hinzugefügten Kindeingabe-Objekt
            new_kid.vorname_eingabefeld.value = kid_vorname
            new_kid.nachname_eingabefeld.value = kid_nachname
            new_kid.geburtsdatum_eingabefeld.value = kid_data["birth_date"]
            # Anwendung der Zuordnungslogik für das Dropdown
            dropdown_value = custody_mapping.get(
                kid_data["custody"], "Antragsteller*in"
            )  # Standardwert als Fallback
            new_kid.wohnort_dropdown.value = dropdown_value

    def setup_input_fields(self, lawyer_details):
        

        # Input fields and labels
        self.reference_input = toga.TextInput(style=StandardStyling.standard_input_style())
        self.court_name_input = toga.TextInput(style=StandardStyling.standard_input_style())
        self.court_department_input = toga.TextInput(style=StandardStyling.standard_input_style())
        self.court_address_input = toga.TextInput(style=StandardStyling.standard_input_style())
        self.court_zip_city_input = toga.TextInput(style=StandardStyling.standard_input_style())

        self.lawyer_name_input = toga.TextInput(
            value=lawyer_details.get("name", ""), style=StandardStyling.standard_input_style()
        )
        self.lawyer_email_input = toga.TextInput(
            value=lawyer_details.get("email", ""), style=StandardStyling.standard_input_style()
        )
        self.lawyer_phone_input = toga.TextInput(
            value=lawyer_details.get("phone", ""), style=StandardStyling.standard_input_style()
        )
        self.lawyer_fax_input = toga.TextInput(
            value=lawyer_details.get("fax", ""), style=StandardStyling.standard_input_style()
        )

        self.lawyer_contact_date_input = toga.TextInput(
            value=self.translate_date_to_german(self.get_current_date_in_word_format()),
            style=StandardStyling.standard_input_style(),
        )
        # self.case_file_number_input = toga.TextInput(style=StandardStyling.standard_input_style())
        self.defendant_name_input = toga.TextInput(style=StandardStyling.standard_input_style())
        self.fine_notice_date_input = toga.TextInput(
            value=self.get_current_date(), style=StandardStyling.standard_highlighted_input_style()
        )
        self.fine_notice_delivery_date_input = toga.TextInput(
            value=self.get_current_date(), style=StandardStyling.standard_highlighted_input_style()
        )
        self.gender_select = toga.Selection(
            items=["Herr", "Frau", "Divers"], style=StandardStyling.standard_input_style()
        )

        # Append all input fields and labels to the standardeingabe_box
        # Append new input fields and labels to the standardeingabe_box

        # DATEV Abfrage
        self.standardeingabe_box.add(
            toga.Label("Unser Zeichen:", style=StandardStyling.standard_label_style())
        )
        self.standardeingabe_box.add(self.reference_input)
       # self.standardeingabe_box.add(
       #     toga.Button("Daten importieren", on_press=self.datenabgleich_datev,style=StandardStyling.standard_button_style())
      #  )

        self.standardeingabe_box.add(
            toga.Label("Gerichtsname:", style=StandardStyling.standard_label_style())
        )
        self.standardeingabe_box.add(self.court_name_input)
        self.standardeingabe_box.add(
            toga.Label("Abteilung:", style=StandardStyling.standard_label_style())
        )
        self.standardeingabe_box.add(self.court_department_input)
        self.standardeingabe_box.add(
            toga.Label("Adresse:", style=StandardStyling.standard_label_style())
        )
        self.standardeingabe_box.add(self.court_address_input)
        self.standardeingabe_box.add(
            toga.Label("PLZ und Stadt:", style=StandardStyling.standard_label_style())
        )
        self.standardeingabe_box.add(self.court_zip_city_input)
        self.standardeingabe_box.add(
            toga.Label("Anwaltsname:", style=StandardStyling.standard_label_style())
        )
        self.standardeingabe_box.add(self.lawyer_name_input)
        self.standardeingabe_box.add(
            toga.Label("E-Mail:", style=StandardStyling.standard_label_style())
        )
        self.standardeingabe_box.add(self.lawyer_email_input)
        self.standardeingabe_box.add(
            toga.Label("Telefonnummer:", style=StandardStyling.standard_label_style())
        )
        self.standardeingabe_box.add(self.lawyer_phone_input)
        self.standardeingabe_box.add(
            toga.Label("Fax:", style=StandardStyling.standard_label_style())
        )
        self.standardeingabe_box.add(self.lawyer_fax_input)
        self.standardeingabe_box.add(
            toga.Label("Datum des Antrags:", style=StandardStyling.standard_label_style())
        )
        self.standardeingabe_box.add(self.lawyer_contact_date_input)
        # self.standardeingabe_box.add(toga.Label("Az.:", style=StandardStyling.standard_input_style()))
        # self.standardeingabe_box.add(self.case_file_number_input)

    def create_umstaende_section(self):

        self.verfahrenskostenhilfe = toga.Switch(
            "Verfahrenskostenhilfe beantragen", style=StandardStyling.standard_switch_style()
        )
        self.umstaende_box.add(self.verfahrenskostenhilfe)
        # Ehe
        self.umstaende_box.add(toga.Label("Ehe", style=StandardStyling.standard_label_style()))
        self.umstaende_box.add(
            toga.Label("Datum der Eheschließung", style=StandardStyling.standard_label_style())
        )
        self.datum_eheschließung_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.datum_eheschließung_eingabefeld)
        self.umstaende_box.add(
            toga.Label("Ort der Eheschließung", style=StandardStyling.standard_label_style())
        )
        self.ort_eheschließung_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.ort_eheschließung_eingabefeld)
        self.umstaende_box.add(
            toga.Label("Eheschließungsnummer", style=StandardStyling.standard_label_style())
        )
        self.eheschließungsnummer_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.eheschließungsnummer_eingabefeld)
        self.umstaende_box.add(
            toga.Label("Standesamt", style=StandardStyling.standard_label_style())
        )
        self.standesamt_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.standesamt_eingabefeld)
        self.umstaende_box.add(
            toga.Label("Getrennt seit:", style=StandardStyling.standard_label_style())
        )
        self.getrennt_seit_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.getrennt_seit_eingabefeld)

        self.scheidungsfolgevereinbarung_existenz = toga.Switch(
            "Scheidungsfolgevereinbarung existent",
            style=StandardStyling.standard_switch_style(),
            on_change=self.scheidungsfolgevereinbarung_existenz_changed,
        )
        self.umstaende_box.add(self.scheidungsfolgevereinbarung_existenz)

        # Antragsteller/in
        self.umstaende_box.add(
            toga.Label("Antragsteller*in", style=StandardStyling.standard_label_style())
        )
        self.umstaende_box.add(
            toga.Label("Geschlecht:", style=StandardStyling.standard_label_style())
        )
        self.applicant_geschlecht_select = toga.Selection(
            items=["Herr", "Frau", "Divers"], style=StandardStyling.standard_selection_style()
        )
        self.umstaende_box.add(self.applicant_geschlecht_select)
        self.umstaende_box.add(toga.Label("Vorname:", style=StandardStyling.standard_label_style()))
        self.applicant_vorname_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.applicant_vorname_eingabefeld)
        self.umstaende_box.add(toga.Label("Nachname:", style=StandardStyling.standard_label_style()))
        self.applicant_nachname_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.applicant_nachname_eingabefeld)
        self.umstaende_box.add(
            toga.Label("Geburtsname:", style=StandardStyling.standard_label_style())
        )
        self.applicant_geburtsname_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.applicant_geburtsname_eingabefeld)

        self.umstaende_box.add(
            toga.Label("Geburtsdatum:", style=StandardStyling.standard_label_style())
        )
        self.applicant_birthdate_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.applicant_birthdate_eingabefeld)
        self.umstaende_box.add(toga.Label("Adresse:", style=StandardStyling.standard_label_style()))
        self.applicant_adress_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.applicant_adress_eingabefeld)
        self.umstaende_box.add(
            toga.Label("Nettoeinkommen:", style=StandardStyling.standard_label_style())
        )
        self.applicant_nettoeinkommen_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.applicant_nettoeinkommen_eingabefeld)
        self.umstaende_box.add(
            toga.Label("Wohnsituation:", style=StandardStyling.standard_label_style())
        )
        self.applicant_wohnsituation_dropdown = toga.Selection(style=StandardStyling.standard_selection_style(),
            items=[
                "Räumlich getrennt in gemeinsamer Immobilie",
                "In einer anderen Immobilie (ausgezogen)",
                "Wohnt in gemeinsamer Immobilie",
            ]
        )
        self.umstaende_box.add(self.applicant_wohnsituation_dropdown)

        # Antraggegner/in
        self.umstaende_box.add(
            toga.Label("Antraggegner*in", style=StandardStyling.standard_label_style())
        )
        self.umstaende_box.add(
            toga.Label("Geschlecht:", style=StandardStyling.standard_label_style())
        )
        self.respondent_geschlecht_select = toga.Selection(
            items=["Herr", "Frau", "Divers"], style=StandardStyling.standard_input_style()
        )
        self.umstaende_box.add(self.respondent_geschlecht_select)
        self.umstaende_box.add(toga.Label("Vorname:", style=StandardStyling.standard_label_style()))
        self.respondent_vorname_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.respondent_vorname_eingabefeld)
        self.umstaende_box.add(toga.Label("Nachname:", style=StandardStyling.standard_label_style()))
        self.respondent_nachname_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.respondent_nachname_eingabefeld)
        self.umstaende_box.add(
            toga.Label("Geburtsname:", style=StandardStyling.standard_label_style())
        )
        self.respondent_geburtsname_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.respondent_geburtsname_eingabefeld)

        self.umstaende_box.add(
            toga.Label("Geburtsdatum:", style=StandardStyling.standard_label_style())
        )
        self.respondent_birthdate_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.respondent_birthdate_eingabefeld)
        self.umstaende_box.add(toga.Label("Adresse:", style=StandardStyling.standard_label_style()))
        self.respondent_adress_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.respondent_adress_eingabefeld)
        self.umstaende_box.add(
            toga.Label("Nettoeinkommen:", style=StandardStyling.standard_label_style())
        )
        self.respondent_nettoeinkommen_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.respondent_nettoeinkommen_eingabefeld)
        self.umstaende_box.add(
            toga.Label("Wohnsituation:", style=StandardStyling.standard_label_style())
        )
        self.wohnsituation_dropdown = toga.Selection(style=StandardStyling.standard_selection_style(),
            items=[
                "Räumlich getrennt in gemeinsamer Immobilie",
                "In einer anderen Immobilie (ausgezogen)",
                "Wohnt in gemeinsamer Immobilie",
            ]
        )
        self.umstaende_box.add(self.wohnsituation_dropdown)

        # Verfahrenswert
        self.umstaende_box.add(
            toga.Label("Verfahrenswert", style=StandardStyling.standard_label_style())
        )
        self.verfahrenswert_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.umstaende_box.add(self.verfahrenswert_eingabefeld)

    def scheidungsfolgevereinbarung_existenz_changed(self, widget):
        # wenn checkbox gesetzt ist, dann wird das label und das e ingabefeld angezeigt, wenn der hacken entfernt wird verschwinden beide elemente
        if self.scheidungsfolgevereinbarung_existenz.value:
            # position für label ist die position nach der checkbox
            position_fuer_label = (
                self.umstaende_box.children.index(
                    self.scheidungsfolgevereinbarung_existenz
                )
                + 1
            )
            self.scheidungsfolgevereinbarung_label = toga.Label(
                "Datum der Scheidungsfolgevereinbarung:",
                style=StandardStyling.standard_label_style(),
            )
            self.umstaende_box.insert(
                position_fuer_label, self.scheidungsfolgevereinbarung_label
            )
            self.datum_scheidungsfolgevereinbarung_eingabefeld = toga.TextInput(
                style=StandardStyling.standard_input_style()
            )
            position_fuer_eingabefeld = position_fuer_label + 1
            self.umstaende_box.insert(
                position_fuer_eingabefeld,
                self.datum_scheidungsfolgevereinbarung_eingabefeld,
            )
        else:
            # wenn checkbox nicht gesetzt ist, dann wird das label und das eingabefeld entfernt
            self.umstaende_box.remove(self.scheidungsfolgevereinbarung_label)
            self.umstaende_box.remove(
                self.datum_scheidungsfolgevereinbarung_eingabefeld
            )

    def create_beweismittel_section(self):
        self.beweismittel_data = get_beweismittel_data_scheidung()

        self.beweismittel_box.clear()

        self.beweismittel_switches: List[toga.Switch] = []  # Store the switch widgets
        for option in self.beweismittel_data.get("options", []):
            switch = toga.Switch(text=option, style=StandardStyling.standard_switch_style())
            self.beweismittel_switches.append(switch)  # Add the switch to the list
            self.beweismittel_box.add(switch)

        edit_button = toga.Button(
            "Liste bearbeiten",
            on_press=self.switch_beweismittel_section_to_edit_mode,
            style=StandardStyling.standard_button_style(),
        )
        self.beweismittel_box.add(edit_button)

    def switch_beweismittel_section_to_edit_mode(self, widget):
        self.beweismittel_edit_box.clear()  # Clear previous content if any

        # Add text inputs for each option in the beweismittel_edit_box
        self.edit_inputs = []
        for option in self.beweismittel_data.get("options", []):
            text_input = toga.TextInput(value=option, style=StandardStyling.standard_input_style())
            self.edit_inputs.append(text_input)
            self.beweismittel_edit_box.add(text_input)

        # Add an empty text input to add new options in the beweismittel_edit_box
        self.new_option_input = toga.TextInput(
            placeholder="New option", style=StandardStyling.standard_input_style()
        )
        self.beweismittel_edit_box.add(self.new_option_input)

        # Add Save and Cancel buttons in the beweismittel_edit_box
        save_button = toga.Button(
            "Speichern", on_press=self.save_edit_window, style=StandardStyling.standard_button_style()
        )
        cancel_button = toga.Button(
            "Abbrechen", on_press=self.close_edit_window, style=StandardStyling.standard_button_style()
        )
        self.beweismittel_edit_box.add(save_button)
        self.beweismittel_edit_box.add(cancel_button)

        # Switch from displaying the beweismittel_box to the beweismittel_edit_box
        self.remove(self.beweismittel_box)
        self.insert(1, self.beweismittel_edit_box)

    def close_edit_window(self, widget):

        # TODO Find a way to figure out at what position the beweismittel_edit_box in the child array is so that the beweismittel_box can be put there and not accidently somewhere else in the order
        # Close the edit window and switch back to the beweismittel switches
        self.remove(self.beweismittel_edit_box)
        self.insert(1, self.beweismittel_box)

    def save_edit_window(self, widget):
        # Placeholder implementation for saving the edited options
        # Collect the values from the text inputs
        edited_options = [
            text_input.value for text_input in self.edit_inputs if text_input.value
        ]
        if self.new_option_input.value:
            edited_options.append(self.new_option_input.value)

        # Update the beweismittel_data with the edited options
        self.beweismittel_data["options"] = edited_options

        set_beweismittel_data_Scheidung(self.beweismittel_data)

        # Refresh the beweismittel section to display the updated options
        self.remove_beweismittel_switches()
        self.create_beweismittel_section()
        self.close_edit_window(widget)

    def remove_beweismittel_switches(self):
        # Remove all beweismittel switches from the view
        self.beweismittel_box.clear()

    def get_current_date_in_word_format(self):
        # Get the current date in the "XX. Month YYYY" format
        return datetime.now().strftime("%d. %B %Y")

    def translate_date_to_german(self, date_str):
        # Map of English month names to German month names
        month_translation = {
            "January": "Januar",
            "February": "Februar",
            "March": "März",
            "April": "April",
            "May": "Mai",
            "June": "Juni",
            "July": "Juli",
            "August": "August",
            "September": "September",
            "October": "Oktober",
            "November": "November",
            "December": "Dezember",
        }

        # Split the date string to extract the month
        parts = date_str.split()
        if len(parts) == 3:
            day, month, year = parts
            # Translate the month to German
            german_month = month_translation.get(month, month)
            # Return the date string in German format
            return f"{day} {german_month} {year}"
        return date_str  # Return the original string if format is unexpected

    def get_current_date(self):
        # Get the current date in the format "DD.MM.YYYY"
        return datetime.now().strftime("%d.%m.%Y")

    def generate_lawyer_list(self):
        # Implement the logic to generate lawyer list from data
        lawyer_data = get_lawyer_data()
        lawyer_details = lawyer_data.get("lawyer_details", {})
        lawyer_list = []
        for lawyer_id, details in lawyer_details.items():
            lawyer_list.append(
                f"{details['title']} {details['name']}: {details['specialty']}"
            )
        return "\n".join(lawyer_list)

    def create_application(self, widget):

        # TODO Liste in format für Formular anpassen, weiteres Feld
        # Collect data from input fields
        kindeingabe_list = {}

        for kid in self.kinder_box.kindeingabe_list:

            kid_vorname = kid.vorname_eingabefeld.value
            kid_nachname = kid.nachname_eingabefeld.value
            kid_geburtsdatum = kid.geburtsdatum_eingabefeld.value
            kid_wohnhaft = kid.wohnort_dropdown.value
            kid_id = uuid4()
            kindeingabe_list[kid_id] = {
                "vorname": kid_vorname,
                "nachname": kid_nachname,
                "geburtsdatum": kid_geburtsdatum,
                "wohnhaft": kid_wohnhaft,
            }

        children_data = []
        for kid in self.kinder_box.kindeingabe_list:
            kid_vorname = kid.vorname_eingabefeld.value
            kid_nachname = kid.nachname_eingabefeld.value
            kid_geburtsdatum = kid.geburtsdatum_eingabefeld.value
            kid_custody_mapping = {
                "Antragsteller*in": "Antragsteller",
                "Antraggegner*in": "Antragsgegner",
            }
            kid_custody = kid_custody_mapping[
                kid.wohnort_dropdown.value
            ]  # Übersetzung des Sorgerechts

            children_data.append(
                {
                    "name": f"{kid_vorname} {kid_nachname}",
                    "birth_date": kid_geburtsdatum,
                    "custody": kid_custody,
                }
            )

        self.applicant_fullname = (
            self.applicant_vorname_eingabefeld.value
            + " "
            + self.applicant_nachname_eingabefeld.value
        )
        self.respondent_fullname = (
            self.respondent_vorname_eingabefeld.value
            + " "
            + self.respondent_nachname_eingabefeld.value
        )
        daten_aus_formular = {
            "COURT_NAME": self.court_name_input.value,
            "COURT_DEPARTMENT": self.court_department_input.value,
            "COURT_ADDRESS": self.court_address_input.value,
            "COURT_ZIP_CITY": self.court_zip_city_input.value,
            "LAWYER_NAME": self.lawyer_name_input.value,
            "LAWYER_EMAIL": self.lawyer_email_input.value,
            "LAWYER_PHONE": self.lawyer_phone_input.value,
            "LAWYER_FAX": self.lawyer_fax_input.value,
            "LAWYER_CONTACT_DATE": self.lawyer_contact_date_input.value,
            "LAWYER_REF": self.reference_input.value,
            # "CASE_FILE_NUMBER": self.case_file_number_input.value,
            "PROCEDURE_VALUE": self.verfahrenswert_eingabefeld.value,
            "APPLICANT_NAME": self.applicant_fullname,
            "APPLICANT_GENDER": self.applicant_geschlecht_select.value,
            "APPLICANT_BIRTH_DATE": self.applicant_birthdate_eingabefeld.value,
            # if the field for APPLICANT_BIRTH_NAME is empty set the value to None
            "APPLICANT_BIRTH_NAME": (
                self.applicant_geburtsname_eingabefeld.value
                if self.applicant_geburtsname_eingabefeld.value != ""
                else None
            ),
            "APPLICANT_ADDRESS": self.applicant_adress_eingabefeld.value,
            "MARRIAGE_DATE": self.datum_eheschließung_eingabefeld.value,
            "MARRIAGE_LOCATION": self.ort_eheschließung_eingabefeld.value,
            "REGISTRATION_NUMBER": self.eheschließungsnummer_eingabefeld.value,
            "MARRIAGE_OFFICE": self.standesamt_eingabefeld.value,
            "RESPONDENT_NAME": self.respondent_fullname,
            "RESPONDENT_GENDER": self.respondent_geschlecht_select.value,
            "RESPONDENT_BIRTH_DATE": self.respondent_birthdate_eingabefeld.value,
            "RESPONDENT_BIRTH_NAME": (
                self.respondent_geburtsname_eingabefeld.value
                if self.respondent_geburtsname_eingabefeld.value != ""
                else None
            ),  # if available
            "RESPONDENT_ADDRESS": self.respondent_adress_eingabefeld.value,
            "SEPARATION_DATE": self.getrennt_seit_eingabefeld.value,
            "AUSGEZOGEN": True,
            "SCHEIDUNGSFOLGEVEREINBARUNG": self.scheidungsfolgevereinbarung_existenz.value,
            "SCHEIDUNGSFOLGEVEREINBARUNG_ABSCHLUSSDATUM": (
                self.datum_scheidungsfolgevereinbarung_eingabefeld.value
                if self.scheidungsfolgevereinbarung_existenz.value
                else None
            ),
            "AGREEMENT_DATE_SIGNED": "05.05.2023",  # Date when the divorce consequences agreement was signed
            "APPLICANT_NET_INCOME": self.applicant_nettoeinkommen_eingabefeld.value,  # Applicant's monthly net income
            "RESPONDENT_NET_INCOME": self.respondent_nettoeinkommen_eingabefeld.value,  # Respondent's monthly net income
            "TOTAL_PROCEDURAL_VALUE": self.verfahrenswert_eingabefeld.value,  # Procedural value based on three months' income
            "children": children_data,
            "LAWYER_FULL_NAME": self.lawyer_name_input.value,
            "LAWYER_TITLE": self.lawyer_details.get("title"),
            "LAWYER_SPECIALTY": self.lawyer_details.get("specialty"),
            # "BEWEISMITTEL_LISTE": {
            #    switch.text: switch.value for switch in self.beweismittel_switches
            # },
            "VERFAHRENSKOSTENHILFE": self.verfahrenskostenhilfe.value,
        }

        # daten_aus_formular = test_daten_anstelle_der_daten_aus_dem_eingabe_formular

        # Assuming there is a variable that holds the value for SCHEIDUNGSFOLGEVEREINBARUNG
        scheidungsfolgevereinbarung = daten_aus_formular.get(
            "SCHEIDUNGSFOLGEVEREINBARUNG", False
        )

        # Check if all required fields are filled and at least one beweismittel_switch is selected
        required_fields = [
            "COURT_NAME",
            # "COURT_DEPARTMENT",
            # "COURT_ADDRESS",
            # "COURT_ZIP_CITY",
            "LAWYER_NAME",
            "LAWYER_EMAIL",
            "LAWYER_PHONE",
            "LAWYER_CONTACT_DATE",
            "LAWYER_REF",
            "APPLICANT_NAME",
        ]
        # Add the additional required field if SCHEIDUNGSFOLGEVEREINBARUNG is True
        if scheidungsfolgevereinbarung:
            required_fields.append("SCHEIDUNGSFOLGEVEREINBARUNG_ABSCHLUSSDATUM")

        missing_fields = [
            field for field in required_fields if not daten_aus_formular.get(field)
        ]
        # if missing_fields or not any(self.beweismittel_switches):
        if missing_fields:
            error_message = ""
            field_labels = {
                "COURT_NAME": "Gerichtsname",
                "COURT_DEPARTMENT": "Abteilung",
                "COURT_ADDRESS": "Adresse",
                "COURT_ZIP_CITY": "PLZ und Stadt",
                "LAWYER_NAME": "Anwaltsname",
                "LAWYER_EMAIL": "Anwalt E-Mail",
                "LAWYER_PHONE": "Anwalt Telefonnummer",
                "LAWYER_CONTACT_DATE": "Datum des Antrags",
                "LAWYER_REF": "Az.",
                "APPLICANT_NAME": "Antragsteller",
                "FINE_NOTICE_DATE": "Zugestellt am",
                "FINE_NOTICE_DELIVERY_DATE": "Datum des Bußgeldbescheids",
                "SCHEIDUNGSFOLGEVEREINBARUNG_ABSCHLUSSDATUM": "Datum der Scheidungsfolgevereinbarung",
            }
            if missing_fields:
                error_message += "Bitte füllen Sie die folgenden Pflichtfelder aus:\n"
                for field in missing_fields:
                    error_message += f"{field_labels[field]}\n\n"
                # error_message += "Bitte wählen Sie mindestens ein Beweismittel aus."

            fehlermeldung = Fehlermeldung(
                self.app,
                retry_function=lambda: self.create_application(widget),
                fehlermeldung=error_message,
            )
            self.fehlermeldung_widget = fehlermeldung
            self.footer_box.add(self.fehlermeldung_widget)
            return

        daten_aus_formular = hinzufuegen_anwaltsdaten_zum_kontext(daten_aus_formular)

        # daten_aus_formular = self.hinzufuegen_beweismittel_zum_kontext_fuer_form_daten(daten_aus_formular, daten_aus_formular)

        # Initialize the data processor
        data_processor = AntragVorlageDatenVerarbeitung(
            name_der_template_datei=self.name_der_template_datei
        )

        print(daten_aus_formular)

        # Generate the output file
        success, error_message = (
            data_processor.erzeuge_antragsdatei_mit_platzhalterinformationen(
                daten_aus_formular=daten_aus_formular
            )
        )
        if success:
            # Entferne das Antrag-Manager-Widget, falls es existiert, und setze es zurück.
            if self.antrag_manager_widget:
                self.app.main_box.remove(self.antrag_manager_widget)
                self.antrag_manager_widget = None

            # Generiere einen einzigartigen Dateinamen für die Ausgabedatei.
            unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.formular_name}_{daten_aus_formular['APPLICANT_NAME']}.docx".replace(" ", "_")

            # Setze den Pfad für die Ausgabedatei.
            mandant_folder = get_mandanten_folder()
            output_folder_path = os.path.join(mandant_folder, daten_aus_formular["LAWYER_REF"])
            output_file_path = os.path.join(output_folder_path, unique_filename)

            # Erstelle den Ausgabeordner, falls er nicht existiert.
            if not os.path.exists(output_folder_path):
                os.makedirs(output_folder_path)

            # Verschiebe die temporäre Datei des ausgefüllten Antrags in den Ausgabeordner.
            shutil.copy(data_processor.pfad_zur_temp_datei_des_ausgefüllten_antrags, output_file_path)

            # Initialisiere den Datei-Manager mit der Ausgabedatei als Basis.
            file_manager = AntragDateiManager(app=self.app, base_docx_datei=output_file_path)

            # temp file löschen
            if data_processor.pfad_zur_temp_datei_des_ausgefüllten_antrags is not None:
                os.remove(data_processor.pfad_zur_temp_datei_des_ausgefüllten_antrags)

            # Füge das Datei-Manager-Interface zum Hauptcontainer der App hinzu.
            self.antrag_manager_widget = file_manager
            self.app.main_box.add(self.antrag_manager_widget)

            # Erstelle eine Ausführung in der Datenbank, um die Nutzung der Software zu dokumentieren.
            # Dies hilft festzuhalten, wie oft Nutzer die Software für spezifische Anträge eingesetzt haben.
            add_ausfuehrung(reference=self.reference_input.value, kundenprogramm_ID=self.kundenprogramm_ID, antrags_name=self.formular_name)

        else:
            
            # temp file löschen
            os.remove(data_processor.pfad_zur_temp_datei_des_ausgefüllten_antrags)
            
            # Create a Fehlermeldung component
            fehlermeldung = Fehlermeldung(
                self.app,
                retry_function=lambda: self.create_application(widget),
                fehlermeldung=error_message,
            )
            self.fehlermeldung_widget = fehlermeldung
            self.footer_box.add(self.fehlermeldung_widget)


    def datenabgleich_datev(self):
        self.datevdata = datenabfrage_datev_for_aktenzeichen(
            aktenzeichen=self.case_file_number_input.value,
            passwort=self.app.nutzerdateneingabekomponente.passwort_eingabefeld.value,
        )

        """def import_data(self, widget):
            


        self.court_name_input.value = self.datevdata.get("court_name")
        self.court_department_input.value = self.datevdata.get("court_department")
        self.court_address_input.value = self.datevdata.get("court_address")
        self.court_zip_city_input.value = self.datevdata.get("court_zip_city")
        self.lawyer_name_input.value = self.datevdata.get("lawyer_name")
        self.lawyer_email_input.value = self.datevdata.get("lawyer_email")
        self.lawyer_phone_input.value = self.datevdata.get("lawyer_phone")
        self.lawyer_fax_input.value = self.datevdata.get("lawyer_fax")
        self.lawyer_contact_date_input.value = self.datevdata.get("contact_date")
        self.reference_input.value = self.datevdata.get("reference")
        self.gender_select.value = self.datevdata.get("gender")
        self.defendant_name_input.value = self.datevdata.get("defendant_name")"""

        """ 
            Um die Daten aus dem JSON-Datensatz, den Sie erhalten, den Elementen Ihrer Benutzeroberfläche zuzuordnen, müssen wir zunächst eine angepasste Datenstruktur (datevdata) erstellen, die alle benötigten Informationen in einer Weise enthält, die mit den .get() Aufrufen in Ihrem import_data-Methode kompatibel ist.

            Aus dem von Ihnen bereitgestellten JSON-Datensatz und den UI-Elementen scheint es, als ob einige der erforderlichen Informationen direkt aus dem JSON abgerufen werden können, während andere möglicherweise nicht direkt verfügbar sind und daher Annahmen oder Standardwerte benötigen könnten.

            Hier ist ein Ansatz, wie Sie eine solche Datenstruktur aufbauen können, basierend auf den Informationen, die Sie aus dem JSON-Datensatz extrahieren möchten:

            Erstellen einer Datenstruktur (datevdata), die alle erforderlichen Felder enthält. Da im bereitgestellten JSON-Datensatz einige der spezifisch angefragten Felder wie court_name, court_department, court_address, court_zip_city, lawyer_name, lawyer_email, lawyer_phone, lawyer_fax, contact_date, reference, gender, defendant_name nicht direkt vorhanden sind, werde ich ein Beispiel geben, wie man eine solche Struktur basierend auf verfügbaren Daten und angenommenen Feldern erstellen könnte.
            Zuordnung der Daten zu den entsprechenden UI-Elementen.
            Zunächst ein Beispiel, wie die datevdata Struktur basierend auf den vorhandenen Daten aussehen könnte:

            datevdata = {
                "court_name": "Nicht verfügbar",  # Nicht im Datensatz, Annahme
                "court_department": "Nicht verfügbar",  # Nicht im Datensatz, Annahme
                "court_address": "Nicht verfügbar",  # Nicht im Datensatz, Annahme
                "court_zip_city": "Nicht verfügbar",  # Nicht im Datensatz, Annahme
                "lawyer_name": json_data[0]["partner"]["display_name"],  # Beispiel: "Ernst Exempeladvokat"
                "lawyer_email": "Nicht verfügbar",  # Nicht im Datensatz, Annahme
                "lawyer_phone": "Nicht verfügbar",  # Nicht im Datensatz, Annahme
                "lawyer_fax": "Nicht verfügbar",  # Nicht im Datensatz, Annahme
                "contact_date": json_data[0]["created"]["date"],  # Beispiel: "2018-09-27"
                "reference": json_data[0]["file_number"],  # Beispiel: "000001-2005/001:00"
                "gender": "Nicht verfügbar",  # Nicht im Datensatz, Annahme oder AI-Detektion erforderlich
                "defendant_name": "Mustermann"  # Annahme basierend auf "file_name"
            }

            Für die .get() Aufrufe in Ihrer import_data-Methode können Sie diese dann wie folgt verwenden:

            self.court_name_input.value = datevdata.get("court_name", "Standardwert")
            self.court_department_input.value = datevdata.get("court_department", "Standardwert")
            self.court_address_input.value = datevdata.get("court_address", "Standardwert")
            self.court_zip_city_input.value = datevdata.get("court_zip_city", "Standardwert")
            self.lawyer_name_input.value = datevdata.get("lawyer_name", "Standardwert")
            self.lawyer_email_input.value = datevdata.get("lawyer_email", "Standardwert")
            self.lawyer_phone_input.value = datevdata.get("lawyer_phone", "Standardwert")
            self.lawyer_fax_input.value = datevdata.get("lawyer_fax", "Standardwert")
            self.lawyer_contact_date_input.value = datevdata.get("contact_date", "Standardwert")
            self.reference_input.value = datevdata.get("reference", "Standardwert")
            self.gender_select.value = datevdata.get("gender", "Standardwert")  # Möglicherweise müssen Sie die Logik für die Zuweisung des Geschlechts hier anpassen
            self.defendant_name_input.value = datevdata.get("defendant_name", "Standardwert")

            Beachten Sie, dass die "Standardwert"-Platzhalter durch tatsächliche Standardwerte ersetzt werden sollten, die Sie verwenden möchten, falls die Daten nicht verfügbar sind. Für Felder wie gender, die möglicherweise eine komplexere Logik für die Zuweisung benötigen (z.B. basierend auf dem Namen), müssen Sie eine separate Logik implementieren, um diesen Wert zu bestimmen, bevor Sie ihn in datevdata einfügen.
        """


class Kindereingabe(toga.Box):

    def __init__(
        self,
        id: str | None = None,
    ):
        style = Pack(direction=COLUMN)
        super().__init__(id=id, style=style)

        self.kindeingabe_list: List[Kindeingabe] = (
            []
        )  # List to keep track of Kindeingabe instances

        self.add_child_button = toga.Button(
            "Kind hinzufügen", on_press=self.add_child_entity, style=StandardStyling.standard_button_style()
        )
        # Initially, add the buttons to the container
        self.add(self.add_child_button)

        self.kind_delete_button = toga.Button(
            "Kind entfernen", on_press=self.kind_entfernen, style=StandardStyling.standard_button_style()
        )
        self.add(self.kind_delete_button)

    def add_child_entity(self, widget):
        kind_box = Kindeingabe()
        self.kindeingabe_list.append(
            kind_box
        )  # Add the new Kindeingabe to the tracking list
        # Insert the Kindeingabe just above the buttons but below the last Kindeingabe
        insert_index = len(
            self.kindeingabe_list
        )  # Calculate the position where the new Kindeingabe should be inserted
        self.insert(insert_index - 1, kind_box)  # Insert at the calculated index

    def kind_entfernen(self, widget):
        if self.kindeingabe_list:  # Check if there's any Kindeingabe to remove
            last_kindeingabe = (
                self.kindeingabe_list.pop()
            )  # Remove the last Kindeingabe from the list
            self.remove(
                last_kindeingabe
            )  # Remove the last Kindeingabe from the Kindereingabe container


class Kindeingabe(toga.Box):

    def __init__(
        self,
        id: str | None = None,
    ):
        style = Pack(direction=COLUMN)
        super().__init__(id=id, style=style)

        self.add(toga.Label("Vorname:", style=StandardStyling.standard_label_style()))
        self.vorname_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.add(self.vorname_eingabefeld)
        self.add(toga.Label("Nachname:", style=StandardStyling.standard_label_style()))
        self.nachname_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.add(self.nachname_eingabefeld)
        self.add(toga.Label("Geburtsdatum:", style=StandardStyling.standard_label_style()))
        self.geburtsdatum_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        self.add(self.geburtsdatum_eingabefeld)
        self.add(toga.Label("Wohnt bei:", style=StandardStyling.standard_label_style()))
        self.wohnort_dropdown = toga.Selection(style=StandardStyling.standard_selection_style(),
            items=["Antragsteller*in", "Antraggegner*in"]
        )
        self.add(self.wohnort_dropdown)
