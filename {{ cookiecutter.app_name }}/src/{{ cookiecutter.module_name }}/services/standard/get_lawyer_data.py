from requests.auth import HTTPBasicAuth
import platform
from datetime import datetime
import json

def get_lawyer_data():
    ensure_lawyer_data_file_exists()
    file_path = get_lawyer_data_file_path()
    with open(file_path, "r") as f:
        return json.load(f)