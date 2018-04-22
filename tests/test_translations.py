# coding: utf-8

from m_librarian.translations import get_translations

translations = get_translations('ru')
_ = getattr(translations, 'ugettext', None) or translations.gettext


def test_translations():
    assert _('xxx') == u'xxx'
    assert _('File') == u'Файл'
