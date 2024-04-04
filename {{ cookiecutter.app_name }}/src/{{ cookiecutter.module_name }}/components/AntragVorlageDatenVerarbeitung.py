from docxtpl import DocxTemplate
from nadoo_law.services import (
    get_temp_file_for_template_file,
)

class AntragVorlageDatenVerarbeitung:
    def __init__(self, name_der_template_datei):
        self.name_der_template_datei = name_der_template_datei
        self.pfad_zur_temp_datei_des_ausgefüllten_antrags = None

    def erzeuge_antragsdatei_mit_platzhalterinformationen(self, daten_aus_formular: str):
        """
            Erstellt eine Einspruchs-OWi-Antragsdatei mit den angegebenen Platzhalterinformationen.
            
            Verarbeitet die Antragsdaten, um ein Kontext-Dictionary zu generieren.
            Fügt Anwaltsdaten und ausgewählte Beweismittel (Beweismittel) zum Kontext hinzu.
            Rendert die Vorlagendatei mit dem Kontext und speichert das Ergebnis.
            
            Gibt ein Tupel zurück, das Erfolg/Misserfolg und den Ausgabepfad angibt.
        """

        try:
            self.pfad_zur_temp_datei_des_ausgefüllten_antrags = get_temp_file_for_template_file(
                self.name_der_template_datei
            )
            temp_file_for_template_file = DocxTemplate(self.pfad_zur_temp_datei_des_ausgefüllten_antrags)

            temp_file_for_template_file.render(daten_aus_formular)
            temp_file_for_template_file.save(self.pfad_zur_temp_datei_des_ausgefüllten_antrags)
        except Exception as e:
            error_msg = f"Beim Erstellen der Antragsdatei ist ein Fehler aufgetreten: {e}. Bitte wenden Sie sich an die IT von Christoph Backaus."
            print(error_msg)
            return False, error_msg

        # Wenn keine Ausnahme aufgetreten ist, war der Verarbeitungsvorgang erfolgreich
        return True, self.pfad_zur_temp_datei_des_ausgefüllten_antrags


