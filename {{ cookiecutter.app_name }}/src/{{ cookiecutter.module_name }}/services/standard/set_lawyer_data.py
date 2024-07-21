from requests.auth import HTTPBasicAuth
import platform
from datetime import datetime
import json

def set_lawyer_data(lawyer_data):
    ensure_lawyer_data_file_exists()
    file_path = get_lawyer_data_file_path()
    with open(file_path, "w") as f:
        json.dump(lawyer_data, f, indent=4)