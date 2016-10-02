# coding: utf-8

import os
save_locale = os.environ.get('LC_CTYPE')
os.environ['LC_CTYPE'] = 'ru_RU'

from m_librarian.translations import translations  # noqa

if save_locale:
    os.environ['LC_CTYPE'] = save_locale

_ = getattr(translations, 'ugettext', None) or translations.gettext


def test_translations():
    assert _('xxx') == u'xxx'
    assert _('File') == u'Файл'
