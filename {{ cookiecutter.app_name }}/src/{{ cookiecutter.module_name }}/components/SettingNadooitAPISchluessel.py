from nadoo_telemarketing.components.SettingsElement import SettingsElement
import toga
from toga.style import Pack
from nadoo_telemarketing.services import set_api_key, get_settings

class SettingNadooitAPISchluessel(SettingsElement):
    
    def __init__(self):
        super().__init__()
        # Eingabefeld für den User Code erstellen
        self.api_key_input = toga.TextInput(
            placeholder="NADOO API Schlüssel",
        )

        setting_lable = toga.Label(
            "NADOO API Schlüssel", style=Pack(padding_bottom=10)
        )

        self.gui.add(setting_lable)
        self.gui.add(self.api_key_input)
        self.load_settings()
    
    def save(self):
        set_api_key(self.api_key_input.value)

    def load_settings(self):
        settings = get_settings()
        self.api_key_input.value = settings.get("api_key", "")