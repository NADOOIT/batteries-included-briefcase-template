import os

def get_updates_datei_app(app):
    updates_datei_app = os.path.join(app.paths.app, "resources", UPDATE_ORDNER_NAME_APP, "update.json")
    return updates_datei_app