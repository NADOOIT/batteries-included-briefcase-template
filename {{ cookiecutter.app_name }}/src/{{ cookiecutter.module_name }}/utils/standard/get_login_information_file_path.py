import os
from cookiecutter.repository import is_repo_url
from briefcase.exceptions import (
    InvalidTemplateRepository,
    NetworkFailure,
    TemplateUnsupportedVersion,
    BriefcaseCommandError,
)

def get_login_information_file_path():
    base_dir_path = get_base_dir_path()
    return os.path.join(base_dir_path, LOGIN_INFORMATION_FILE_NAME)