import toga
import toml

def set_installation_state(app:toga.App):
    config_path = app.paths.config / "install_state.toml"

    # Ensure the directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Check if the file exists
    if not config_path.exists():
        # If not, create it with the initial 'installed' state
        config_data = {"installed": True}
    else:
        # If it exists, load the existing data
        with open(config_path, "r") as config_file:
            config_data = toml.load(config_file)

    # Update the 'installed' state to True
    config_data["installed"] = True

    # Save the updated data
    with open(config_path, "w") as config_file:
        toml.dump(config_data, config_file)