import subprocess

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