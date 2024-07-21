import subprocess
import os
from cookiecutter.repository import is_repo_url
from briefcase.exceptions import (
    InvalidTemplateRepository,
    NetworkFailure,
    TemplateUnsupportedVersion,
    BriefcaseCommandError,
)

def create_and_activate_venv_mac(self):
    python_path = (
        subprocess.check_output(["pyenv", "which", "python"]).decode().strip()
    )
    # Create the virtual environment inside the project folder
    venv_path = os.path.join(get_project_folder_path(), "env")
    subprocess.run([python_path, "-m", "venv", venv_path])
    # Activate the virtual environment - for macOS
    activate_command = f"source {venv_path}/bin/activate"
    subprocess.run(["bash", "-c", activate_command])

    return venv_path