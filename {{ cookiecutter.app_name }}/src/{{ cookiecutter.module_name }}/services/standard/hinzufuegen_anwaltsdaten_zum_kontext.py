

def hinzufuegen_anwaltsdaten_zum_kontext(kontext, anwalt_json=None):

    if anwalt_json is None:
        anwalt_json = get_lawyer_data()

    # Hier werden die Anwaltsdetails aus der anwalt_json extrahiert
    anwalt_details = anwalt_json.get('lawyer_details', {})
    kontext['ANWÄLTE'] = [
        {
            'NAME': details.get('name', ''),
            'FACHGEBIETE': details.get('specialty', '').split('; ') if details.get('specialty') else []
        }
        for anwalt_id, details in anwalt_details.items()
    ]
    return kontext