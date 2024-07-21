import os

def get_help_file_path(app):
    return os.path.join(app.paths.app, "resources", "help.pdf")