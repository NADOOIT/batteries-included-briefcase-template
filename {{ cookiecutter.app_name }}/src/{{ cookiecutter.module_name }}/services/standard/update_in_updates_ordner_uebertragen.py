import shutil
import os

def update_in_updates_ordner_uebertragen(app):
        updates_datei_app = os.path.join(app.paths.app, "resources", UPDATE_ORDNER_NAME_APP, "update.json")
        updates_datei_user = get_updates_datei_user()

        shutil.copy(updates_datei_app, updates_datei_user)