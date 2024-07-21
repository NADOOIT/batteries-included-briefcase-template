import json

def set_settings(settings):
    settings_file = get_settings_file_path()
    with open(settings_file, "w") as file:
        json.dump(settings, file, indent=4)