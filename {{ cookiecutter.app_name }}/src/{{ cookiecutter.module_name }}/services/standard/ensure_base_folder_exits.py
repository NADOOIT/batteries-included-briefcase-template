import os

def ensure_base_folder_exits():
    base_dir = os.path.join(os.path.expanduser("~"), BASE_DIR)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)