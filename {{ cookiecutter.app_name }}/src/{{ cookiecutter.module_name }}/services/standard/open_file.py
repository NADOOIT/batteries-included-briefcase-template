from datetime import datetime
from requests.auth import HTTPBasicAuth
import platform
import requests
import whisper
import subprocess

def open_file(file_path):
    if file_path:
        try:
            if platform.system() == "Windows":
                subprocess.run(["explorer", file_path], check=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", file_path], check=True)
            else:  # Assuming Linux
                subprocess.run(["xdg-open", file_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error opening file: {e}")
    else:
        print("File path is not set. Unable to open file.")