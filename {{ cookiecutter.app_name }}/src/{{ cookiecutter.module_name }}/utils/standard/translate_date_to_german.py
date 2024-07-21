

def translate_date_to_german(date_str):
    # Map of English month names to German month names
    month_translation = {
        "January": "Januar",
        "February": "Februar",
        "March": "März",
        "April": "April",
        "May": "Mai",
        "June": "Juni",
        "July": "Juli",
        "August": "August",
        "September": "September",
        "October": "Oktober",
        "November": "November",
        "December": "Dezember",
    }
    # Split the date string to extract the month
    parts = date_str.split()
    if len(parts) == 3:
        day, month, year = parts
        # Translate the month to German
        german_month = month_translation.get(month, month)
        # Return the date string in German format
        return f"{day} {german_month} {year}"
    return date_str