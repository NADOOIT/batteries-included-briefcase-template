from pathlib import Path
import platform
from cookiecutter.main import cookiecutter
import json
from cookiecutter import exceptions as cookiecutter_exceptions
from briefcase.exceptions import (
    InvalidTemplateRepository,
    NetworkFailure,
    TemplateUnsupportedVersion,
    BriefcaseCommandError,
)
import os
from cookiecutter.repository import is_repo_url

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