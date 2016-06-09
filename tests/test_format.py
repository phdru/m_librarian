#! /usr/bin/env python


import unittest
from tests import main
from m_librarian import config, download


class TestFormat(unittest.TestCase):
    def test_compile_format(self):
        config.get_config().set('download', 'format', '%a/%s/%n %t')
        download._compile_format()
        self.assertEqual(download.compiled_format,
                         u'%(author)s/%(series)s/%(ser_no)d %(title)s')


if __name__ == "__main__":
    main()
