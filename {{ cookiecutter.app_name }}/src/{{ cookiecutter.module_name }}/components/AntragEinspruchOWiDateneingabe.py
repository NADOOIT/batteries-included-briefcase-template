from __future__ import annotations
import shutil
from typing import List, TYPE_CHECKING
import os

from nadoo_law.components.AntragVorlageDatenVerarbeitung import (
    AntragVorlageDatenVerarbeitung,
)
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from datetime import datetime
from nadoo_law.styling import StandardStyling

from nadoo_law.services import (
    add_ausfuehrung,
    get_beweismittel_data_OWi,
    get_datev_example_data,
    hinzufuegen_anwaltsdaten_zum_kontext,
    set_beweismittel_data_OWi,
    get_mandanten_folder
)
from nadoo_law.components.Fehlermeldung import Fehlermeldung
from nadoo_law.components.AntragDateiManager import AntragDateiManager



if TYPE_CHECKING:
    from nadoo_law.app import NadooLaw


class AntragEinspruchOWiDateneingabe(toga.Box):
    name_der_template_datei = "MUSTER_EINSPRUCH_OWI.docx"
    formular_name = "Einspruch OWi"
    kategorie = "Verkehrsrecht"
    kundenprogramm_ID = "4ccd2124-6875-42b1-adaf-7039f2954e4d"

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
        self.beweismittel_auswahl_box = toga.Box(style=Pack(direction=COLUMN, flex= 1))
        self.beweismittel_auswahl_edit_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        self.footer_box = toga.Box(style=Pack(direction=COLUMN, flex=1))

        self.setup_input_fields(lawyer_details)
        self.create_beweismittel_section()

        self.create_Antrag_button = toga.Button(
            "Antrag erstellen",
            on_press=self.create_application,
            style=StandardStyling.standard_button_style(),
        )
        self.footer_box.add(self.create_Antrag_button)

        self.add(self.standardeingabe_box)
        self.add(
            self.beweismittel_auswahl_box
        )  # This will be switched with beweismittel_auswahl_edit_box when editing
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
            "LAWYER_CONTACT_DATE": "05. Februar 2024",
            "LAWYER_REF": "000004-23",
            "CASE_FILE_NUMBER": "12.3.4567.89012.34",
            "DEFENDANT_NAME": "Max Mustermann",
            "FINE_NOTICE_DATE": "18.01.2023",
            "FINE_NOTICE_DELIVERY_DATE": "01.01.2023",
            "GENDER": "Herr",
            "LAWYER_FULL_NAME": "Sebastian Kutzner",
            "LAWYER_TITLE": "Rechtsanwalt",
            "LAWYER_SPECIALTY": "Fachanwalt für Verkehrsrecht",
            "BEWEISMITTEL_LISTE": {
                "Messprotokolle": True,
                "Ausbildungsnachweise der Mess- und Auswertebeamten": True,
                "Originalbeweisfotos": True,
                "Eichscheine": True,
                "Gesamte Messreihe vom Tattag": True,
                "Digitale Rohmessdaten sowie die dazugehörigen öff. Token und Passwörter": True,
                "Statistikdatei mit Case List": True,
                "Konformitätsbescheinigung und –erklärung zum Messgerät": True,
                "Kalibrier- und Testfotos": True,
                "Bedienungsanleitung der zum Tattag gültigen Version": True,
                "Auskunft über Reparaturen, Wartungen, vorgezogene Neueichung oder vgl. die Funktionsfähigkeit des hier verwendeten Messgerätes berührende Ereignisse": True,
                "Beschilderungsnachweise für 2 km vor und nach der Messstelle": True,
                "Liste aller am Tattag aufgenommenen Verkehrsverstöße": True,
            },
        }

        # Zuweisen der Testdaten zu den Formularfeldern für Einspruch OWi
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
        self.case_file_number_input.value = test_daten["CASE_FILE_NUMBER"]
        self.defendant_name_input.value = test_daten["DEFENDANT_NAME"]
        self.fine_notice_date_input.value = test_daten["FINE_NOTICE_DATE"]
        self.fine_notice_delivery_date_input.value = test_daten[
            "FINE_NOTICE_DELIVERY_DATE"
        ]
        self.gender_select.value = test_daten["GENDER"]

        # Beweismittel Liste füllen
        for beweismittel, status in test_daten["BEWEISMITTEL_LISTE"].items():
            for switch in self.beweismittel_switches:
                if switch.text == beweismittel:
                    switch.value = status
                    break

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
        self.case_file_number_input = toga.TextInput(style=StandardStyling.standard_input_style())
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

        # DATEV Abfrage
        self.standardeingabe_box.add(
            toga.Label("Unser Zeichen:", style=StandardStyling.standard_label_style())
        )
        self.standardeingabe_box.add(self.reference_input)
       # self.standardeingabe_box.add(
       #     toga.Button(
       #         "Daten importieren",
       #         on_press=self.datenabgleich_datev,
       #         style=StandardStyling.standard_button_style(),
       #     )
       # )

        # Append all input fields and labels to the standardeingabe_box
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

        self.standardeingabe_box.add(
            toga.Label("Az.:", style=StandardStyling.standard_label_style())
        )
        self.standardeingabe_box.add(self.case_file_number_input)
        self.standardeingabe_box.add(
            toga.Label("Geschlecht:", style=StandardStyling.standard_label_style())
        )
        self.standardeingabe_box.add(self.gender_select)
        self.standardeingabe_box.add(
            toga.Label("Kundenname:", style=StandardStyling.standard_label_style())
        )
        self.standardeingabe_box.add(self.defendant_name_input)
        self.standardeingabe_box.add(
            toga.Label("Datum des Bußgeldbescheids:", style=StandardStyling.standard_label_style())
        )
        self.standardeingabe_box.add(self.fine_notice_date_input)
        self.standardeingabe_box.add(
            toga.Label("Zugestellt am:", style=StandardStyling.standard_label_style())
        )
        self.standardeingabe_box.add(self.fine_notice_delivery_date_input)

    def create_beweismittel_section(self):
        self.beweismittel_data = get_beweismittel_data_OWi()

        self.beweismittel_auswahl_box.clear()

        self.beweismittel_switches: List[toga.Switch] = []  # Store the switch widgets
        for option in self.beweismittel_data.get("options", []):
            switch = toga.Switch(text=option, style=StandardStyling.standard_switch_style())
            self.beweismittel_switches.append(switch)  # Add the switch to the list
            self.beweismittel_auswahl_box.add(switch)

        edit_button = toga.Button(
            "Liste bearbeiten ", on_press=self.open_edit_window, style=StandardStyling.standard_button_style()
        )
        self.beweismittel_auswahl_box.add(edit_button)

    def open_edit_window(self, widget):
        self.beweismittel_auswahl_edit_box.clear()  # Clear previous content if any

        # Add text inputs for each option in the beweismittel_auswahl_edit_box
        self.edit_inputs = []
        for option in self.beweismittel_data.get("options", []):
            text_input = toga.TextInput(value=option, style=StandardStyling.standard_input_style())
            self.edit_inputs.append(text_input)
            self.beweismittel_auswahl_edit_box.add(text_input)

        # Add an empty text input to add new options in the beweismittel_auswahl_edit_box
        self.new_option_input = toga.TextInput(
            placeholder="New option", style=StandardStyling.standard_input_style()
        )
        self.beweismittel_auswahl_edit_box.add(self.new_option_input)

        # Add Save and Cancel buttons in the beweismittel_auswahl_edit_box
        save_button = toga.Button(
            "Speichern", on_press=self.save_edit_window, style=StandardStyling.standard_button_style()
        )
        cancel_button = toga.Button(
            "Abbrechen", on_press=self.close_edit_window, style=StandardStyling.standard_button_style()
        )
        self.beweismittel_auswahl_edit_box.add(save_button)
        self.beweismittel_auswahl_edit_box.add(cancel_button)

        # Switch from displaying the body_box to the beweismittel_auswahl_edit_box
        self.remove(self.beweismittel_auswahl_box)
        self.insert(1, self.beweismittel_auswahl_edit_box)

    def close_edit_window(self, widget):
        # Close the edit window and switch back to the beweismittel switches
        self.remove(self.beweismittel_auswahl_edit_box)
        self.insert(1, self.beweismittel_auswahl_box)

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

        set_beweismittel_data_OWi(self.beweismittel_data)

        # Refresh the beweismittel section to display the updated options
        self.remove_beweismittel_switches()
        self.create_beweismittel_section()
        self.close_edit_window(widget)

    def remove_beweismittel_switches(self):
        # Remove all beweismittel switches from the view
        self.body_box.clear()

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

    def create_application(self, widget):

        # Überprüfen Sie, ob bereits eine Fehlermeldung angezeigt wird, und entfernen Sie diese
        if self.fehlermeldung_widget:
            self.footer_box.remove(self.fehlermeldung_widget)
            self.fehlermeldung_widget = None

        # Collect data from input fields
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
            "CASE_FILE_NUMBER": self.case_file_number_input.value,
            "DEFENDANT_NAME": self.defendant_name_input.value,
            "FINE_NOTICE_DATE": self.fine_notice_date_input.value,
            "FINE_NOTICE_DELIVERY_DATE": self.fine_notice_delivery_date_input.value,
            "GENDER": self.gender_select.value,
            "LAWYER_FULL_NAME": self.lawyer_name_input.value,
            "LAWYER_TITLE": self.lawyer_details.get("title"),
            "LAWYER_SPECIALTY": self.lawyer_details.get("specialty"),
            "BEWEISMITTEL_LISTE": {
                switch.text: switch.value for switch in self.beweismittel_switches
            },
        }

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
            "CASE_FILE_NUMBER",
            "DEFENDANT_NAME",
            "FINE_NOTICE_DATE",
            "FINE_NOTICE_DELIVERY_DATE",
            "GENDER",
        ]

        missing_fields = [
            field for field in required_fields if not daten_aus_formular.get(field)
        ]
        if missing_fields or not any(self.beweismittel_switches):
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
                "CASE_FILE_NUMBER": "Zeichen",
                "DEFENDANT_NAME": "Kundenname",
                "FINE_NOTICE_DATE": "Zugestellt am",
                "FINE_NOTICE_DELIVERY_DATE": "Datum des Bußgeldbescheids",
            }
            if missing_fields:
                error_message += "Bitte füllen Sie die folgenden Pflichtfelder aus:\n"
                for field in missing_fields:
                    error_message += f"{field_labels[field]}\n\n"
                if not any(self.beweismittel_switches):
                    error_message += "Bitte wählen Sie mindestens ein Beweismittel aus."

            fehlermeldung = Fehlermeldung(
                self.app,
                retry_function=lambda: self.create_application(widget),
                fehlermeldung=error_message,
            )
            self.fehlermeldung_widget = fehlermeldung
            self.footer_box.add(self.fehlermeldung_widget)
            return

        daten_aus_formular = hinzufuegen_anwaltsdaten_zum_kontext(daten_aus_formular)

        daten_aus_formular = self.hinzufuegen_beweismittel_zum_kontext_fuer_form_daten(
            daten_aus_formular, daten_aus_formular
        )

        # Initialize the data processor
        data_processor = AntragVorlageDatenVerarbeitung(
            name_der_template_datei=self.name_der_template_datei
        )

        # Generate the output file
        success, error_message = (
            data_processor.erzeuge_antragsdatei_mit_platzhalterinformationen(
                daten_aus_formular=daten_aus_formular
            )
        )

        if success:
            # Überprüfen Sie, ob bereits ein AntragDateiManager angezeigt wird, und entfernen Sie diesen
            if self.antrag_manager_widget:
                self.app.main_box.remove(self.antrag_manager_widget)
                self.antrag_manager_widget = None

            # Generate a unique filename for the output file
            unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.formular_name}_{daten_aus_formular['DEFENDANT_NAME']}.docx".replace(
                " ", "_"
            )

            # Setze den Pfad für die Ausgabedatei.
            mandant_folder = get_mandanten_folder()
            output_folder_path = os.path.join(mandant_folder, daten_aus_formular["LAWYER_REF"])
            output_file_path = os.path.join(output_folder_path, unique_filename)

            # Erstelle den Ausgabeordner, falls er nicht existiert.s
            if not os.path.exists(output_folder_path):
                os.makedirs(output_folder_path)

            # TODO In AntragDateiManager verschieben
            # Save the output file
            shutil.copy(
                data_processor.pfad_zur_temp_datei_des_ausgefüllten_antrags,
                output_file_path,
            )

            # Initialize the file manager
            file_manager = AntragDateiManager(
                app=self.app, base_docx_datei=output_file_path
            )

            # temp file löschen
            os.remove(data_processor.pfad_zur_temp_datei_des_ausgefüllten_antrags)

            # Add the file manager interface to the main_box of the app
            self.antrag_manager_widget = file_manager
            self.app.main_box.add(self.antrag_manager_widget)
            
            # Erstelle eine Ausführung in der Datenbank, um die Nutzung der Software zu dokumentieren.
            # Dies hilft festzuhalten, wie oft Nutzer die Software für spezifische Anträge eingesetzt haben.
            add_ausfuehrung(reference=self.reference_input.value, kundenprogramm_ID=self.kundenprogramm_ID, antrags_name=self.formular_name)

        else:
            
            # temp file löschen
            if data_processor.pfad_zur_temp_datei_des_ausgefüllten_antrags is not None:
                os.remove(data_processor.pfad_zur_temp_datei_des_ausgefüllten_antrags)
            
            # Create a Fehlermeldung component
            fehlermeldung = Fehlermeldung(
                self.app,
                retry_function=lambda: self.create_application(widget),
                fehlermeldung=error_message,
            )
            self.fehlermeldung_widget = fehlermeldung
            self.footer_box.add(self.fehlermeldung_widget)

    def hinzufuegen_beweismittel_zum_kontext_fuer_form_daten(self, kontext, form_daten):
        beweismittel_optionen = get_beweismittel_data_OWi()["options"]
        beweismittel_ausgewaehlt = form_daten.get("BEWEISMITTEL_LISTE", {})

        # Erstellt die Liste der ausgewählten Beweismittel
        ausgewaehlte_beweismittel = [
            option
            for option in beweismittel_optionen
            if beweismittel_ausgewaehlt.get(option, False)
        ]

        kontext["AUSGEWÄHLTE_BEWEISMITTEL"] = ausgewaehlte_beweismittel
        return kontext

    def datenabgleich_datev(self):
        # self.datevdata = datenabfrage_datev_for_aktenzeichen(aktenzeichen=self.case_file_number_input.value, passwort=self.app.nutzerdateneingabekomponente.passwort_eingabefeld.value)
        self.datevdata = get_datev_example_data()

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
