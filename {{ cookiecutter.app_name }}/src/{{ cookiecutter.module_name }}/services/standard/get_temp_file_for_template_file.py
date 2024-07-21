from datetime import datetime
from requests.auth import HTTPBasicAuth
import uuid
import requests
import shutil
import whisper
import logging
import subprocess
import os

def get_temp_file_for_template_file(template_file):
    source_path = os.path.join(get_template_folder(), template_file)

    if not os.path.exists(source_path):
        logging.error(f"Template file does not exist: {source_path}")
        raise FileNotFoundError(f"Template file does not exist: {source_path}")

    # Generate a unique temporary file name
    unique_filename = f"{uuid.uuid4()}_{template_file}"
    temp_file_path = os.path.join(get_temp_folder(), unique_filename)

    # Copy the template to a temporary file and return its path
    try:
        shutil.copyfile(source_path, temp_file_path)
        return temp_file_path
    except IOError as e:
        logging.error(f"Failed to create a temporary file from template: {e}")
        raise