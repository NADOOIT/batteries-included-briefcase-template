import toga

def update_ui(self:toga.App):
    # Refresh the UI to show changes
    self.main_window.content = self.new_project_form