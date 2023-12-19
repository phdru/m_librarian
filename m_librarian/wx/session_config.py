#! /usr/bin/env python

from __future__ import print_function
import os

from ..config import RawConfigParser, ConfigWrapper, find_config_file


__all__ = ['get_session_config']


def _find_config_dirs_posix():
    config_dirs = []
    if 'XDG_CACHE_HOME' in os.environ:
        config_dirs.append(os.environ['XDG_CACHE_HOME'])
    home_cache = os.path.expanduser('~/.cache')
    if home_cache not in config_dirs:
        config_dirs.append(home_cache)
    return config_dirs


def _find_config_dirs():
    if os.name == 'posix':
        return _find_config_dirs_posix()
    return None


_ml_session_config = None


class SessionConfigWrapper(ConfigWrapper):
    def __init__(self, config, config_path):
        ConfigWrapper.__init__(self, config)
        self.config_path = config_path

    def set(self, section, option, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        super(SessionConfigWrapper, self).set(section, option, value)

    def save(self):
        if self.config_path is None:
            config_dirs = _find_config_dirs()
            self.config_path = \
                os.path.join(config_dirs[0], 'm_librarian_session.conf')
        with open(self.config_path, 'wt') as fp:
            self.config.write(fp)


def get_session_config(config_path=None):
    global _ml_session_config
    if _ml_session_config is None:
        _ml_session_config = RawConfigParser()
        if config_path is None:
            config_dirs = _find_config_dirs()
            config_path = \
                find_config_file(config_dirs, 'm_librarian_session.conf')
        if config_path is not None:
            _ml_session_config.read(config_path)
        _ml_session_config = \
            SessionConfigWrapper(_ml_session_config, config_path)
    return _ml_session_config


def _test():
    config_dirs = _find_config_dirs()
    print("Config dirs:", config_dirs)
    print("Config file:",
          find_config_file(config_dirs, 'm_librarian_session.conf'))


if __name__ == '__main__':
    _test()
