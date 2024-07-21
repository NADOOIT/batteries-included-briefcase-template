from requests.auth import HTTPBasicAuth
import platform
from datetime import datetime
import json

def set_beweismittel_data_OWi(beweismittel_data):
    ensure_beweismittel_OWi_data_file_exists()
    file_path = get_beweismittel_OWi_data_file_path()
    with open(file_path, "w") as f:
        json.dump(beweismittel_data, f, indent=4)