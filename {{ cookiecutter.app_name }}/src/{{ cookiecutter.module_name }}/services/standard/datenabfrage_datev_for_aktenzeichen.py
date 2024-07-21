import requests
from requests.auth import HTTPBasicAuth

def datenabfrage_datev_for_aktenzeichen(aktenzeichen:str, passwort:str):
    url = 'https://localhost:58452/datev/api/law/v1/files/'
    params = {
        'select': 'id, name, number',
        'filter': f"file_number eq '{aktenzeichen}'",  # Verwendung eines f-Strings zur Einsetzung
        'orderby': 'my_property_name desc,other_property_name asc',
        'top': '100',
        'skip': '10'
    }
    headers = {
        'accept': 'application/json; charset=utf-8'
    }
    # Ersetzen Sie 'your_username' und 'your_password' mit Ihren tatsächlichen Anmeldedaten
    username = get_nutzername()
    auth = HTTPBasicAuth(username, passwort)

    response = requests.get(url, params=params, headers=headers, auth=auth, verify=False)

    if response.status_code == 200:
        return response.json()  # Gibt das JSON-Antwortobjekt zurück
    else:
        return f"Error: {response.status_code}"