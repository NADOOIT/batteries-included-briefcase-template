import os
import json
from cookiecutter.repository import is_repo_url
from briefcase.exceptions import (
    InvalidTemplateRepository,
    NetworkFailure,
    TemplateUnsupportedVersion,
    BriefcaseCommandError,
)

def ensure_data_file_exists():
    file_path = get_ausfuehrungen_file_path()
    if not os.path.isfile(file_path):
        with open(file_path, "w") as file:
            json.dump([], file)