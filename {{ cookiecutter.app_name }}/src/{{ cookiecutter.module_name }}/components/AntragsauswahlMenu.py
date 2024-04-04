from __future__ import annotations
from typing import List, TYPE_CHECKING
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from nadoo_law.components.AntragEinspruchOWiDateneingabe import AntragEinspruchOWiDateneingabe
from nadoo_law.components.AntragScheidungsverfahrenDateneingabe import (
    AntragScheidungsverfahrenDateneingabe,
)
from nadoo_law.styling import StandardStyling

if TYPE_CHECKING:
    from nadoo_law.app import NadooLaw


class AntragsauswahlMenu(toga.Box):

    def __init__(
        self,
        app: NadooLaw,
        id: str | None = None,
        selected_lawyer_details=None,
    ):
        style = Pack(direction=COLUMN)
        super().__init__(id=id, style=style)
        self.app = app

        self.aktiver_antrag = None

        # Dropdown-Menüs
        self.application_type_dropdown = toga.Selection(style=StandardStyling.standard_selection_style())

        self.kategorie_liste: List[str] = []

        self.antraege = [
            AntragEinspruchOWiDateneingabe(
                app,
                lawyer_details=selected_lawyer_details,
            ),
            AntragScheidungsverfahrenDateneingabe(
                app,
                lawyer_details=selected_lawyer_details,
            ),
            # Add other forms as needed
        ]

        self.kategorie_liste = [formular.kategorie for formular in self.antraege]

        if self.antraege:  # Check if there is at least one form
            self.update_application_types(self.antraege[0].kategorie)

        """ 
            "Verkehrsrecht",
            "Familienrecht",
            "Zivilrecht",
            "Strafrecht",
            "Öffentliches Recht",
        """

        self.legal_area_dropdown = toga.Selection(
            on_select=self.on_legal_area_select,
            style=StandardStyling.standard_selection_style(),
            items=self.kategorie_liste,
        )

        # Suchleiste und Button
        """
         search_input = toga.TextInput(
            placeholder="Nach Mandatsnummer suchen", style=Pack(flex=1)
        )
        search_button = toga.Button("Suchen", on_press=self.search_documents)

        search_container = toga.Box(
            children=[search_input, search_button], style=Pack(direction=ROW)
        )
        """

        # Update the dropdown to call a method in the app when selection changes
        self.application_type_dropdown.on_change = self.on_application_type_select

        # Hinzufügen der Widgets zum Hauptlayout
        self.add(self.legal_area_dropdown)
        self.add(self.application_type_dropdown)
        
        self.add(toga.Divider())
        
        # Da sofort die Standardauswahl getroffen ist wird auch dieser Antrag angezeigt
        if self.antraege:  # Check if there is at least one form
            self.aktiver_antrag = next(
                (
                    form
                    for form in self.antraege
                    if form.formular_name == self.application_type_dropdown.value
                ),
                None,
            )

            self.add(self.aktiver_antrag)

        # self.add(search_container)
        """ 
        # Dokumentenliste (Platzhalter für echte Daten)
        document_list = toga.ScrollContainer(style=Pack(flex=1))

        self.add(document_list)
        """

    def on_application_type_select(self, widget):
        # Entferne alle möglichen Anträge aus dem Hauptlayout und füge das ausgewählte Formular hinzu

        if self.aktiver_antrag:
            self.remove(self.aktiver_antrag)

        self.aktiver_antrag = next(
            (form for form in self.antraege if form.formular_name == widget.value), None
        )

        self.add(self.aktiver_antrag)

    def generate_application_types(self):
        application_types = {}
        for formular in self.antraege:
            kategorie = formular.kategorie
            formular_name = formular.formular_name
            if kategorie not in application_types:
                application_types[kategorie] = []
            application_types[kategorie].append(formular_name)
        return application_types

    def update_application_types(self, legal_area):
        application_types = self.generate_application_types()
        self.application_type_dropdown.items = application_types[legal_area]

    def on_legal_area_select(self, widget):
        selected_legal_area = widget.value
        self.update_application_types(selected_legal_area)

    def search_documents(self, widget):
        # Implementierung der Suchlogik
        pass
