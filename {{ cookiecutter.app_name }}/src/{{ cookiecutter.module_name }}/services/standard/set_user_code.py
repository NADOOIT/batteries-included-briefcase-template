

def set_user_code(user_code):
    settings = get_settings()
    settings["user_code"] = user_code
    set_settings(settings)