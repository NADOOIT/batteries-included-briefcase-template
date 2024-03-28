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

def set_user_code(user_code):
    settings = get_settings()
    settings["user_code"] = user_code
    set_settings(settings)

def set_api_key(api_key):
    settings = get_settings()
    settings["api_key"] = api_key
    set_settings(settings)

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