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
from cookiecutter.repository import is_repo_url

def get_login_information():
    ensure_login_information_file_exists()
    file_path = get_login_information_file_path()
    with open(file_path, "r") as f:
        return json.load(f)