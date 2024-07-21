from datetime import datetime

def ermittel_den_aktuellen_monat_als_deutsches_wort(monat_offset=0):
    """
    Ermittelt den Monat relativ zum aktuellen Monat als Zahl und gibt den entsprechenden deutschen Monatsnamen zurück.

    Args:
        monat_offset (int, optional): Die Anzahl der Monate, die zum aktuellen Monat addiert werden sollen. Standard ist 0.

    Returns:
        str: Der ermittelte Monat auf Deutsch (z.B. "Januar", "Februar", ...).
    """
    # Erstelle ein Dictionary, das die Monatszahlen auf die deutschen Monatsnamen abbildet
    monatsnamen = {
        1: "Januar",
        2: "Februar",
        3: "März",
        4: "April",
        5: "Mai",
        6: "Juni",
        7: "Juli",
        8: "August",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Dezember"
    }

    # Ermittle den aktuellen Monat als Zahl
    aktueller_monat_als_zahl = datetime.now().month

    # Addiere den Offset zum aktuellen Monat
    ziel_monat = (aktueller_monat_als_zahl + monat_offset) % 12
    if ziel_monat == 0:
        ziel_monat = 12

    # Gib den entsprechenden deutschen Monatsnamen zurück
    return monatsnamen[ziel_monat]