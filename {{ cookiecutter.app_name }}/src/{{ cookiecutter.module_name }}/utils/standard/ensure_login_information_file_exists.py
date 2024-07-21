from pathlib import Path
import platform
from cookiecutter.main import cookiecutter
import json
from cookiecutter import exceptions as cookiecutter_exceptions
from briefcase.exceptions import (
    InvalidTemplateRepository,
    NetworkFailure,
    TemplateUnsupportedVersion,
    BriefcaseCommandError,
)
import os
from cookiecutter.repository import is_repo_url

def ensure_login_information_file_exists():
    file_path = get_login_information_file_path()
    if not os.path.isfile(file_path):
        # Initialize the file with a dummy lawyer if it doesn't exist
        dummy_data = {
            "username": "Bitte DATEV-Nutzername eingeben",
                }
        with open(file_path, "w") as f:
            json.dump(dummy_data, f, indent=4)