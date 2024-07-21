import toga

def update_ui_post_install(self:toga.App):
    # Remove the 'Install' button and add the 'New Project' button
    self.main_box.remove(self.install_btn)