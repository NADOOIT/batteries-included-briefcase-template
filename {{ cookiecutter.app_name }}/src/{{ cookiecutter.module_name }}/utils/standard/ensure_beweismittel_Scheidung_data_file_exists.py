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

def ensure_beweismittel_Scheidung_data_file_exists():
    file_path = get_beweismittel_Scheidung_data_file_path()
    if not os.path.isfile(file_path):
        # Initialize the file with default data if it doesn't exist
        default_data = {
            "options": [
                "Geburtsurkunde",
                "Scheidungsfolgevereinbarung",
            ]
        }
        with open(file_path, "w") as f:
            json.dump(default_data, f, indent=4)