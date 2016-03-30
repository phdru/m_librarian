
import gettext
import locale
import os

language = locale.getdefaultlocale()[0]
translations = None

if language:
    mo_filename = os.path.join(
        os.path.dirname(__file__), 'translations', language + '.mo')
    if os.path.exists(mo_filename):
        mo_file = open(mo_filename, 'rb')
        translations = gettext.GNUTranslations(mo_file)
        mo_file.close()

if translations is None:
    translations = gettext.NullTranslations()
