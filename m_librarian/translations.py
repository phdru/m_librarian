
import gettext
import locale
import os


def get_translations(language):
    mo_filename = os.path.join(
        os.path.dirname(__file__), 'translations', language + '.mo')
    if os.path.exists(mo_filename):
        mo_file = open(mo_filename, 'rb')
        translations = gettext.GNUTranslations(mo_file)
        mo_file.close()
        return translations
    return None


language = locale.getdefaultlocale()[0]
translations = None

if language:
    if language in ('ru_RU', 'Russian_Russia'):
        language = 'ru'
    translations = get_translations(language)

if translations is None:
    translations = gettext.NullTranslations()
