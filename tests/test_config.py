
import os
from m_librarian.config import get_config


def test_config():
    config_path = os.path.join(
        os.path.dirname(__file__), 'test_config.conf')
    get_config(config_path)
    ml_conf = get_config()
    assert ml_conf.get('library', 'path') == '/home/test-config'
