import toga
from toga.style import Pack
from toga.style.pack import COLUMN

class EinklappbarerContainer(toga.Box):
    def __init__(self, titel, eingeklappt_zu_beginn=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.titel = titel
        self.eingeklappt = eingeklappt_zu_beginn

        self.titel_button = toga.Button(
            f'{self.titel} {"+" if eingeklappt_zu_beginn else "-"}',
            on_press=self.toggle_ein_ausklappen,
            style=Pack(padding=5)
        )

        self.inhalt_container = toga.Box(style=Pack(direction=COLUMN, flex=1))
        if eingeklappt_zu_beginn:
            self.inhalt_container.style.height = 0
        self.add(self.titel_button)
        self.add(self.inhalt_container)

    def toggle_ein_ausklappen(self, widget:toga.Button):
        self.eingeklappt = not self.eingeklappt

        # Ändere die Sichtbarkeit des inhalt_containers
        if self.eingeklappt:
            # Verwende die 'del' Anweisung, um die Höhe zu entfernen, was den Container ausblendet
            self.inhalt_container.style.height = 0  # Setze die Höhe auf 0, um den Container auszublenden
            widget.text = f'{self.titel} +'
        else:
            # Entferne die Höheneinstellung, um den Container wieder einzublenden
            del self.inhalt_container.style.height
            widget.text = f'{self.titel} -'
        
        self.inhalt_container.refresh()


    def add_inhalt(self, widget):
        # Füge Widgets zum inhalt_container hinzu
        self.inhalt_container.add(widget)
