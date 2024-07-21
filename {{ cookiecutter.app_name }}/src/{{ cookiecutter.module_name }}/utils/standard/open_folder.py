import re
import platform
from cookiecutter.main import cookiecutter
import unicodedata
from cookiecutter import exceptions as cookiecutter_exceptions
from briefcase.exceptions import (
    InvalidTemplateRepository,
    NetworkFailure,
    TemplateUnsupportedVersion,
    BriefcaseCommandError,
)
import subprocess
from cookiecutter.repository import is_repo_url

def open_folder(self, widget):
    folder_path = self.folder_path  # Assuming this is the path you want to open
    try:
        if platform.system() == "Windows":
            subprocess.run(["explorer", folder_path], check=True)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", folder_path], check=True)
        else:  # Assuming Linux
            subprocess.run(["xdg-open", folder_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error opening folder: {e}")