import os

def get_settings_file_path():
    settings_folder = ensure_folder_exists(SETTINGS_ORDNER)
    settings_file = os.path.join(settings_folder, "settings.json")
    return settings_file