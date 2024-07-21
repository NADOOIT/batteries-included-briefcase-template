import os

def get_update_folder():
    update_folder_path = os.path.join(
        os.path.expanduser("~"), BASE_DIR, UPDATE_ORDNER_NAME
    )
    ensure_folder_exists(update_folder_path)
    return update_folder_path