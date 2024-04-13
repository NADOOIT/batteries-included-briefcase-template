from nadoo_telemarketing.components.SettingsElement import SettingsElement
import toga
from toga.style import Pack
from toga.style.pack import ROW
from nadoo_telemarketing.services import set_uhrzeit_nächsten_werktag_wechsel, get_settings

class SettingUhrzeitWerktagswechsel(SettingsElement):
    
    def __init__(self):
        super().__init__()
        
        # Dropdown-Menü für die Stunde erstellen
        self.stunde_dropdown = toga.Selection(
            items=[f"{stunde:02d}" for stunde in range(24)],
            style=Pack(flex=1)
        )
        
        # Dropdown-Menü für die Minute erstellen
        self.minute_dropdown = toga.Selection(
            items=[f"{minute:02d}" for minute in range(0, 60, 15)],
            style=Pack(flex=1)
        )
        
        # Dropdown-Menüs nebeneinander platzieren
        dropdown_box = toga.Box(
            children=[self.stunde_dropdown, self.minute_dropdown],
            style=Pack(direction=ROW)
        )
        
        setting_lable = toga.Label(
            "Uhrzeit für den nächsten Werktag wechseln", style=Pack(padding_bottom=10)
        )

        self.gui.add(setting_lable)
        self.gui.add(dropdown_box)
        self.load_settings()
    
    def save(self):
        stunde = self.stunde_dropdown.value
        minute = self.minute_dropdown.value
        uhrzeit = f"{stunde}:{minute}:00"
        set_uhrzeit_nächsten_werktag_wechsel(uhrzeit)

    def load_settings(self):
        settings = get_settings()
        uhrzeit = settings.get("uhrzeit_nächsten_werktag_wechsel", "16:00:00")
        stunde, minute, _ = uhrzeit.split(":")
        self.stunde_dropdown.value = stunde
        self.minute_dropdown.value = minute
