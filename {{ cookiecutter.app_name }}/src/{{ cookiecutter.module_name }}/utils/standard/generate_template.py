import re
from cookiecutter.main import cookiecutter
from cookiecutter import exceptions as cookiecutter_exceptions
import unicodedata
from briefcase.exceptions import (
    InvalidTemplateRepository,
    NetworkFailure,
    TemplateUnsupportedVersion,
    BriefcaseCommandError,
)
import subprocess
from cookiecutter.repository import is_repo_url

def generate_template(template, branch, output_path, extra_context):
    """Ensure the named template is up-to-date for the given branch, and roll out
    that template.

    :param template: The template URL or path to generate
    :param branch: The branch of the template to use
    :param output_path: The filesystem path where the template will be generated.
    :param extra_context: Extra context to pass to the cookiecutter template
    """
    # Make sure we have an updated cookiecutter template,
    # checked out to the right branch
    cached_template = update_cookiecutter_cache(template=template, branch=branch)

    try:
        # Unroll the template
        cookiecutter(
            str(cached_template),
            no_input=True,
            output_dir=str(output_path),
            checkout=branch,
            extra_context=extra_context,
        )
    except subprocess.CalledProcessError as e:
        # Computer is offline
        # status code == 128 - certificate validation error.
        raise NetworkFailure("clone template repository") from e
    except cookiecutter_exceptions.RepositoryNotFound as e:
        # Either the template path is invalid,
        # or it isn't a cookiecutter template (i.e., no cookiecutter.json)
        raise InvalidTemplateRepository(template) from e
    except cookiecutter_exceptions.RepositoryCloneFailed as e:
        # Branch does not exist.
        raise TemplateUnsupportedVersion(branch) from e