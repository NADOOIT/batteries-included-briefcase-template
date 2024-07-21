import os

def get_updates_datei_user():
    #ich möchte den dateipfad der update.json datei aus dem updates ordner haben, welcher im updates ordner im user verzeichnis liegt
    updates_dateipfad_user = os.path.join(os.path.expanduser("~"), get_base_dir(), UPDATE_ORDNER_NAME_USER, "update.json")
    return updates_dateipfad_user