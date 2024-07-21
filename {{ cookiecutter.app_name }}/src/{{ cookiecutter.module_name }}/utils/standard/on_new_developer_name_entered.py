

def on_new_developer_name_entered(self, widget):
    # Generate the email based on the entered name
    new_name = widget.value
    if new_name:
        new_email = f"{new_name.replace(' ', '.').lower()}@nadooit.de"
        self.author_email_input.value = new_email