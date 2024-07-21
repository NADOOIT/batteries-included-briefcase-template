

def make_module_name(app_name):
    """Construct a valid module name from an app name.

    :param app_name: The app name
    :returns: The app's module name.
    """
    return app_name.replace("-", "_")