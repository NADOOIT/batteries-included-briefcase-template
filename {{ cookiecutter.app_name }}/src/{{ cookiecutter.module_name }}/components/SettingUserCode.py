from {{ cookiecutter.app_name|lower|replace('-', '_') }}.components.SettingsElement import SettingsElement
import toga
from toga.style import Pack
from {{ cookiecutter.app_name|lower|replace('-', '_') }}.services import set_user_code, get_settings

class SettingUserCode(SettingsElement):
    
    def __init__(self):
        super().__init__()
        # Eingabefeld für den User Code erstellen
        self.user_code_input = toga.TextInput(
            placeholder="User Code",
        )

        setting_lable = toga.Label(
            "NADOO Nutzercode", style=Pack(padding_bottom=10)
        )

        self.gui.add(setting_lable)
        self.gui.add(self.user_code_input)
        self.load_settings()
    
    def save(self):
        set_user_code(self.user_code_input.value)

    def load_settings(self):
        settings = get_settings()
        self.user_code_input.value = settings.get("user_code", "")