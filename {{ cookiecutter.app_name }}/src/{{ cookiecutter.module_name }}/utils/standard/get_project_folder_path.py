import os
from cookiecutter.repository import is_repo_url
from briefcase.exceptions import (
    InvalidTemplateRepository,
    NetworkFailure,
    TemplateUnsupportedVersion,
    BriefcaseCommandError,
)

def get_project_folder_path():
    home_dir = os.path.expanduser("~")
    project_folder = os.path.join(home_dir, "Documents", "GitHub")

    # Create the folder if it doesn't exist
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)

    return project_folder