

def set_api_key(api_key):
    settings = get_settings()
    settings["api_key"] = api_key
    set_settings(settings)