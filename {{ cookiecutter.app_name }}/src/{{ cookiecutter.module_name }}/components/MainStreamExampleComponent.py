from __future__ import annotations
from typing import List, TYPE_CHECKING
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from nadoo_ai.styling import StandardStyling

if TYPE_CHECKING:
    from nadoo_ai.app import nadoo_ai

class MainStreamExampleComponent(toga.Box):
    def __init__(
        self,
        app: nadoo_ai,
        id: str | None = None,
        start_values: dict | None = None
    ):
        style = Pack(direction=COLUMN)
        super().__init__(id=id, style=style)
        self.app = app

        self.standardeingabe_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        self.standardeingabe_box.lable1 = toga.Label(
            "Reference",
            style=StandardStyling.standard_label_style(),
        )
        self.standardeingabe_box.add(self.standardeingabe_box.lable1)
        
        if start_values is not None:
            self.setup_input_fields(start_values)

        self.next_button = toga.Button(
            "Next",
            on_press=self.next_step,
            style=StandardStyling.standard_button_style(),
        )
        self.add(self.standardeingabe_box)
        self.add(self.next_button)

    def setup_input_fields(self, start_values):
        self.standardeingabe_box.lable1.text = start_values["lable1"]

    def next_step(self, widget):
        # Implement the logic for the next step
        pass