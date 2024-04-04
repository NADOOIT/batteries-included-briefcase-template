import uuid
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from toga.widgets.button import OnPressHandler
from toga import Window
from nadoo_law.services import get_lawyer_data, set_lawyer_data
from nadoo_law.styling import StandardStyling
class LawyerSelectionComponent(toga.Box):
    def __init__(
        self,
        app,
        id: str | None = None,
    ):
        style = Pack(direction=COLUMN)
        super().__init__(id=id, style=style)
        self.app = app

        # Setup and load data
        self.setup_data()
        
        self.name_input = toga.TextInput(
            placeholder="Name",
            style=StandardStyling.standard_input_style(),
            value=self.lawyer_details[self.selected_lawyer_id].get("name", ""),
        )
        self.email_input = toga.TextInput(
            placeholder="Email",
            style=StandardStyling.standard_input_style(),
            value=self.lawyer_details[self.selected_lawyer_id].get("email", ""),
        )
        self.phone_input = toga.TextInput(
            placeholder="Phone",
            style=StandardStyling.standard_input_style(),
            value=self.lawyer_details[self.selected_lawyer_id].get("phone", ""),
        )
        self.fax_input = toga.TextInput(
            placeholder="Fax",
            style=StandardStyling.standard_input_style(),
            value=self.lawyer_details[self.selected_lawyer_id].get("fax", ""),
        )
        self.title_input = toga.TextInput(
            placeholder="Title",
            style=StandardStyling.standard_input_style(),
            value=self.lawyer_details[self.selected_lawyer_id].get("title", ""),
        )
        self.specialty_input = toga.TextInput(
            placeholder="Specialty",
            style=StandardStyling.standard_input_style(),
            value=self.lawyer_details[self.selected_lawyer_id].get("specialty", ""),
        )

        current_names = self.get_lawyer_names()

        self.lawyer_select = toga.Selection(
            items=current_names,
            value=self.lawyer_details[self.selected_lawyer_id]["name"],
            on_change=self.on_lawyer_select,
            style=StandardStyling.standard_selection_style(),
        )

        self.new_button = toga.Button(
            "Neu", on_press=NewLawyerHandler(self), style=StandardStyling.standard_button_style()
        )
        self.delete_button = toga.Button(
            "Löschen",
            on_press=DeleteLawyerHandler(self),
            style=StandardStyling.standard_button_style(),
        )
        self.save_lawyer_button = toga.Button(
            "Speichern",
            on_press=SaveLawyerHandler(self),
            style=StandardStyling.standard_button_style(),
        )

        self.add(self.lawyer_select)
        self.add(self.name_input)
        self.add(self.email_input)
        self.add(self.phone_input)
        self.add(self.fax_input)
        self.add(self.title_input)
        self.add(self.specialty_input)
        self.add(self.new_button)
        self.add(self.save_lawyer_button)
        self.add(self.delete_button)

    def get_dummy_lawyer(self):
        dummy_id = str(uuid.uuid4())
        return {
            dummy_id: {
                "name": "Dummy Lawyer",
                "email": "dummy@lawfirm.com",
                "phone": "123-456-7890",
                "fax": "098-765-4321",
                "title": "Lawyer",
                "specialty": "General",
            }
        }

    def setup_data(self):
        # Use the service function to get lawyer details
        lawyer_data = get_lawyer_data()
        self.lawyer_details = lawyer_data.get("lawyer_details", {})
        self.selected_lawyer_id = lawyer_data.get("selected_lawyer_id")

        # If there's no valid selected lawyer ID, or it's not in the details, use the first lawyer ID
        if (
            not self.selected_lawyer_id
            or self.selected_lawyer_id not in self.lawyer_details
        ):
            print(
                "No valid selected lawyer ID found. Creating a new one with a dummy lawyer."
            )
            dummy_lawyer = self.get_dummy_lawyer()
            self.lawyer_details.update(dummy_lawyer)
            self.selected_lawyer_id = next(iter(dummy_lawyer))

        # Save the lawyer details with the newly added dummy lawyer
        try:
            data = {
                "selected_lawyer_id": self.selected_lawyer_id,
                "lawyer_details": self.lawyer_details,
            }
            set_lawyer_data(data)
        except Exception as e:
            print(f"Error saving lawyer details: {e}")

        print(f"The last lawyer id that was selected {self.selected_lawyer_id} ")

    def update_dropdown_items(self):
        # Get the current names, including placeholders
        current_names = self.get_lawyer_names()

        lawyer_selected_before_list_update = self.selected_lawyer_id

        # Update the dropdown items
        self.lawyer_select.items = current_names

        self.lawyer_select.value = self.get_lawyer_details_for_id(
            lawyer_selected_before_list_update
        )["name"]

    def reset_input_fields(self):
        self.name_input.value = ""
        self.email_input.value = ""
        self.phone_input.value = ""
        self.fax_input.value = ""
        self.title_input.value = ""
        self.specialty_input.value = ""

    def clean_empty_lawyer_details(self):
        self.lawyer_details = {
            id: details
            for id, details in self.lawyer_details.items()
            if any(details.values())
        }

    def get_lawyer_names(self):
        return [details["name"] for details in self.lawyer_details.values()]

    def on_lawyer_select(self, widget, **kwargs):
        try:
            print("Lawyer was selected")

            selected_name = widget.value
            print(f"Selected lawyer: {selected_name}")

            if selected_name == self.get_lawyer_details_for_id(
                self.selected_lawyer_id
            ).get("name"):
                print(
                    "Selection was the same as the selected lawyer. Skipping loading the lawyer details"
                )
                return

            if selected_name:
                print(self.lawyer_details.items())

                for lawyer_id, details in self.lawyer_details.items():
                    print(lawyer_id)
                    print(details)

                    if details["name"] == selected_name:
                        self.selected_lawyer_id = lawyer_id

                        # Set the currently selected lawyer id in the lawyer_details
                        try:
                            data = {
                                "selected_lawyer_id": self.selected_lawyer_id,
                                "lawyer_details": self.lawyer_details,
                            }
                            set_lawyer_data(data)
                        except Exception as e:
                            print(f"Error saving lawyer details: {e}")

                        self.set_input_fields_for_id(lawyer_id)
                        break
        except Exception as e:
            print(f"Error during lawyer selection: {e}")

    def set_input_fields_for_id(self, lawyer_id):
        try:
            details = self.get_lawyer_details_for_id(lawyer_id)
            self.name_input.value = details.get("name", "")
            self.email_input.value = details.get("email", "")
            self.phone_input.value = details.get("phone", "")
            self.fax_input.value = details.get("fax", "")
            self.title_input.value = details.get("title", "")
            self.specialty_input.value = details.get("specialty", "")
        except Exception as e:
            print(f"Error during lawyer selection: {e}")

    def get_lawyer_details_for_id(self, lawyer_id):
        return self.lawyer_details.get(lawyer_id, {})

    def get_selected_lawyer_details(self):
        if self.selected_lawyer_id and self.selected_lawyer_id in self.lawyer_details:
            return self.lawyer_details[self.selected_lawyer_id]
        return None


class DeleteLawyerHandler(OnPressHandler):
    def __init__(self, component: LawyerSelectionComponent):
        self.component = component

    def __call__(self, widget, **kwargs):
        # Show confirmation dialog with the result handler
        self.component.app.main_window.confirm_dialog(
            title="Bestätigung",
            message="Wollen Sie wirklich den Eintrag löschen?",
            on_result=self.on_confirm_dialog_result,
        )

    def on_confirm_dialog_result(self, window: Window, result: bool):
        # Proceed based on confirmation result
        if result:
            self.delete_lawyer()

    def delete_lawyer(self):
        # Retrieve the current lawyer details
        lawyer_data = get_lawyer_data()
        lawyer_details = lawyer_data.get("lawyer_details", {})
        selected_lawyer_id = lawyer_data.get("selected_lawyer_id")

        if selected_lawyer_id and selected_lawyer_id in lawyer_details:
            # Remove the selected lawyer from the lawyer_details dictionary
            del lawyer_details[selected_lawyer_id]

            # Determine the next selected lawyer or create a dummy if none are left
            if not lawyer_details:
                dummy_lawyer = self.component.get_dummy_lawyer()
                lawyer_details.update(dummy_lawyer)
                selected_lawyer_id = next(iter(dummy_lawyer))
            else:
                # Select the first lawyer from the remaining ones
                selected_lawyer_id = next(iter(lawyer_details))

            # Save the updated lawyer details
            set_lawyer_data(
                {
                    "selected_lawyer_id": selected_lawyer_id,
                    "lawyer_details": lawyer_details,
                }
            )

            # Update the component state
            self.component.lawyer_details = lawyer_details
            self.component.selected_lawyer_id = selected_lawyer_id

            # Update the UI components
            self.component.update_dropdown_items()
            self.component.set_input_fields_for_id(selected_lawyer_id)

            print("Lawyer successfully deleted.")
        else:
            print("No valid lawyer selected for deletion.")


class NewLawyerHandler(OnPressHandler):
    def __init__(self, component: LawyerSelectionComponent):
        self.component = component

    def __call__(self, widget, **kwargs):
        print("New Lawyer Handler Called")
        new_id = str(uuid.uuid4())

        # Construct the new lawyer details
        new_lawyer_details = {
            new_id: {
                "name": "New Lawyer "
                + new_id[:8],  # Shorten the UUID for display purposes
                "email": "new.lawyer@lawfirm.com",
                "phone": "+49 (221) 99999 9999",
                "fax": "+49 (221) 99999 9998",
                "title": "Rechtsanwalt",
                "specialty": "Fachanwalt für Spezialgebiet",
            }
        }

        # Retrieve the current lawyer details and update them with the new lawyer
        lawyer_data = get_lawyer_data()
        lawyer_data["lawyer_details"].update(new_lawyer_details)
        lawyer_data["selected_lawyer_id"] = new_id  # Update the selected lawyer ID

        # Save the updated lawyer details
        set_lawyer_data(lawyer_data)

        # Update the component state with the new details
        self.component.lawyer_details = lawyer_data["lawyer_details"]
        self.component.selected_lawyer_id = new_id

        # Refresh the UI components
        self.component.update_dropdown_items()
        self.component.set_input_fields_for_id(new_id)
        self.component.lawyer_select.value = new_lawyer_details[new_id]["name"]

        print(f"New lawyer created with name: {new_lawyer_details[new_id]['name']}")


class SaveLawyerHandler(OnPressHandler):
    def __init__(self, component: LawyerSelectionComponent):
        self.component = component

    def __call__(self, widget, **kwargs):
        print("Save Lawyer Handler Called")
        # Gather the updated details from the input fields
        updated_details = {
            "name": self.component.name_input.value.strip(),
            "email": self.component.email_input.value.strip(),
            "phone": self.component.phone_input.value.strip(),
            "fax": self.component.fax_input.value.strip(),
            "title": self.component.title_input.value.strip(),
            "specialty": self.component.specialty_input.value.strip(),
        }

        # Check for uniqueness of the new name
        if any(
            lawyer["name"] == updated_details["name"]
            and lawyer_id != self.component.selected_lawyer_id
            for lawyer_id, lawyer in self.component.lawyer_details.items()
        ):
            print(f"A lawyer with the name '{updated_details['name']}' already exists.")
            self.component.app.main_window.info_dialog(
                "Doppelter Name",
                f"Ein Anwalt mit dem Namen '{updated_details['name']}' existiert bereits. Bitte wählen Sie einen anderen Namen.",
            )
            return

        # Update the details of the selected lawyer directly in the component
        self.component.lawyer_details[self.component.selected_lawyer_id] = (
            updated_details
        )

        # Prepare data to save
        lawyer_data = {
            "selected_lawyer_id": self.component.selected_lawyer_id,
            "lawyer_details": self.component.lawyer_details,
        }

        # Save the updated lawyer details
        set_lawyer_data(lawyer_data)

        # Refresh the UI components
        self.component.update_dropdown_items()
        print(f"Lawyer details for '{updated_details['name']}' have been updated.")
