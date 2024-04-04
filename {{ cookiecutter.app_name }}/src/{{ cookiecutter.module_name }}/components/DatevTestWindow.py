import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError, HTTPError

import toga
from toga.style import Pack
from toga.style.pack import COLUMN

from nadoo_law.components.Nutzerdateneingabekomponente import Nutzerdateneingabekomponente
from nadoo_law.styling import StandardStyling


class DatevTestWindow(toga.Window):
    def __init__(self, title, width=400, height=400):  # Adjusted height to accommodate new field
        super().__init__(title, size=(width, height))
        self.content = self.build()

    def build(self):
        

        box = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))

        self.nutzerdateneingabekomponente = Nutzerdateneingabekomponente()
        box.add(self.nutzerdateneingabekomponente)

                # Hinzufügen des Switches zur Box
        self.will_apischlüssel_verwenden = toga.Switch(
            "API Schlüssel verwenden",
            style=StandardStyling.standard_switch_style()
        )
        box.add(self.will_apischlüssel_verwenden)  
        self.apischluessel_label = toga.Label("API Schlüssel:", style=StandardStyling.standard_label_style())
        box.add(self.apischluessel_label)    
        self.apischluessel_eingabefeld = toga.TextInput(style=StandardStyling.standard_input_style())
        box.add(self.apischluessel_eingabefeld)



        self.datev_anfrage_eingabefeld = toga.MultilineTextInput(style=Pack(padding_bottom=10, height=100, flex=1))
        box.add(self.datev_anfrage_eingabefeld)
        
        anfrage_akte_senden = toga.Button('Anfrage Akten senden', on_press=self.datenabfrage_akten_datev, style=Pack(padding_top=10))
        box.add(anfrage_akte_senden)
        
        self.datev_anfrage_ausgabe = toga.MultilineTextInput(style=Pack(padding_bottom=10, height=100, flex=1))
        box.add(self.datev_anfrage_ausgabe)

       
        box.add(toga.Label("Aktennummer:", style=Pack(padding_top=10)))

        box.add(toga.Label("Mitarbeiter Info:", style=Pack(padding_top=10)))
        self.datev_mitarbeiter_ausgabe = toga.MultilineTextInput(style=Pack(padding_bottom=10, height=100, flex=1))
        box.add(self.datev_mitarbeiter_ausgabe)
        anfrage_mitarbeiter_senden = toga.Button('Anfrage Mitarbeiter senden', on_press=self.datenabfrage_mitarbeiter_datev, style=Pack(padding_top=10))
        box.add(anfrage_mitarbeiter_senden)


        
        
        # New field for displaying linked data
        self.datev_linked_data_ausgabe = toga.MultilineTextInput(style=Pack(padding_bottom=10, height=100, flex=1))
        box.add(self.datev_linked_data_ausgabe)
        anfrage_teilanfragen_senden = toga.Button('Anfrage für unterkategorien von Akten senden', on_press=self.datenabfrage_datev, style=Pack(padding_top=10))
        box.add(anfrage_teilanfragen_senden)
        
        close_button = toga.Button('Close', on_press=self.close_window, style=Pack(padding_top=10))
        box.add(close_button)

        return box

    def close_window(self, widget):
        self.close()
   
    def datenabfrage_akten_datev(self, widget):
        headers = {
            'Accept': 'application/json; charset=utf-8',
        }
        
        url = 'http://localhost:58454/datev/api/law/v1/files/'
        params = {'top': '10'}
        
        # Überprüfen, ob der API-Schlüssel verwendet werden soll
        if self.will_apischlüssel_verwenden.value:
            apischlüssel = self.apischluessel_eingabefeld.value
            # Fügen Sie den API-Schlüssel dem Header hinzu
            headers['X-DATEV-Client-Id'] = apischlüssel
            auth = None  # Keine Basic Auth notwendig, wenn API-Schlüssel verwendet wird
        else:
            nutzername = self.nutzerdateneingabekomponente.nutzername_eingabefeld.value
            password = self.nutzerdateneingabekomponente.passwort_eingabefeld.value
            auth = HTTPBasicAuth(nutzername, password)
            self.datev_anfrage_eingabefeld.value = f"Trying to connect to DATEV with user {nutzername}"
        
        try:
            # Stellen Sie sicher, dass auth und headers korrekt verwendet werden
            response = requests.get(url, params=params, headers=headers, auth=auth, verify=True)
            response.raise_for_status()
            
            data = response.json()
            self.datev_anfrage_ausgabe.value = str(data)
        except ConnectionError:
            self.datev_anfrage_ausgabe.value = "Connection error: Unable to reach the server. Please check your network connection and the server status."
        except HTTPError as e:
            self.datev_anfrage_ausgabe.value = f"HTTP error: {e.response.status_code} - {e.response.reason}"
        except Exception as e:
            self.datev_anfrage_ausgabe.value = f"An error occurred: {str(e)}"

    def datenabfrage_datev(self, widget):
        headers = {
            'Accept': 'application/json; charset=utf-8',
        }
        
        url = 'http://localhost:58454/datev/api/law/v1/files/'
        params = {'top': '10'}
        
        # Überprüfen, ob der API-Schlüssel verwendet werden soll
        if self.will_apischlüssel_verwenden.value:
            apischlüssel = self.apischluessel_eingabefeld.value
            # Fügen Sie den API-Schlüssel dem Header hinzu
            headers['X-DATEV-Client-Id'] = apischlüssel
            auth = None  # Keine Basic Auth notwendig, wenn API-Schlüssel verwendet wird
            nutzername = "API Key Mode"  # Für die Anzeige, wenn API-Schlüssel verwendet wird
        else:
            nutzername = self.nutzerdateneingabekomponente.nutzername_eingabefeld.value
            password = self.nutzerdateneingabekomponente.passwort_eingabefeld.value
            auth = HTTPBasicAuth(nutzername, password)
        
        self.datev_anfrage_eingabefeld.value = f"Trying to connect to DATEV with user {nutzername}"
        
        try:
            response = requests.get(url, params=params, headers=headers, auth=auth, verify=True)
            response.raise_for_status()
            data = response.json()
            self.datev_anfrage_ausgabe.value = str(data)

            # Fetch and display linked data
            linked_data = []
            for item in data:
                for key, value in item.items():
                    if isinstance(value, dict) and 'link' in value:
                        link_response = requests.get(value['link'], headers=headers, auth=auth, verify=True)
                        if link_response.status_code == 200:
                            linked_data.append(link_response.json())
            self.datev_linked_data_ausgabe.value = str(linked_data)

        except ConnectionError:
            self.datev_anfrage_ausgabe.value = "Connection error: Unable to reach the server."
        except HTTPError as e:
            self.datev_anfrage_ausgabe.value = f"HTTP error: {e.response.status_code} - {e.response.reason}"
        except Exception as e:
            self.datev_anfrage_ausgabe.value = f"An error occurred: {str(e)}"

                    
    def datenabfrage_mitarbeiter_datev(self, widget):
        headers = {
            'Accept': 'application/json; charset=utf-8',
        }
        
        url = 'http://localhost:58454/datev/api/law/v1/employees/'
        
        # Überprüfen, ob der API-Schlüssel verwendet werden soll
        if self.will_apischlüssel_verwenden.value:
            apischlüssel = self.apischluessel_eingabefeld.value
            # Fügen Sie den API-Schlüssel dem Header hinzu
            headers['X-DATEV-Client-Id'] = apischlüssel
            auth = None
            self.datev_anfrage_eingabefeld.value = "Trying to connect to DATEV with API key."
        else:
            nutzername = self.nutzerdateneingabekomponente.nutzername_eingabefeld.value
            password = self.nutzerdateneingabekomponente.passwort_eingabefeld.value
            auth = HTTPBasicAuth(nutzername, password)
            self.datev_anfrage_eingabefeld.value = f"Trying to connect to DATEV with user {nutzername}"
        
        try:
            response = requests.get(url, headers=headers, auth=auth, verify=True)
            response.raise_for_status()
            data = response.json()
            self.datev_mitarbeiter_ausgabe.value = str(data)
        except ConnectionError:
            self.datev_mitarbeiter_ausgabe.value = "Connection error: Unable to reach the server. Please check your network connection and the server status."
        except HTTPError as e:
            self.datev_mitarbeiter_ausgabe.value = f"HTTP error: {e.response.status_code} - {e.response.reason}"
        except Exception as e:
            self.datev_mitarbeiter_ausgabe.value = f"An error occurred: {str(e)}"