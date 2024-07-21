import os
import json

def get_settings():
    settings_file = get_settings_file_path()
    if os.path.exists(settings_file):
        with open(settings_file, "r") as file:
            return json.load(file)
    else:
        return {}