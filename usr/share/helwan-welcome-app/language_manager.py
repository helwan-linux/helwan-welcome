import os
import gettext
from PyQt5.QtCore import QLocale, QTranslator, QLibraryInfo, QCoreApplication

def load_translation(language_code):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    locale_path = os.path.join(current_dir, 'locales')
    try:
        translation = gettext.translation('base', localedir=locale_path, languages=[language_code])
        translation.install()
        return translation.gettext
    except FileNotFoundError:
        return lambda s: s

def change_application_language(app: QCoreApplication, language_code: str):
    translator = QTranslator(app)
    path = os.path.join(QLibraryInfo.location(QLibraryInfo.TranslationsPath), "qtbase_")
    if translator.load(path + QLocale(language_code).name()):
        app.installTranslator(translator)
        return True
    else:
        print(f"Warning: Could not load Qt translation for {language_code}")
        return False

def get_system_locale():
    locale = QLocale.system().name()
    return locale
