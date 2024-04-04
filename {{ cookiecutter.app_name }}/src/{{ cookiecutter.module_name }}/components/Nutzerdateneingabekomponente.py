import toga
from toga.style import Pack
from toga.style.pack import COLUMN

from nadoo_law.services import get_nutzername, set_nutzername
from nadoo_law.styling import StandardStyling

class Nutzerdateneingabekomponente(toga.Box):

    def nutzername_eingabefeld_on_change(self, widget):
        set_nutzername(widget.value)

    def __init__(
        self,
        
        id: str | None = None,
    ):

        style = Pack(direction=COLUMN)
        super().__init__(id=id, style=style)


        self.add(toga.Label("Nutzername:", style=StandardStyling.standard_label_style()))
        self.nutzername_eingabefeld = toga.TextInput(
            on_change=self.nutzername_eingabefeld_on_change,
            style=StandardStyling.standard_input_style(),
        )
        self.add(self.nutzername_eingabefeld)
        self.nutzername_eingabefeld.value = get_nutzername()
        self.add(toga.Label("Passwort:", style=StandardStyling.standard_label_style()))
        self.passwort_eingabefeld = toga.PasswordInput(style=StandardStyling.standard_input_style())
        self.add(self.passwort_eingabefeld)