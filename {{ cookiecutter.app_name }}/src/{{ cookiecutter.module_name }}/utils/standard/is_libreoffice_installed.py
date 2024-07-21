import platform
import subprocess

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