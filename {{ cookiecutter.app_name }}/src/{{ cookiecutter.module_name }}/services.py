import subprocess
import platform
import os
import json
import shutil

from datetime import datetime

from {{ cookiecutter.app_name|lower|replace('-', '_') }}.CONSTANTS import KUNDENDATEN_ORDNER_APP, ARCHIV_ORDNER, BASE_DIR, UPDATE_ORDNER_NAME_USER, UPDATE_ORDNER_NAME_APP, SETTINGS_ORDNER

from {{ cookiecutter.app_name|lower|replace('-', '_') }}.utils import (
    get_base_dir_path, get_settings_file_path
)

""" 
Vorlage for JSON-Datei anbindung
def set_xyz_data(beweismittel_data):
    ensure_beweismittel_OWi_data_file_exists()
    file_path = get_beweismittel_OWi_data_file_path()
    with open(file_path, "w") as f:
        json.dump(beweismittel_data, f, indent=4)


def get_xyz_data():
    ensure_beweismittel_OWi_data_file_exists()
    file_path = get_beweismittel_OWi_data_file_path()
    with open(file_path, "r") as f:
        return json.load(f)
"""
def setup_folders():
    # Grund Verzeichnisstruktur anlegen
    ensure_base_folder_exits()
    ensure_folder_exists(UPDATE_ORDNER_NAME_USER)
    ensure_folder_exists(SETTINGS_ORDNER)
    pass
        
def ensure_folder_exists(folder_name):
    base_dir = get_base_dir_path()
    folder_path = os.path.join(base_dir, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def ensure_base_folder_exits():
    base_dir = os.path.join(os.path.expanduser("~"), BASE_DIR)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

def open_file(file_path):
    if file_path:
        try:
            if platform.system() == "Windows":
                subprocess.run(["explorer", file_path], check=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", file_path], check=True)
            else:  # Assuming Linux
                subprocess.run(["xdg-open", file_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error opening file: {e}")
    else:
        print("File path is not set. Unable to open file.")
        
def get_updates_datei_user():
    #ich möchte den dateipfad der update.json datei aus dem updates ordner haben, welcher im updates ordner im user verzeichnis liegt
    updates_dateipfad_user = os.path.join(os.path.expanduser("~"), get_base_dir(), UPDATE_ORDNER_NAME_USER, "update.json")
    return updates_dateipfad_user

def get_updates_pdf_path(app):
    updates_pdf_dateipfad = os.path.join(app.paths.app, "resources", "update.pdf")
    return updates_pdf_dateipfad

def update_daten_laden_user():
        file_path = get_updates_datei_user()
        with open(file_path, "r") as f:
            return json.load(f)
        
def update_daten_laden_app(app):
        file_path = get_updates_datei_app(app)
        with open(file_path, "r") as f:
            return json.load(f)
        
def get_updates_datei_app(app):
    updates_datei_app = os.path.join(app.paths.app, "resources", UPDATE_ORDNER_NAME_APP, "update.json")
    return updates_datei_app

def update_in_updates_ordner_uebertragen(app):
        updates_datei_app = os.path.join(app.paths.app, "resources", UPDATE_ORDNER_NAME_APP, "update.json")
        updates_datei_user = get_updates_datei_user()

        shutil.copy(updates_datei_app, updates_datei_user)
        
def get_help_file_path(app):
    return os.path.join(app.paths.app, "resources", "help.pdf")

def get_base_dir():
    return get_base_dir_path()

def get_settings():
    settings_file = get_settings_file_path()
    if os.path.exists(settings_file):
        with open(settings_file, "r") as file:
            return json.load(file)
    else:
        return {}
def set_settings(settings):
    settings_file = get_settings_file_path()
    with open(settings_file, "w") as file:
        json.dump(settings, file, indent=4)

def get_settings_file_path():
    settings_folder = ensure_folder_exists(SETTINGS_ORDNER)
    settings_file = os.path.join(settings_folder, "settings.json")
    return settings_file

def set_user_code(user_code):
    settings = get_settings()
    settings["user_code"] = user_code
    set_settings(settings)

def set_api_key(api_key):
    settings = get_settings()
    settings["api_key"] = api_key
    set_settings(settings)

def audio_zu_text_konvertieren(audio_dateipfad):
    # wenn verwendet wir muss openai-whisper installiert sein
    import whisper

    model = whisper.load_model("base")
    result = model.transcribe(audio_dateipfad)
    return result["text"]

def load_settings():
    settings_file = get_settings_file_path()
    if os.path.exists(settings_file):
        with open(settings_file, "r") as file:
            return json.load(file)
    else:
        return {}


def measure_execution_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        #print(f"Die Funktion '{func.__name__}' hat {execution_time:.2f} Sekunden gedauert.")
        return result
    return wrapper

def ermittel_den_aktuellen_monat_als_deutsches_wort(monat_offset=0):
    """
    Ermittelt den Monat relativ zum aktuellen Monat als Zahl und gibt den entsprechenden deutschen Monatsnamen zurück.

    Args:
        monat_offset (int, optional): Die Anzahl der Monate, die zum aktuellen Monat addiert werden sollen. Standard ist 0.

    Returns:
        str: Der ermittelte Monat auf Deutsch (z.B. "Januar", "Februar", ...).
    """
    # Erstelle ein Dictionary, das die Monatszahlen auf die deutschen Monatsnamen abbildet
    monatsnamen = {
        1: "Januar",
        2: "Februar",
        3: "März",
        4: "April",
        5: "Mai",
        6: "Juni",
        7: "Juli",
        8: "August",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Dezember"
    }

    # Ermittle den aktuellen Monat als Zahl
    aktueller_monat_als_zahl = datetime.now().month

    # Addiere den Offset zum aktuellen Monat
    ziel_monat = (aktueller_monat_als_zahl + monat_offset) % 12
    if ziel_monat == 0:
        ziel_monat = 12

    # Gib den entsprechenden deutschen Monatsnamen zurück
    return monatsnamen[ziel_monat]

"""
#TODO #96 Veralgemeinern
def update_daten_in_basis_ordner_uebertragen(app):
    kundendaten_ordner_app = os.path.join(app.paths.app, "resources", KUNDENDATEN_ORDNER_APP)
    basis_ordner_user = get_base_dir()  # Angenommen, diese Funktion gibt den Basisordner des Benutzers zurück
    archiv_ordner = os.path.join(basis_ordner_user,ARCHIV_ORDNER, "archivierte_anwalt_daten")
    ziel_json_datei_name = "lawyer_details.json"
    update_datei_name = "update_lawyer_details.json"

    ziel_datei_pfad = os.path.join(basis_ordner_user, ziel_json_datei_name)
    update_datei_pfad = os.path.join(kundendaten_ordner_app, update_datei_name)

    # Stelle sicher, dass der Archivordner existiert
    if not os.path.exists(archiv_ordner):
        os.makedirs(archiv_ordner)

    # Überprüfe, ob die Datei lawyer_details.json bereits im Zielordner existiert
    if os.path.isfile(ziel_datei_pfad):
        # Wenn ja, und update_lawyer_details.json ist vorhanden, archiviere die alte Datei
        if os.path.isfile(update_datei_pfad):
            # Generiere einen eindeutigen Namen für die archivierte Datei
            datumsanhang = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            archivierte_datei_name = f"lawyer_details_{datumsanhang}.json"
            archivierte_datei_pfad = os.path.join(archiv_ordner, archivierte_datei_name)

            # Verschiebe die alte lawyer_details.json in den Archivordner
            shutil.move(ziel_datei_pfad, archivierte_datei_pfad)

            # Kopiere die update_lawyer_details.json in den Zielordner und benenne sie um
            shutil.copy(update_datei_pfad, ziel_datei_pfad)

    else:
        # Wenn keine lawyer_details.json im Zielordner, kopiere diese aus dem Kundendatenordner, falls vorhanden
        source_datei_pfad = os.path.join(kundendaten_ordner_app, ziel_json_datei_name)
        if os.path.isfile(source_datei_pfad):
            shutil.copy(source_datei_pfad, ziel_datei_pfad)
            
def vorlagen_in_vorlagen_ordner_uebertragen(app):
    vorlagen_ordner_app = os.path.join(app.paths.app, "resources", KUNDENDATEN_ORDNER_APP, VORLAGEN_ORDNER_APP)
    vorlagen_ordner_user = get_template_folder()  # Annahme, dass diese Funktion das Benutzerverzeichnis für Vorlagen zurückgibt
    archiv_ordner = os.path.join(vorlagen_ordner_user, ARCHIV_ORDNER)
    placeholder_file_name = "placeholder.txt"

    # Stelle sicher, dass der Archivordner existiert
    if not os.path.exists(archiv_ordner):
        os.makedirs(archiv_ordner)

    # Überprüfe, ob der Vorlagenordner existiert
    if not os.path.isdir(vorlagen_ordner_app):
        return  # Beende die Funktion, wenn der Ordner nicht existiert

    for file in os.listdir(vorlagen_ordner_app):
        if file == placeholder_file_name:
            continue  # Ignoriere die Platzhalterdatei

        vorlage_app_pfad = os.path.join(vorlagen_ordner_app, file)
        neuer_name_ohne_update = file.replace("update_", "")
        vorlage_user_pfad = os.path.join(vorlagen_ordner_user, neuer_name_ohne_update)

        # Wenn es sich um eine Update-Datei handelt ODER keine Datei im Benutzerverzeichnis existiert, führe den Kopiervorgang durch
        if file.startswith("update_") or not os.path.exists(vorlage_user_pfad):
            if os.path.exists(vorlage_user_pfad):
                # Archiviere die existierende Datei, bevor sie durch die Update-Datei ersetzt wird
                basisname, erweiterung = os.path.splitext(neuer_name_ohne_update)
                datumsanhang = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                archivierte_datei_name = f"{basisname}_{datumsanhang}{erweiterung}"
                shutil.move(vorlage_user_pfad, os.path.join(archiv_ordner, archivierte_datei_name))
            
            # Kopiere die Vorlage oder aktualisierte Vorlage in das Benutzerverzeichnis
            shutil.copy(vorlage_app_pfad, vorlage_user_pfad)

            if file.startswith("update_"):
                # Umbenennen der "update_"-Datei im Anwendungsordner, indem das "update_" Präfix entfernt wird
                neuer_app_pfad_ohne_update = os.path.join(vorlagen_ordner_app, neuer_name_ohne_update)
                os.rename(vorlage_app_pfad, neuer_app_pfad_ohne_update)
"""




#LaunchPad

def ermittel_den_aktuellen_monat_als_deutsches_wort(monat_offset=0):
    """
    Ermittelt den Monat relativ zum aktuellen Monat als Zahl und gibt den entsprechenden deutschen Monatsnamen zurück.

    Args:
        monat_offset (int, optional): Die Anzahl der Monate, die zum aktuellen Monat addiert werden sollen. Standard ist 0.

    Returns:
        str: Der ermittelte Monat auf Deutsch (z.B. "Januar", "Februar", ...).
    """
    # Erstelle ein Dictionary, das die Monatszahlen auf die deutschen Monatsnamen abbildet
    monatsnamen = {
        1: "Januar",
        2: "Februar",
        3: "März",
        4: "April",
        5: "Mai",
        6: "Juni",
        7: "Juli",
        8: "August",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Dezember"
    }

    # Ermittle den aktuellen Monat als Zahl
    aktueller_monat_als_zahl = datetime.now().month

    # Addiere den Offset zum aktuellen Monat
    ziel_monat = (aktueller_monat_als_zahl + monat_offset) % 12
    if ziel_monat == 0:
        ziel_monat = 12

    # Gib den entsprechenden deutschen Monatsnamen zurück
    return monatsnamen[ziel_monat]

#LAW

import json
import requests
from requests.auth import HTTPBasicAuth
import logging
import os
import uuid
import shutil
from {{ cookiecutter.app_name|lower|replace('-', '_') }}.CONSTANTS import TEMP_FOLDER, BASE_DIR,MANDATEN_ORDNER_NAME,KUNDENDATEN_ORDNER_APP, UPDATE_ORDNER_NAME_APP, UPDATE_ORDNER_NAME_USER,VORLAGEN_ORDNER_APP, ARCHIV_ORDNER
from datetime import datetime
import subprocess
import platform

from {{ cookiecutter.app_name|lower|replace('-', '_') }}.utils import (
    ensure_beweismittel_OWi_data_file_exists,
    ensure_beweismittel_Scheidung_data_file_exists,
    ensure_data_file_exists,
    ensure_lawyer_data_file_exists,
    get_base_dir_path,
    get_ausfuehrungen_file_path,
    get_beweismittel_OWi_data_file_path,
    get_beweismittel_Scheidung_data_file_path,
    get_lawyer_data_file_path,
    ensure_folder_exists,
    get_login_information,
    set_login_information,
)



def set_beweismittel_data_Scheidung(beweismittel_data):
    ensure_beweismittel_Scheidung_data_file_exists()
    file_path = get_beweismittel_Scheidung_data_file_path()
    with open(file_path, "w") as f:
        json.dump(beweismittel_data, f, indent=4)


def get_beweismittel_data_scheidung():
    ensure_beweismittel_Scheidung_data_file_exists()
    file_path = get_beweismittel_Scheidung_data_file_path()
    with open(file_path, "r") as f:
        return json.load(f)
    
def set_beweismittel_data_OWi(beweismittel_data):
    ensure_beweismittel_OWi_data_file_exists()
    file_path = get_beweismittel_OWi_data_file_path()
    with open(file_path, "w") as f:
        json.dump(beweismittel_data, f, indent=4)


def get_beweismittel_data_OWi():
    ensure_beweismittel_OWi_data_file_exists()
    file_path = get_beweismittel_OWi_data_file_path()
    with open(file_path, "r") as f:
        return json.load(f)



def set_lawyer_data(lawyer_data):
    ensure_lawyer_data_file_exists()
    file_path = get_lawyer_data_file_path()
    with open(file_path, "w") as f:
        json.dump(lawyer_data, f, indent=4)


def get_lawyer_data():
    ensure_lawyer_data_file_exists()
    file_path = get_lawyer_data_file_path()
    with open(file_path, "r") as f:
        return json.load(f)


def setup_folders():
    ensure_folder_exists(get_template_folder())
    ensure_folder_exists(get_temp_folder())
    ensure_folder_exists(get_mandanten_folder())
    versionsordner_erstellen()


def vorlagen_in_vorlagen_ordner_uebertragen(app):
    vorlagen_ordner_app = os.path.join(app.paths.app, "resources", KUNDENDATEN_ORDNER_APP, VORLAGEN_ORDNER_APP)
    vorlagen_ordner_user = get_template_folder()  # Annahme, dass diese Funktion das Benutzerverzeichnis für Vorlagen zurückgibt
    archiv_ordner = os.path.join(vorlagen_ordner_user, ARCHIV_ORDNER)
    placeholder_file_name = "placeholder.txt"

    # Stelle sicher, dass der Archivordner existiert
    if not os.path.exists(archiv_ordner):
        os.makedirs(archiv_ordner)

    # Überprüfe, ob der Vorlagenordner existiert
    if not os.path.isdir(vorlagen_ordner_app):
        return  # Beende die Funktion, wenn der Ordner nicht existiert

    for file in os.listdir(vorlagen_ordner_app):
        if file == placeholder_file_name:
            continue  # Ignoriere die Platzhalterdatei

        vorlage_app_pfad = os.path.join(vorlagen_ordner_app, file)
        neuer_name_ohne_update = file.replace("update_", "")
        vorlage_user_pfad = os.path.join(vorlagen_ordner_user, neuer_name_ohne_update)

        # Wenn es sich um eine Update-Datei handelt ODER keine Datei im Benutzerverzeichnis existiert, führe den Kopiervorgang durch
        if file.startswith("update_") or not os.path.exists(vorlage_user_pfad):
            if os.path.exists(vorlage_user_pfad):
                # Archiviere die existierende Datei, bevor sie durch die Update-Datei ersetzt wird
                basisname, erweiterung = os.path.splitext(neuer_name_ohne_update)
                datumsanhang = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                archivierte_datei_name = f"{basisname}_{datumsanhang}{erweiterung}"
                shutil.move(vorlage_user_pfad, os.path.join(archiv_ordner, archivierte_datei_name))
            
            # Kopiere die Vorlage oder aktualisierte Vorlage in das Benutzerverzeichnis
            shutil.copy(vorlage_app_pfad, vorlage_user_pfad)

            if file.startswith("update_"):
                # Umbenennen der "update_"-Datei im Anwendungsordner, indem das "update_" Präfix entfernt wird
                neuer_app_pfad_ohne_update = os.path.join(vorlagen_ordner_app, neuer_name_ohne_update)
                os.rename(vorlage_app_pfad, neuer_app_pfad_ohne_update)

def anwalt_liste_in_basis_ordner_uebertragen(app):
    kundendaten_ordner_app = os.path.join(app.paths.app, "resources", KUNDENDATEN_ORDNER_APP)
    basis_ordner_user = get_base_dir()  # Angenommen, diese Funktion gibt den Basisordner des Benutzers zurück
    archiv_ordner = os.path.join(basis_ordner_user,ARCHIV_ORDNER, "archivierte_anwalt_daten")
    name_der_anwalt_daten_json_datei = "lawyer_details.json"
    update_datei_name = "update_lawyer_details.json"

    ziel_datei_pfad = os.path.join(basis_ordner_user, name_der_anwalt_daten_json_datei)
    update_datei_pfad = os.path.join(kundendaten_ordner_app, update_datei_name)

    # Stelle sicher, dass der Archivordner existiert
    if not os.path.exists(archiv_ordner):
        os.makedirs(archiv_ordner)

    # Überprüfe, ob die Datei lawyer_details.json bereits im Zielordner existiert
    if os.path.isfile(ziel_datei_pfad):
        # Wenn ja, und update_lawyer_details.json ist vorhanden, archiviere die alte Datei
        if os.path.isfile(update_datei_pfad):
            # Generiere einen eindeutigen Namen für die archivierte Datei
            datumsanhang = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            archivierte_datei_name = f"lawyer_details_{datumsanhang}.json"
            archivierte_datei_pfad = os.path.join(archiv_ordner, archivierte_datei_name)

            # Verschiebe die alte lawyer_details.json in den Archivordner
            shutil.move(ziel_datei_pfad, archivierte_datei_pfad)

            # Kopiere die update_lawyer_details.json in den Zielordner und benenne sie um
            shutil.copy(update_datei_pfad, ziel_datei_pfad)

    else:
        # Wenn keine lawyer_details.json im Zielordner, kopiere diese aus dem Kundendatenordner, falls vorhanden
        source_datei_pfad = os.path.join(kundendaten_ordner_app, name_der_anwalt_daten_json_datei)
        if os.path.isfile(source_datei_pfad):
            shutil.copy(source_datei_pfad, ziel_datei_pfad)


def get_temp_folder():
    temp_folder_path = os.path.join(os.path.expanduser("~"), BASE_DIR, TEMP_FOLDER)
    ensure_folder_exists(temp_folder_path)
    return temp_folder_path

def get_base_dir():
    return get_base_dir_path()

def get_template_folder():
    template_folder_path = os.path.join(
        os.path.expanduser("~"), BASE_DIR, VORLAGEN_ORDNER_APP
    )
    ensure_folder_exists(template_folder_path)
    return template_folder_path

def get_update_folder():
    update_folder_path = os.path.join(
        os.path.expanduser("~"), BASE_DIR, UPDATE_ORDNER_NAME
    )
    ensure_folder_exists(update_folder_path)
    return update_folder_path

def get_mandanten_folder():
    mandanten_folder_path = os.path.join(
        os.path.expanduser("~"), BASE_DIR, MANDATEN_ORDNER_NAME
    )
    ensure_folder_exists(mandanten_folder_path)
    return mandanten_folder_path

def get_temp_file_for_template_file(template_file):
    source_path = os.path.join(get_template_folder(), template_file)

    if not os.path.exists(source_path):
        logging.error(f"Template file does not exist: {source_path}")
        raise FileNotFoundError(f"Template file does not exist: {source_path}")

    # Generate a unique temporary file name
    unique_filename = f"{uuid.uuid4()}_{template_file}"
    temp_file_path = os.path.join(get_temp_folder(), unique_filename)

    # Copy the template to a temporary file and return its path
    try:
        shutil.copyfile(source_path, temp_file_path)
        return temp_file_path
    except IOError as e:
        logging.error(f"Failed to create a temporary file from template: {e}")
        raise



def print_paragraph_details(paragraph):
    print("This is one paragraph:")
    if paragraph.text:
        print(f"Text: {paragraph.text}")
    if paragraph.style:
        print(f"Style: {paragraph.style.name}")
    if paragraph.alignment:
        print(f"Alignment: {paragraph.alignment}")
    if paragraph.contains_page_break:
        print(f"Contains page break: {paragraph.contains_page_break}")
    if paragraph.hyperlinks:
        print(f"Hyperlinks: {paragraph.hyperlinks}")
    if paragraph.paragraph_format:
        print("Paragraph format details:")
        format = paragraph.paragraph_format
        if format.alignment:
            print(f"    Alignment: {format.alignment}")
        if format.keep_together:
            print(f"    Keep together: {format.keep_together}")
        if format.keep_with_next:
            print(f"    Keep with next: {format.keep_with_next}")
        if format.left_indent:
            print(f"    Left indent: {format.left_indent}")
        if format.line_spacing:
            print(f"    Line spacing: {format.line_spacing}")
        if format.line_spacing_rule:
            print(f"    Line spacing rule: {format.line_spacing_rule}")
        if format.page_break_before:
            print(f"    Page break before: {format.page_break_before}")
        if format.right_indent:
            print(f"    Right indent: {format.right_indent}")
        if format.space_after:
            print(f"    Space after: {format.space_after}")
        if format.space_before:
            print(f"    Space before: {format.space_before}")
        if format.tab_stops:
            print("    Tab stops:")
            for tabstop in format.tab_stops:
                print(f"        Alignment: {tabstop.alignment}")
                print(f"        Leader: {tabstop.leader}")
                print(f"        Position: {tabstop.position}")
        if format.widow_control:
            print(f"    Widow control: {format.widow_control}")
    if paragraph.runs:
        print("Runs:")
        for run in paragraph.runs:
            if run.text:
                print(f"    Text: {run.text}")
            if run.bold:
                print(f"    Bold: {run.bold}")
            if run.italic:
                print(f"    Italic: {run.italic}")
            if run.underline:
                print(f"    Underline: {run.underline}")
            if run.font:
                if run.font.name:
                    print(f"    Font name: {run.font.name}")
                if run.font.size:
                    print(f"    Font size: {run.font.size}")    

def datenabfrage_datev_for_aktenzeichen(aktenzeichen:str, passwort:str):
    url = 'https://localhost:58452/datev/api/law/v1/files/'
    params = {
        'select': 'id, name, number',
        'filter': f"file_number eq '{aktenzeichen}'",  # Verwendung eines f-Strings zur Einsetzung
        'orderby': 'my_property_name desc,other_property_name asc',
        'top': '100',
        'skip': '10'
    }
    headers = {
        'accept': 'application/json; charset=utf-8'
    }
    # Ersetzen Sie 'your_username' und 'your_password' mit Ihren tatsächlichen Anmeldedaten
    username = get_nutzername()
    auth = HTTPBasicAuth(username, passwort)

    response = requests.get(url, params=params, headers=headers, auth=auth, verify=False)
    
    if response.status_code == 200:
        return response.json()  # Gibt das JSON-Antwortobjekt zurück
    else:
        return f"Error: {response.status_code}"

def get_nutzername():
    login_information = get_login_information()
    return login_information["username"]

def set_nutzername(nutzername):
    login_information = get_login_information()
    login_information["username"] = nutzername
    set_login_information(login_information)

def get_datev_example_data():
    return [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "file_number_short": "000001-05",
                    "file_number": "000001-2005/001:00",
                    "file_name": "Insolvenzverfahren Mustermann",
                    "project_number": "123/331-12",
                    "short_reason": "Beratung",
                    "long_reason": "vacnatocbosa",
                    "department": {
                    "id": "ebd93cfc-1c2e-4927-aee5-24b448b050fd",
                    "link": "https://localhost:58452/datev/api/law/v1/departments/ebd93cfc-1c2e-4927-aee5-24b448b050fd"
                    },
                    "causes": [
                    {
                        "id": "051534f8-7b78-441a-aa9e-6f708b49d855",
                        "number": 3,
                        "name": "Forderung aus Warenlieferung",
                        "department_id": "ebd93cfc-1c2e-4927-aee5-24b448b050fd",
                        "department_link": "https://localhost:58452/datev/api/law/v1/departments/ebd93cfc-1c2e-4927-aee5-24b448b050fd"
                    },
                    {
                        "id": "051534f8-7b78-441a-aa9e-6f708b49d855",
                        "number": 15,
                        "name": "sonstige zivilrechtliche Ansprüche",
                        "department_id": "e5a91019-af4d-4373-a18c-36e64e4ec478",
                        "department_link": "https://localhost:58452/datev/api/law/v1/departments/e5a91019-af4d-4373-a18c-36e64e4ec478"
                    }
                    ],
                    "partner": {
                    "id": "c015c071-43c4-432f-be80-508d54c720e7",
                    "number": 62,
                    "display_name": "Ernst Exempeladvokat",
                    "link": "https://localhost:58452/datev/api/law/v1/employees/c015c071-43c4-432f-be80-508d54c720e7"
                    },
                    "case_handlers": [
                    {
                        "id": "c015c071-43c4-432f-be80-508d54c720e7",
                        "number": 62,
                        "display_name": "Ernst Exempeladvokat",
                        "primary_case_handler": true,
                        "commission": 100,
                        "employee_id": "f8586db2-4f22-44af-8cec-16f426bd5440",
                        "employee_link": "http://localhost:58454/datev/api/master-data/v1/employees/f8586db2-4f22-44af-8cec-16f426bd5440"
                    }
                    ],
                    "security_zone": {
                    "id": "174ddc49-e8c4-466b-8c35-d8eef5d655b6",
                    "short_name": "SB-0",
                    "name": "Öffentliche Akten"
                    },
                    "establishment": {
                    "number": 1,
                    "name": "Musterniederlassung",
                    "link": "http://localhost:58454/datev/api/master-data/v1/corporate-structures/3fa85f64-5717-4562-b3fc-2c963f66afa6/establishments/59bb1870-5e0a-4ce9-bb7d-42e95f5cdb4e",
                    "organization": {
                        "id": "2da7f880-6c24-44cd-be38-32746a268b0f",
                        "number": 1,
                        "name": "Musterkanzlei",
                        "link": "http://localhost:58454/datev/api/master-data/v1/corporate-structures/3fa85f64-5717-4562-b3fc-2c963f66afa6"
                    }
                    },
                    "economic_data": {
                    "cause_value": {
                        "amount": 20000,
                        "currency": "EUR"
                    },
                    "budget": {
                        "amount": 10000,
                        "currency": "EUR"
                    },
                    "budget_timespan": "total",
                    "base_currency": "EUR"
                    },
                    "accounting_area": {
                    "id": "7447f931-b42e-4e71-84f3-1319a49fb076",
                    "number": 1,
                    "name": "Standardbuchungskreis",
                    "link": "https://localhost:58452/datev/api/law/v1/accounting-areas/7447f931-b42e-4e71-84f3-1319a49fb076"
                    },
                    "reactivated": false,
                    "filing": {
                    "date": "2019-08-12",
                    "number": "000001-2005",
                    "retention_period_end": "2029-08-12",
                    "location": "Keller"
                    },
                    "note": "umamonabp",
                    "created": {
                    "date": "2018-09-27",
                    "creator": "Ernst Exempeladvokat"
                    },
                    "modified": {
                    "date": "2019-08-11",
                    "creator": "Ernst Exempeladvokat"
                    }
                },
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "file_number_short": "000001-05",
                    "file_number": "000001-2005/001:00",
                    "file_name": "Insolvenzverfahren Mustermann",
                    "project_number": "123/331-12",
                    "short_reason": "Beratung",
                    "long_reason": "morigejofo",
                    "department": {
                    "id": "ebd93cfc-1c2e-4927-aee5-24b448b050fd",
                    "link": "https://localhost:58452/datev/api/law/v1/departments/ebd93cfc-1c2e-4927-aee5-24b448b050fd"
                    },
                    "causes": [
                    {
                        "id": "051534f8-7b78-441a-aa9e-6f708b49d855",
                        "number": 3,
                        "name": "Forderung aus Warenlieferung",
                        "department_id": "ebd93cfc-1c2e-4927-aee5-24b448b050fd",
                        "department_link": "https://localhost:58452/datev/api/law/v1/departments/ebd93cfc-1c2e-4927-aee5-24b448b050fd"
                    },
                    {
                        "id": "051534f8-7b78-441a-aa9e-6f708b49d855",
                        "number": 15,
                        "name": "sonstige zivilrechtliche Ansprüche",
                        "department_id": "e5a91019-af4d-4373-a18c-36e64e4ec478",
                        "department_link": "https://localhost:58452/datev/api/law/v1/departments/e5a91019-af4d-4373-a18c-36e64e4ec478"
                    }
                    ],
                    "partner": {
                    "id": "c015c071-43c4-432f-be80-508d54c720e7",
                    "number": 62,
                    "display_name": "Ernst Exempeladvokat",
                    "link": "https://localhost:58452/datev/api/law/v1/employees/c015c071-43c4-432f-be80-508d54c720e7"
                    },
                    "case_handlers": [
                    {
                        "id": "c015c071-43c4-432f-be80-508d54c720e7",
                        "number": 62,
                        "display_name": "Ernst Exempeladvokat",
                        "primary_case_handler": true,
                        "commission": 100,
                        "employee_id": "f8586db2-4f22-44af-8cec-16f426bd5440",
                        "employee_link": "http://localhost:58454/datev/api/master-data/v1/employees/f8586db2-4f22-44af-8cec-16f426bd5440"
                    }
                    ],
                    "security_zone": {
                    "id": "174ddc49-e8c4-466b-8c35-d8eef5d655b6",
                    "short_name": "SB-0",
                    "name": "Öffentliche Akten"
                    },
                    "establishment": {
                    "number": 1,
                    "name": "Musterniederlassung",
                    "link": "http://localhost:58454/datev/api/master-data/v1/corporate-structures/3fa85f64-5717-4562-b3fc-2c963f66afa6/establishments/59bb1870-5e0a-4ce9-bb7d-42e95f5cdb4e",
                    "organization": {
                        "id": "2da7f880-6c24-44cd-be38-32746a268b0f",
                        "number": 1,
                        "name": "Musterkanzlei",
                        "link": "http://localhost:58454/datev/api/master-data/v1/corporate-structures/3fa85f64-5717-4562-b3fc-2c963f66afa6"
                    }
                    },
                    "economic_data": {
                    "cause_value": {
                        "amount": 20000,
                        "currency": "EUR"
                    },
                    "budget": {
                        "amount": 10000,
                        "currency": "EUR"
                    },
                    "budget_timespan": "total",
                    "base_currency": "EUR"
                    },
                    "accounting_area": {
                    "id": "7447f931-b42e-4e71-84f3-1319a49fb076",
                    "number": 1,
                    "name": "Standardbuchungskreis",
                    "link": "https://localhost:58452/datev/api/law/v1/accounting-areas/7447f931-b42e-4e71-84f3-1319a49fb076"
                    },
                    "reactivated": false,
                    "filing": {
                    "date": "2019-08-12",
                    "number": "000001-2005",
                    "retention_period_end": "2029-08-12",
                    "location": "Keller"
                    },
                    "note": "supvujsekdiras",
                    "created": {
                    "date": "2018-09-27",
                    "creator": "Ernst Exempeladvokat"
                    },
                    "modified": {
                    "date": "2019-08-11",
                    "creator": "Ernst Exempeladvokat"
                    }
                },
                {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "file_number_short": "000001-05",
                "file_number": "000001-2005/001:00",
                "file_name": "Insolvenzverfahren Mustermann",
                "project_number": "123/331-12",
                "short_reason": "Beratung",
                "long_reason": "tanejomeve",
                "department": {
                "id": "ebd93cfc-1c2e-4927-aee5-24b448b050fd",
                "link": "https://localhost:58452/datev/api/law/v1/departments/ebd93cfc-1c2e-4927-aee5-24b448b050fd"
                },
                "causes": [
                {
                    "id": "051534f8-7b78-441a-aa9e-6f708b49d855",
                    "number": 3,
                    "name": "Forderung aus Warenlieferung",
                    "department_id": "ebd93cfc-1c2e-4927-aee5-24b448b050fd",
                    "department_link": "https://localhost:58452/datev/api/law/v1/departments/ebd93cfc-1c2e-4927-aee5-24b448b050fd"
                },
                {
                    "id": "051534f8-7b78-441a-aa9e-6f708b49d855",
                    "number": 15,
                    "name": "sonstige zivilrechtliche Ansprüche",
                    "department_id": "e5a91019-af4d-4373-a18c-36e64e4ec478",
                    "department_link": "https://localhost:58452/datev/api/law/v1/departments/e5a91019-af4d-4373-a18c-36e64e4ec478"
                }
                ],
                "partner": {
                "id": "c015c071-43c4-432f-be80-508d54c720e7",
                "number": 62,
                "display_name": "Ernst Exempeladvokat",
                "link": "https://localhost:58452/datev/api/law/v1/employees/c015c071-43c4-432f-be80-508d54c720e7"
                },
                "case_handlers": [
                {
                    "id": "c015c071-43c4-432f-be80-508d54c720e7",
                    "number": 62,
                    "display_name": "Ernst Exempeladvokat",
                    "primary_case_handler": true,
                    "commission": 100,
                    "employee_id": "f8586db2-4f22-44af-8cec-16f426bd5440",
                    "employee_link": "http://localhost:58454/datev/api/master-data/v1/employees/f8586db2-4f22-44af-8cec-16f426bd5440"
                }
                ],
                "security_zone": {
                "id": "174ddc49-e8c4-466b-8c35-d8eef5d655b6",
                "short_name": "SB-0",
                "name": "Öffentliche Akten"
                },
                "establishment": {
                "number": 1,
                "name": "Musterniederlassung",
                "link": "http://localhost:58454/datev/api/master-data/v1/corporate-structures/3fa85f64-5717-4562-b3fc-2c963f66afa6/establishments/59bb1870-5e0a-4ce9-bb7d-42e95f5cdb4e",
                "organization": {
                    "id": "2da7f880-6c24-44cd-be38-32746a268b0f",
                    "number": 1,
                    "name": "Musterkanzlei",
                    "link": "http://localhost:58454/datev/api/master-data/v1/corporate-structures/3fa85f64-5717-4562-b3fc-2c963f66afa6"
                }
                },
                "economic_data": {
                "cause_value": {
                    "amount": 20000,
                    "currency": "EUR"
                },
                "budget": {
                    "amount": 10000,
                    "currency": "EUR"
                },
                "budget_timespan": "total",
                "base_currency": "EUR"
                },
                "accounting_area": {
                "id": "7447f931-b42e-4e71-84f3-1319a49fb076",
                "number": 1,
                "name": "Standardbuchungskreis",
                "link": "https://localhost:58452/datev/api/law/v1/accounting-areas/7447f931-b42e-4e71-84f3-1319a49fb076"
                },
                "reactivated": false,
                "filing": {
                "date": "2019-08-12",
                "number": "000001-2005",
                "retention_period_end": "2029-08-12",
                "location": "Keller"
                },
                "note": "tuhoweswurisa",
                "created": {
                "date": "2018-09-27",
                "creator": "Ernst Exempeladvokat"
                },
                "modified": {
                "date": "2019-08-11",
                "creator": "Ernst Exempeladvokat"
                }
            }
    ]

def hinzufuegen_anwaltsdaten_zum_kontext(kontext, anwalt_json=None):
    
    if anwalt_json is None:
        anwalt_json = get_lawyer_data()
    
    # Hier werden die Anwaltsdetails aus der anwalt_json extrahiert
    anwalt_details = anwalt_json.get('lawyer_details', {})
    kontext['ANWÄLTE'] = [
        {
            'NAME': details.get('name', ''),
            'FACHGEBIETE': details.get('specialty', '').split('; ') if details.get('specialty') else []
        }
        for anwalt_id, details in anwalt_details.items()
    ]
    return kontext



def add_ausfuehrung(reference, kundenprogramm_ID, antrags_name):
    ensure_data_file_exists()
    new_ausfuehrung = {
        "id": str(uuid.uuid4()),
        "reference": reference,
        "kundenprogramm_ID": kundenprogramm_ID,
        "datum": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "antrags_name": antrags_name,
        "fehlerhaft": False
    }
    with open(get_ausfuehrungen_file_path(), "r+") as file:
        data = json.load(file)
        data.append(new_ausfuehrung)
        file.seek(0)
        json.dump(data, file, indent=4)
        
def mark_ausfuehrung_as_fehlerhaft(ausfuehrung_id):
    ensure_data_file_exists()
    with open(get_ausfuehrungen_file_path(), "r+") as file:
        data = json.load(file)
        for ausfuehrung in data:
            if ausfuehrung["id"] == ausfuehrung_id:
                ausfuehrung["fehlerhaft"] = True
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)


def open_file(file_path):
    if file_path:
        try:
            if platform.system() == "Windows":
                subprocess.run(["explorer", file_path], check=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", file_path], check=True)
            else:  # Assuming Linux
                subprocess.run(["xdg-open", file_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error opening file: {e}")
    else:
        print("File path is not set. Unable to open file.")
        
def get_help_file_path(app):
    return os.path.join(app.paths.app, "resources", "help.pdf")

def get_updates_datei_user():
    #ich möchte den dateipfad der update.json datei aus dem updates ordner haben, welcher im updates ordner im user verzeichnis liegt
    updates_dateipfad_user = os.path.join(os.path.expanduser("~"), get_base_dir(), UPDATE_ORDNER_NAME_USER, "update.json")
    return updates_dateipfad_user

def get_updates_pdf_path(app):
    updates_pdf_dateipfad = os.path.join(app.paths.app, "resources", "update.pdf")
    return updates_pdf_dateipfad

def update_daten_laden_user():
        file_path = get_updates_datei_user()
        with open(file_path, "r") as f:
            return json.load(f)
        
def update_daten_laden_app(app):
        file_path = get_updates_datei_app(app)
        with open(file_path, "r") as f:
            return json.load(f)
        
def get_updates_datei_app(app):
    updates_datei_app = os.path.join(app.paths.app, "resources", UPDATE_ORDNER_NAME_APP, "update.json")
    return updates_datei_app

def update_in_updates_ordner_uebertragen(app):
        updates_datei_app = os.path.join(app.paths.app, "resources", UPDATE_ORDNER_NAME_APP, "update.json")
        updates_datei_user = get_updates_datei_user()

        shutil.copy(updates_datei_app, updates_datei_user)

def versionsordner_erstellen():
        folder_name = UPDATE_ORDNER_NAME_USER
        ensure_folder_exists(folder_name)