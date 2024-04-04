import os
import json
import subprocess
import platform
from nadoo_telemarketing.CONSTANTS import BASE_DIR
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