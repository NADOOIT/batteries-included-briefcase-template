import os

def get_mandanten_folder():
    mandanten_folder_path = os.path.join(
        os.path.expanduser("~"), BASE_DIR, MANDATEN_ORDNER_NAME
    )
    ensure_folder_exists(mandanten_folder_path)
    return mandanten_folder_path