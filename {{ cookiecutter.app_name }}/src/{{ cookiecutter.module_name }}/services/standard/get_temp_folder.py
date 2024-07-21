import os

def get_temp_folder():
    temp_folder_path = os.path.join(os.path.expanduser("~"), BASE_DIR, TEMP_FOLDER)
    ensure_folder_exists(temp_folder_path)
    return temp_folder_path