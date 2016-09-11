
import os
import unittest
from m_librarian.config import get_config


class TestFormat(unittest.TestCase):
    def test_config(self):
        config_path = os.path.join(
            os.path.dirname(__file__), 'test_config.conf')
        get_config(config_path)
        ml_conf = get_config()
        self.assertEqual(ml_conf.get('library', 'path'), '/home/test-config')
