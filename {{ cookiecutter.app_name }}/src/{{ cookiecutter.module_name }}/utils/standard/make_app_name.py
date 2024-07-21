import unicodedata
from cookiecutter.repository import is_repo_url
import re
from briefcase.exceptions import (
    InvalidTemplateRepository,
    NetworkFailure,
    TemplateUnsupportedVersion,
    BriefcaseCommandError,
)

def make_app_name(formal_name):
    """Construct a candidate app name from a formal name.

    :param formal_name: The formal name
    :returns: The candidate app name
    """
    normalized = unicodedata.normalize("NFKD", formal_name)
    stripped = re.sub("[^0-9a-zA-Z_]+", "", normalized).lstrip("_")
    if stripped:
        return stripped.lower()
    else:
        # If stripping removes all the content,
        # use a dummy app name as the suggestion.
        return "myapp"