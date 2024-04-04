
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from nadoo_travel.components.KundenKarte import KundenKarte
from nadoo_travel.styling import StandardStyling

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
        self.scrollcontain = toga.ScrollContainer(
            content=self.inhalt_container,
            style=Pack(direction=COLUMN, flex=1),
            vertical=True,
        )
        self.scrollcontainer_inhalt = toga.Box(style=Pack(direction=COLUMN, flex=1))
        self.scrollcontain.content  = self.scrollcontainer_inhalt
        self.inhalt_container.add(self.scrollcontain)
        if eingeklappt_zu_beginn:
            self.inhalt_container.style.height = 0
            
        self.add(self.titel_button)
        self.add(self.inhalt_container)

    def toggle_ein_ausklappen(self, widget:toga.Button):
        self.eingeklappt = not self.eingeklappt

        # Ändere die Sichtbarkeit des inhalt_containers
        if self.eingeklappt:
            self.inhalt_container.style.height = 0
            self.scrollcontain.style.visibility = toga.style.pack.HIDDEN
            widget.text = f'{self.titel} +'
            for child in self.scrollcontainer_inhalt.children:
                if isinstance(child, KundenKarte):
                    child.style.visibility = toga.style.pack.HIDDEN
        else:
            del self.inhalt_container.style.height
            self.scrollcontain.style.visibility = toga.style.pack.VISIBLE
            widget.text = f'{self.titel} -'
            for child in self.scrollcontainer_inhalt.children:
                if isinstance(child, KundenKarte):
                    child.style.visibility = toga.style.pack.VISIBLE

        self.refresh()



    def add_inhalt(self, widget):
        # Füge das Widget zum inhalt_container hinzu
        self.scrollcontainer_inhalt.add(widget)

        # Weise dem Widget die Sichtbarkeit basierend auf dem aktuellen Zustand des Containers zu
        if self.eingeklappt:
            widget.style.visibility = toga.style.pack.HIDDEN
        else:
            widget.style.visibility = toga.style.pack.VISIBLE

        # Aktualisiere das Interface
        self.refresh()
