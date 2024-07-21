import os
from cookiecutter.repository import is_repo_url
from briefcase.exceptions import (
    InvalidTemplateRepository,
    NetworkFailure,
    TemplateUnsupportedVersion,
    BriefcaseCommandError,
)

def get_user_auth_data_file_path():
    base_dir = os.path.join(os.path.expanduser("~"), BASE_DIR)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    return os.path.join(base_dir, "user_auth_data.json")