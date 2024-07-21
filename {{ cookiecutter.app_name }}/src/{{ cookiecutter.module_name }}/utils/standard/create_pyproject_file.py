from pathlib import Path
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

def create_pyproject_file(self, user_data, project_folder):
    # Construct the path to the template file
    template_file_name = "base_project_template.toml"
    template_path = Path(self.app.paths.app / "resources" / template_file_name)

    # Ensure the project subfolder exists
    project_subfolder = Path(project_folder, user_data["app_name"])
    project_subfolder.mkdir(parents=True, exist_ok=True)

    # New project file path
    new_project_path = project_subfolder / "pyproject.toml"

    try:
        with open(template_path, "r") as template_file:
            template_content = template_file.read()

        # Replace placeholders with actual data
        for key, value in user_data.items():
            placeholder = "{{" + key.upper() + "}}"
            template_content = template_content.replace(placeholder, value)

        print(template_content)

        # Write the new pyproject.toml file
        with open(new_project_path, "w") as new_project_file:
            new_project_file.write(template_content)

        return new_project_file

    except FileNotFoundError as e:
        self.display_error(f"Template file not found: {e}")
    except IOError as e:
        self.display_error(f"Error while handling the file: {e}")
    except Exception as e:
        self.display_error(f"An unexpected error occurred: {e}")