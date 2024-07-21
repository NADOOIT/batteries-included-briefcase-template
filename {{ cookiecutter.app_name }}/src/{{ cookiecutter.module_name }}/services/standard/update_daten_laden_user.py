from requests.auth import HTTPBasicAuth
import platform
from datetime import datetime
import json

def update_daten_laden_user():
        file_path = get_updates_datei_user()
        with open(file_path, "r") as f:
            return json.load(f)