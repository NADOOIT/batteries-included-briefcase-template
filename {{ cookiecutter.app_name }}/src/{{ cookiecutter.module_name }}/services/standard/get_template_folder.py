import os

def get_template_folder():
    template_folder_path = os.path.join(
        os.path.expanduser("~"), BASE_DIR, VORLAGEN_ORDNER_APP
    )
    ensure_folder_exists(template_folder_path)
    return template_folder_path