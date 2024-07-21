import subprocess

def install_pyenv():
    # Example command, adjust based on OS
    subprocess.run(["curl", "-L", "https://pyenv.run", "|", "bash"])