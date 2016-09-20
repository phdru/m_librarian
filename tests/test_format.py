
import os
from m_librarian import download
from m_librarian.config import get_config


def test_compile_format():
    config_path = os.path.join(
        os.path.dirname(__file__), 'test_config.conf')
    get_config(config_path)
    ml_conf = get_config()
    ml_conf.set('download', 'format', '%a/%s/%n %t')
    download._compile_format()
    assert download.compiled_format == \
        u'%(author)s/%(series)s/%(ser_no)d %(title)s'
