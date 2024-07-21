import os
from cookiecutter.repository import is_repo_url
from briefcase.exceptions import (
    InvalidTemplateRepository,
    NetworkFailure,
    TemplateUnsupportedVersion,
    BriefcaseCommandError,
)

def get_base_dir_path():
    ensure_base_folder_exits()
    return os.path.join(os.path.expanduser("~"), BASE_DIR)