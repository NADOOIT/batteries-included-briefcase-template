import shutil
from datetime import datetime
import os

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