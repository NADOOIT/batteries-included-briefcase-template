import os

def get_updates_pdf_path(app):
    updates_pdf_dateipfad = os.path.join(app.paths.app, "resources", "update.pdf")
    return updates_pdf_dateipfad