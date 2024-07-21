from requests.auth import HTTPBasicAuth
import platform
from datetime import datetime
import json

def get_beweismittel_data_OWi():
    ensure_beweismittel_OWi_data_file_exists()
    file_path = get_beweismittel_OWi_data_file_path()
    with open(file_path, "r") as f:
        return json.load(f)