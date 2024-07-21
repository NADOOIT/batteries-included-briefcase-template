

def set_nutzername(nutzername):
    login_information = get_login_information()
    login_information["username"] = nutzername
    set_login_information(login_information)