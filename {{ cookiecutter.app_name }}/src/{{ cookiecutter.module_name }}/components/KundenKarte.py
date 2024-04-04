import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, RIGHT

class KundenKarte(toga.Box):
    def __init__(self, name, datum, id=None):
        super().__init__(style=Pack(direction=ROW, padding=5))
        
        self.bearbeitet = False  # Neues Feld für den Bearbeitungszustand
        self.datum = datum  # Neues Attribut für das Datum
        
        # Linke Spalte mit den Kundeninformationen
        self.info_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        self.name_label = toga.Label(name, style=Pack(padding=(0, 5)))
        self.datum_label = toga.Label(datum, style=Pack(padding=(0, 5)))  # Label für das Datum
        self.fortschrittsbalken = toga.ProgressBar(style=Pack(padding=(0, 5)))
        self.arbeitsschritt_label = toga.Label("Arbeitsschritt startet...", style=Pack(padding=(0, 5)))
        self.fehler_label = toga.Label("", style=Pack(padding=(0, 5)))
        
        self.info_box.add(self.name_label)
        self.info_box.add(self.datum_label)  # Füge das Datum-Label zur info_box hinzu
        self.info_box.add(self.fortschrittsbalken)
        self.info_box.add(self.arbeitsschritt_label)
        self.info_box.add(self.fehler_label)
        
        # Rechte Spalte mit dem "Bearbeiten" Button
        self.button_box = toga.Box(style=Pack(direction=COLUMN, alignment=RIGHT))
        self.bearbeiten_button = toga.Button(
            "Bearbeiten",
            on_press=self.bearbeiten_button_pressed,
            style=Pack(padding=(0, 5))
        )
        self.button_box.add(self.bearbeiten_button)
        
        # Füge die linke und rechte Spalte zur Kundenkarte hinzu
        self.add(self.info_box)
        self.add(self.button_box)

    def bearbeiten_button_pressed(self, widget):
        # Funktion, die ausgeführt wird, wenn der "Bearbeiten" Button gedrückt wird
        print(f"Bearbeiten Button für Kunde {self.name_label.text} gedrückt")

        asyncio.create_task(self.bearbeiten())

    async def bearbeiten(self):
        # Setze den Fortschrittsbalken auf 0%
        self.fortschrittsbalken.value = 0
        
        await asyncio.sleep(2)  # Correctly pause for 2 seconds

        # Aktualisiere die Beschriftung des Arbeitsschritts
        self.arbeitsschritt_label.text = "Kundendaten werden geladen"
        self.fortschrittsbalken.value = 0.5  # Setze den Fortschrittsbalken auf 50%
        self.refresh()
        await asyncio.sleep(2)  # Correctly pause for 2 seconds

        # Weitere Aktualisierung der Beschriftung und des Fortschrittsbalkens
        self.arbeitsschritt_label.text = "Kundendaten werden verarbeitet"
        self.fortschrittsbalken.value = 0.8  # Beispiel: Fortschrittsbalken auf 80%
        self.refresh()
        await asyncio.sleep(2)  # Correctly pause for 2 seconds

        # Abschließende Aktualisierungen
        self.arbeitsschritt_label.text = "Abgeschlossen"
        self.fortschrittsbalken.value = 1  # Beispiel: Fortschrittsbalken auf 100%
        self.bearbeitet = True
        self.refresh()