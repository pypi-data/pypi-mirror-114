"""Use the 153957-theme as theme for the gallery"""

from pathlib import Path

from sigal import signals


def get_path():
    return str(Path(__file__).resolve().parent)


def theme(gallery):
    """Set theme settings to this theme"""

    gallery.settings['theme'] = get_path()


def register(settings):
    signals.gallery_initialized.connect(theme)
