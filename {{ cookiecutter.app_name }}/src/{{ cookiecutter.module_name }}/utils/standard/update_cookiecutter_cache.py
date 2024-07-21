import re
from cookiecutter.main import cookiecutter
import unicodedata
from cookiecutter import exceptions as cookiecutter_exceptions
from briefcase.exceptions import (
    InvalidTemplateRepository,
    NetworkFailure,
    TemplateUnsupportedVersion,
    BriefcaseCommandError,
)
import subprocess
from cookiecutter.repository import is_repo_url

def update_cookiecutter_cache(template: str, branch="master"):
    """Ensure that we have a current checkout of a template path.

    If the path is a local path, use the path as is.

    If the path is a URL, look for a local cache; if one exists, update it,
    including checking out the required branch.

    :param template: The template URL or path.
    :param branch: The template branch to use. Default: ``master``
    :return: The path to the cached template. This may be the originally
        provided path if the template was a file path.
    """
    if is_repo_url(template):
        # The app template is a repository URL.
        #
        # When in `no_input=True` mode, cookiecutter deletes and reclones
        # a template directory, rather than updating the existing repo.
        #
        # Look for a cookiecutter cache of the template; if one exists,
        # try to update it using git. If no cache exists, or if the cache
        # directory isn't a git directory, or git fails for some reason,
        # fall back to using the specified template directly.
        cached_template = cookiecutter_cache_path(template)
        try:
            repo = self.tools.git.Repo(cached_template)
            # Raises ValueError if "origin" isn't a valid remote
            remote = repo.remote(name="main")
            try:
                # Attempt to update the repository
                remote.fetch()
            except self.tools.git.exc.GitCommandError as e:
                # We are offline, or otherwise unable to contact
                # the origin git repo. It's OK to continue; but
                # capture the error in the log and warn the user
                # that the template may be stale.
                pass

            try:
                # Check out the branch for the required version tag.
                head = remote.refs[branch]

                self.logger.info(
                    f"Using existing template (sha {head.commit.hexsha}, "
                    f"updated {head.commit.committed_datetime.strftime('%c')})"
                )
                head.checkout()
            except IndexError as e:
                # No branch exists for the requested version.
                raise TemplateUnsupportedVersion(branch) from e
        except self.tools.git.exc.NoSuchPathError:
            # Template cache path doesn't exist.
            # Just use the template directly, rather than attempting an update.
            cached_template = template
        except self.tools.git.exc.InvalidGitRepositoryError:
            # Template cache path exists, but isn't a git repository
            # Just use the template directly, rather than attempting an update.
            cached_template = template
        except ValueError as e:
            raise BriefcaseCommandError(
                f"Git repository in a weird state, delete {cached_template} and try briefcase create again"
            ) from e
    else:
        # If this isn't a repository URL, treat it as a local directory
        cached_template = template

    return cached_template