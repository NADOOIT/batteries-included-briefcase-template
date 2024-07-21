import shutil
from datetime import datetime
import os

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