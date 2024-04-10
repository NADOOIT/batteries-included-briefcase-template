import os
import json
import subprocess
import platform
from {{ cookiecutter.app_name|lower|replace('-', '_') }}.CONSTANTS import BASE_DIR, SETTINGS_ORDNER

def ensure_folder_exists(folder_name):
    base_dir = get_base_dir_path()
    folder_path = os.path.join(base_dir, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def get_base_dir_path():
    ensure_base_folder_exits()
    return os.path.join(os.path.expanduser("~"), BASE_DIR)

def ensure_base_folder_exits():
    base_dir = os.path.join(os.path.expanduser("~"), BASE_DIR)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        
""" Beispiel für Abrufen von Dateipfad
def get_xyz_data_file_path():
    base_dir = get_base_dir_path()
    return os.path.join(base_dir, XYZ)
"""
"""
def ensure_editible_dropdown_file_exists():
    file_path = get_editable_dropdown_data_file_path()
    if not os.path.isfile(file_path):
        # Initialize the file with default data if it doesn't exist
        default_data = {
            "options": [
                "Option 1",
                "Option 2",
                "Option 3",
                "Option 4",
                "Option 5",
            ]


        }
        with open(file_path, "w") as f:
            json.dump(default_data, f, indent=4)
"""

def translate_date_to_german(date_str):
    # Map of English month names to German month names
    month_translation = {
        "January": "Januar",
        "February": "Februar",
        "March": "März",
        "April": "April",
        "May": "Mai",
        "June": "Juni",
        "July": "Juli",
        "August": "August",
        "September": "September",
        "October": "Oktober",
        "November": "November",
        "December": "Dezember",
    }
    # Split the date string to extract the month
    parts = date_str.split()
    if len(parts) == 3:
        day, month, year = parts
        # Translate the month to German
        german_month = month_translation.get(month, month)
        # Return the date string in German format
        return f"{day} {german_month} {year}"
    return date_str  # Return the original string if format is unexpected

def convert_docx_to_pdf_with_libreoffice(self, docx_path, output_folder):
        # Determine the LibreOffice command based on the operating system
        if platform.system() == "Darwin":  # macOS
            libreoffice_command = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
        elif platform.system() == "Windows":
            libreoffice_command = "C:\\Program Files\\LibreOffice\\program\\soffice.exe"
        else:
            raise OSError("Unsupported operating system for this conversion script")

        # Correctly determining the output directory from the provided path
        if not os.path.isdir(output_folder):  # If the provided path is not a directory
            # Assuming the provided path might be a file path, use its directory as the output folder
            output_folder = os.path.dirname(docx_path)

        # Ensuring the output directory exists
        os.makedirs(output_folder, exist_ok=True)

        # Define the base name for the output files without the extension
        base_output_name = os.path.splitext(os.path.basename(docx_path))[0]

        # Define the PDF export options for different versions
        pdf_versions = {
            "_PDF_A-1": 'pdf:writer_pdf_Export:{"SelectPdfVersion":{"type":"long","value":"1"}}',
            "_PDF_A-2": 'pdf:writer_pdf_Export:{"SelectPdfVersion":{"type":"long","value":"2"}}',
            "_PDF_UA": 'pdf:writer_pdf_Export:{"SelectPdfVersion":{"type":"long","value":"2"},"PDFUACompliance":{"type":"boolean","value":true}}',
            "": "",
        }

        # Ensure the output directory exists
        os.makedirs(output_folder, exist_ok=True)

        # Iterate over the PDF versions and export each one
        for suffix, export_options in pdf_versions.items():
            output_pdf_path = os.path.join(
                output_folder, f"{base_output_name}{suffix}.pdf"
            )
            try:

                print(f"Converting to PDF: '{output_pdf_path}'")
                # TODO on Windows the "normal" PDF does not work
                # Construct the command as a list
                command = [
                    libreoffice_command,
                    "--headless",
                    "--convert-to",
                    export_options,
                    "--outdir",
                    output_folder,
                    docx_path,
                ]

                # Print the command to see what will be executed
                print("Executing command:", " ".join(command))

                # Execute the command using subprocess.run
                subprocess.run(
                    command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                # Check if the default output PDF was created
                default_output_pdf_path = os.path.join(
                    output_folder, f"{base_output_name}.pdf"
                )

                print(f"Checking if {default_output_pdf_path} exists...")

                if os.path.exists(default_output_pdf_path):
                    # Rename the output file to include the suffix
                    os.rename(default_output_pdf_path, output_pdf_path)
                    print(f"Converted to PDF: '{output_pdf_path}'")
                    self.pdf_file_path = output_pdf_path
                else:
                    print(
                        f"Expected PDF '{default_output_pdf_path}' not found after conversion."
                    )
            except subprocess.CalledProcessError as e:
                print(f"Error during conversion: {e}")
                print(e.stdout.decode())
                print(e.stderr.decode())
            except FileNotFoundError:
                print(
                    f"LibreOffice executable not found at '{libreoffice_command}'. Please ensure LibreOffice is installed at the specified path."
                )
            except OSError as e:
                print(f"Error during file renaming: {e}")

def open_folder(self, widget):
    folder_path = self.folder_path  # Assuming this is the path you want to open
    try:
        if platform.system() == "Windows":
            subprocess.run(["explorer", folder_path], check=True)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", folder_path], check=True)
        else:  # Assuming Linux
            subprocess.run(["xdg-open", folder_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error opening folder: {e}")
        
def is_libreoffice_installed():
        if platform.system() == "Darwin":  # macOS
            libreoffice_command = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
        elif platform.system() == "Windows":
            libreoffice_command = "C:\\Program Files\\LibreOffice\\program\\soffice.exe"
        else:
            libreoffice_command = (
                "libreoffice"  # For Linux and other OSes, try the generic command
            )

        try:
            subprocess.run(
                [libreoffice_command, "--version"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
        
#Law
        
        import json
import os
import uuid
from nadoo_law.CONSTANTS import (
    BEWEISMITTEL_OWI_DATA_FILE_NAME,
    BEWEISMITTEL_SCHEIDUNG_DATA_FILE_NAME,
    LAWYER_DATA_FILE_NAME,
    BASE_DIR,
    LOGIN_INFORMATION_FILE_NAME,
    AUSFÜHRUNGEN_DATEI_NAME
)


def get_lawyer_data_file_path():
    base_dir = get_base_dir_path()
    return os.path.join(base_dir, LAWYER_DATA_FILE_NAME)


def get_beweismittel_OWi_data_file_path():
    base_dir = get_base_dir_path()
    return os.path.join(base_dir, BEWEISMITTEL_OWI_DATA_FILE_NAME)

def get_beweismittel_Scheidung_data_file_path():
    base_dir = get_base_dir_path()
    return os.path.join(base_dir, BEWEISMITTEL_SCHEIDUNG_DATA_FILE_NAME)



def ensure_lawyer_data_file_exists():
    file_path = get_lawyer_data_file_path()
    if not os.path.isfile(file_path):
        # Initialize the file with a dummy lawyer if it doesn't exist
        dummy_data = {
            "selected_lawyer_id": str(uuid.uuid4()),
            "lawyer_details": {
                "dummy_id": {
                    "name": "Dummy Lawyer",
                    "email": "dummy@lawfirm.com",
                    "phone": "123-456-7890",
                    "fax": "098-765-4321",
                    "title": "Lawyer",
                    "specialty": "General",
                }
            },
        }
        with open(file_path, "w") as f:
            json.dump(dummy_data, f, indent=4)


def ensure_beweismittel_OWi_data_file_exists():
    file_path = get_beweismittel_OWi_data_file_path()
    if not os.path.isfile(file_path):
        # Initialize the file with default data if it doesn't exist
        default_data = {
            "options": [
                "Messprotokolle",
                "Ausbildungsnachweise der Mess- und Auswertebeamten",
                "Originalbeweisfotos",
                "Eichscheine",
                "Gesamte Messreihe vom Tattag",
                "Digitale Rohmessdaten sowie die dazugehörigen öff. Token und Passwörter",
                "Statistikdatei mit Case List",
                "Konformitätsbescheinigung und –erklärung zum Messgerät",
                "Kalibrier- und Testfotos",
                "Bedienungsanleitung der zum Tattag gültigen Version",
                "Auskunft über Reparaturen, Wartungen, vorgezogene Neueichung oder vgl. die Funktionsfähigkeit des hier verwendeten Messgerätes berührende Ereignisse",
                "Beschilderungsnachweise für 2 km vor und nach der Messstelle",
                "Liste aller am Tattag aufgenommenen Verkehrsverstöße",
            ]


        }
        with open(file_path, "w") as f:
            json.dump(default_data, f, indent=4)

def ensure_beweismittel_Scheidung_data_file_exists():
    file_path = get_beweismittel_Scheidung_data_file_path()
    if not os.path.isfile(file_path):
        # Initialize the file with default data if it doesn't exist
        default_data = {
            "options": [
                "Geburtsurkunde",
                "Scheidungsfolgevereinbarung",
            ]
        }
        with open(file_path, "w") as f:
            json.dump(default_data, f, indent=4)

def ensure_user_auth_data_file_exists():
    file_path = get_user_auth_data_file_path()
    if not os.path.isfile(file_path):
        # Initialize the file with default data if it doesn't exist
        default_data = {
            "user_name": "",
            }
        with open(file_path, "w") as f:
            json.dump(default_data, f, indent=4)

def get_user_auth_data_file_path():
    base_dir = os.path.join(os.path.expanduser("~"), BASE_DIR)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    return os.path.join(base_dir, "user_auth_data.json")

def get_login_information_test():
    login_information = {
        "username": "test",
    }
    return login_information

def get_login_information():
    ensure_login_information_file_exists()
    file_path = get_login_information_file_path()
    with open(file_path, "r") as f:
        return json.load(f)
    
    
def get_login_information_file_path():
    base_dir_path = get_base_dir_path()
    return os.path.join(base_dir_path, LOGIN_INFORMATION_FILE_NAME)

def get_ausfuehrungen_file_path():
    base_dir_path = get_base_dir_path()
    return os.path.join(base_dir_path, AUSFÜHRUNGEN_DATEI_NAME)

    
def ensure_login_information_file_exists():
    file_path = get_login_information_file_path()
    if not os.path.isfile(file_path):
        # Initialize the file with a dummy lawyer if it doesn't exist
        dummy_data = {
            "username": "Bitte DATEV-Nutzername eingeben",
                }
        with open(file_path, "w") as f:
            json.dump(dummy_data, f, indent=4)


def set_login_information(login_information):
    ensure_login_information_file_exists()
    file_path = get_login_information_file_path()
    with open(file_path, "w") as f:
        json.dump(login_information, f, indent=4)

def ensure_data_file_exists():
    file_path = get_ausfuehrungen_file_path()
    if not os.path.isfile(file_path):
        with open(file_path, "w") as file:
            json.dump([], file)

#LaunchPad
            
import os
import platform
import re
import unicodedata
import subprocess
from briefcase.exceptions import (
    InvalidTemplateRepository,
    NetworkFailure,
    TemplateUnsupportedVersion,
    BriefcaseCommandError,
)
from cookiecutter import exceptions as cookiecutter_exceptions
from cookiecutter.main import cookiecutter
from cookiecutter.repository import is_repo_url
from pathlib import Path
import toga
import toml

cookiecutter = staticmethod(cookiecutter)

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


def make_module_name(app_name):
    """Construct a valid module name from an app name.

    :param app_name: The app name
    :returns: The app's module name.
    """
    return app_name.replace("-", "_")


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


def cookiecutter_cache_path(template):
    """Determine the cookiecutter template cache directory given a template URL.

    This will return a valid path, regardless of whether `template`

    :param template: The template to use. This can be a filesystem path or
        a URL.
    :returns: The path that cookiecutter would use for the given template name.
    """
    template = template.rstrip("/")
    tail = template.split("/")[-1]
    cache_name = tail.rsplit(".git")[0]
    return Path.home() / ".cookiecutters" / cache_name

def update_ui(self:toga.App):
    # Refresh the UI to show changes
    self.main_window.content = self.new_project_form

def set_installation_state(app:toga.App):
    config_path = app.paths.config / "install_state.toml"

    # Ensure the directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Check if the file exists
    if not config_path.exists():
        # If not, create it with the initial 'installed' state
        config_data = {"installed": True}
    else:
        # If it exists, load the existing data
        with open(config_path, "r") as config_file:
            config_data = toml.load(config_file)

    # Update the 'installed' state to True
    config_data["installed"] = True

    # Save the updated data
    with open(config_path, "w") as config_file:
        toml.dump(config_data, config_file)

def update_ui_post_install(self:toga.App):
    # Remove the 'Install' button and add the 'New Project' button
    self.main_box.remove(self.install_btn)

def install_python_with_pyenv():
    # Check if the Python version already exists
    pyenv_version_exists = (
        subprocess.run(
            ["pyenv", "versions", "--bare", "--skip-aliases", "3.11.7"],
            capture_output=True,
        ).returncode
        == 0
    )

    # If the version exists, skip installation
    if not pyenv_version_exists:
        # Use 'yes' to automatically answer 'y' to any prompts
        subprocess.run("yes | pyenv install 3.11.7", shell=True)
    else:
        print("Python 3.11.7 is already installed.")

    # Set global version
    subprocess.run(["pyenv", "global", "3.11.7"])

def install_pyenv():
    # Example command, adjust based on OS
    subprocess.run(["curl", "-L", "https://pyenv.run", "|", "bash"])
    # Additional commands may be needed to integrate pyenv into the shell

def setup_project_folder():
    # Get the current user's home directory and set the project folder path
    project_folder = get_project_folder_path()
    return project_folder

def get_project_folder_path():
    home_dir = os.path.expanduser("~")
    project_folder = os.path.join(home_dir, "Documents", "GitHub")

    # Create the folder if it doesn't exist
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)

    return project_folder

def create_and_activate_venv(self):
    os_type = platform.system()
    if os_type == "Darwin":  # macOS
        return self.create_and_activate_venv_mac()
    # Add more conditions for other OS types here
    else:
        print(f"OS {os_type} not supported yet")

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

def on_new_developer_name_entered(self, widget):
    # Generate the email based on the entered name
    new_name = widget.value
    if new_name:
        new_email = f"{new_name.replace(' ', '.').lower()}@nadooit.de"
        self.author_email_input.value = new_email

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
        