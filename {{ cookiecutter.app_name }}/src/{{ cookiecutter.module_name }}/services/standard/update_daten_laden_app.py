from requests.auth import HTTPBasicAuth
import platform
from datetime import datetime
import json

def update_daten_laden_app(app):
        file_path = get_updates_datei_app(app)
        with open(file_path, "r") as f:
            return json.load(f)