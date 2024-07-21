import os

def ensure_folder_exists(folder_name):
    base_dir = get_base_dir_path()
    folder_path = os.path.join(base_dir, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path