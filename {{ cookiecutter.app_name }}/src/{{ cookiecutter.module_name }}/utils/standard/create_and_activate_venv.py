import platform

def create_and_activate_venv(self):
    os_type = platform.system()
    if os_type == "Darwin":  # macOS
        return self.create_and_activate_venv_mac()
    # Add more conditions for other OS types here
    else:
        print(f"OS {os_type} not supported yet")