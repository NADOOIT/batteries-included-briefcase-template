from pathlib import Path
import platform
import uuid
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

def ensure_lawyer_data_file_exists():
    file_path = get_lawyer_data_file_path()
    if not os.path.isfile(file_path):
        # Initialize the file with a dummy lawyer if it doesn't exist
        dummy_data = {
            "selected_lawyer_id": str(uuid.uuid4()),
            "lawyer_details": {
                "dummy_id": {
                    "name": "Dummy Lawyer",
                    "email": "dummy@lawfirm.com",
                    "phone": "123-456-7890",
                    "fax": "098-765-4321",
                    "title": "Lawyer",
                    "specialty": "General",
                }
            },
        }
        with open(file_path, "w") as f:
            json.dump(dummy_data, f, indent=4)