import json

def mark_ausfuehrung_as_fehlerhaft(ausfuehrung_id):
    ensure_data_file_exists()
    with open(get_ausfuehrungen_file_path(), "r+") as file:
        data = json.load(file)
        for ausfuehrung in data:
            if ausfuehrung["id"] == ausfuehrung_id:
                ausfuehrung["fehlerhaft"] = True
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)