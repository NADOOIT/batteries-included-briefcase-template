import os
from cookiecutter.repository import is_repo_url
from briefcase.exceptions import (
    InvalidTemplateRepository,
    NetworkFailure,
    TemplateUnsupportedVersion,
    BriefcaseCommandError,
)

def get_beweismittel_OWi_data_file_path():
    base_dir = get_base_dir_path()
    return os.path.join(base_dir, BEWEISMITTEL_OWI_DATA_FILE_NAME)