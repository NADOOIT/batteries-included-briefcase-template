from datetime import datetime
import json
import uuid

def add_ausfuehrung(reference, kundenprogramm_ID, antrags_name):
    ensure_data_file_exists()
    new_ausfuehrung = {
        "id": str(uuid.uuid4()),
        "reference": reference,
        "kundenprogramm_ID": kundenprogramm_ID,
        "datum": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "antrags_name": antrags_name,
        "fehlerhaft": False
    }
    with open(get_ausfuehrungen_file_path(), "r+") as file:
        data = json.load(file)
        data.append(new_ausfuehrung)
        file.seek(0)
        json.dump(data, file, indent=4)