from __future__ import annotations
from typing import TYPE_CHECKING
import subprocess
import platform
import os
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from nadoo_law.styling import StandardStyling
from nadoo_law.services import open_file
if TYPE_CHECKING:
    from nadoo_law.app import NadooLaw


class AntragDateiManager(toga.Box):
    def __init__(
        self, app: NadooLaw, base_docx_datei, id: str | None = None
    ):

        style = Pack(direction=COLUMN)
        super().__init__(id=id, style=style)

        self.app = app

        self.base_docx_datei = base_docx_datei
        self.pdf_file_path = None

        # Extract the folder path from the base_docx_datei for all other files
        self.folder_path = os.path.dirname(self.base_docx_datei)

        # Create the files in the following formats:
        """
        PDF einschließlich 2.0, PDF/A-1, PDF/A-2, PDF/UA
        TIFF (auch TIF) Version 6 (TIFF 6 ist die neueste Version, und zwar bereits seit 1992) zusätzlich zur PDF, wenn das PDF die Datei nicht darstellen kann.
        """
        # self.create_files()

        # Create the UI
        self.create_ui()

    def create_files(self):

        self.convert_docx_to_pdf_with_libreoffice(
            self.base_docx_datei, f"{os.path.basename(self.base_docx_datei)[:-5]}.pdf"
        )

        """ 
        # Convert the base_docx_datei to a PDF file
        output_file_path = os.path.join(self.folder_path, f"{os.path.basename(self.base_docx_datei)[:-5]}.pdf")
        pypandoc.convert_file(self.base_docx_datei, 'pdf', outputfile=output_file_path)

        # Convert the base_docx_datei to a PDF/A-1 file
        output_file_path = os.path.join(self.folder_path, f"{os.path.basename(self.base_docx_datei)[:-5]}_PDF_A-1.pdf")
        pypandoc.convert_file(self.base_docx_datei, 'pdf', outputfile=output_file_path, extra_args=['--pdf-engine-opt', '--pdf-a=1'])

        # Convert the base_docx_datei to a PDF/A-2 file
        output_file_path = os.path.join(self.folder_path, f"{os.path.basename(self.base_docx_datei)[:-5]}_PDF_A-2.pdf")
        pypandoc.convert_file(self.base_docx_datei, 'pdf', outputfile=output_file_path, extra_args=['--pdf-engine-opt', '--pdf-a=2'])

        # Convert the base_docx_datei to a PDF/UA file
        output_file_path = os.path.join(self.folder_path, f"{os.path.basename(self.base_docx_datei)[:-5]}_PDF_UA.pdf")
        pypandoc.convert_file(self.base_docx_datei, 'pdf', outputfile=output_file_path, extra_args=['--pdf-engine-opt', '--pdf-option=/PDF/UA'])

        # Convert the base_docx_datei to a TIFF file
        output_file_path = os.path.join(self.folder_path, f"{os.path.basename(self.base_docx_datei)[:-5]}.tiff")
        pypandoc.convert_file(self.base_docx_datei, 'tiff', outputfile=output_file_path)
             """

    def is_libreoffice_installed(self):
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

    def create_ui(self):
        main_box = toga.Box(style=Pack(direction=COLUMN,flex = 1))

        main_box.add(toga.Divider())

        # Button for opening the docx file
        docx_button = toga.Button(
            "Docx öffnen",
            on_press=lambda btn: open_file(self.base_docx_datei),
            style=StandardStyling.standard_button_style(),
        )
        main_box.add(docx_button)

        # Check if LibreOffice is installed and if a PDF was generated
        if self.is_libreoffice_installed():
            # Optionally convert DOCX to PDF if LibreOffice is installed
            self.convert_docx_to_pdf_with_libreoffice(
                self.base_docx_datei, self.folder_path
            )

            # Button for opening the PDF if it was generated
            pdf_button = toga.Button(
                "PDF öffnen",
                on_press=lambda btn: open_file(self.pdf_file_path),
                style=StandardStyling.standard_button_style(),
            )
            main_box.add(pdf_button)

        # Button for opening the folder
        folder_button = toga.Button(
            "Ordner öffnen", on_press=self.open_folder, style=StandardStyling.standard_button_style()
        )
        main_box.add(folder_button)

        self.add(main_box)

    def open_pdf_file(self, widget):
        open_file(self.pdf_file_path)

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
