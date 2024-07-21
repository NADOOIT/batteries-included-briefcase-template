import re
import platform
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
import os
from cookiecutter.repository import is_repo_url

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