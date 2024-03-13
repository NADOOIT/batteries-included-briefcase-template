import toga
from toga.style.pack import COLUMN
from toga.style import Pack

class Fehlermeldung(toga.Box):
    def __init__(self, app, id: str | None = None, style=None, fehlermeldung=None, retry_function=None):
        style = style or Pack(direction=COLUMN)
        super().__init__(id=id, style=style)

        self.app = app
        self.fehlermeldung = fehlermeldung or ""
        self.retry_function = retry_function

        self.content = self.create_content()
        self.add(self.content)
                            
    def create_content(self):
        # Get the width of the main window
        main_window_width, _ = self.app.main_window.size

        # Calculate the width of the content_box widget to be 20% smaller than the main window
        error_text_width = main_window_width * 0.8

        content_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        
        # Calculate the height of the error_text widget based on the number of newline characters
        # TODO find a way for dynamic height
        #num_lines = self.fehlermeldung.count('\n') + 1
        
        error_text = toga.MultilineTextInput(value=self.fehlermeldung, style=Pack(padding=10, width=error_text_width, height=200), readonly=True)
        content_box.add(error_text)

        contact_label = toga.TextInput(value="Für Support kontaktieren Sie bitte:\nName: Support Team\nEmail: support@nadooit.de Telefon: 02065 - 7098429", style=Pack(padding=10, height=100))
        content_box.add(contact_label)

        # Add a button to send the error code to support
        # send_button = toga.Button("Senden", on_press=self.send_error_email)
        # content_box.add(send_button)

        # Add a retry button
        retry_button = toga.Button("Retry", on_press=self.retry)
        content_box.add(retry_button)

        return content_box

        """
            def send_error_email(self, widget):
                # Set up the email message
                msg = email.message.EmailMessage()
                msg.set_content("Error code: {}\n\nRegards,\nThe Nadoo Law Team".format(12345))
                msg["Subject"] = "Error Report"
                msg["From"] = "nadoo_law@example.com"
                msg["To"] = "support@example.com"

                # Send the email
                try:
                    server = smtplib.SMTP("smtp.example.com", 587)
                    server.starttls()
                    server.login("nadoo_law@example.com", "password")
                    server.send_message(msg)
                    server.quit()

                    # Display a success message
                    toga.Message.info("Die Fehlermeldung wurde erfolgreich gesendet.", title="Gesendet")

                except Exception as e:
                    # Display an error message
                    toga.Message.error("Fehler beim Senden der Fehlermeldung: {}\nBitte kontaktieren Sie das Support-Team manuell.".format(str(e)), title="Fehler")
        """
    def retry(self, widget):
        # Call the retry function
        if self.retry_function:
            self.retry_function()
