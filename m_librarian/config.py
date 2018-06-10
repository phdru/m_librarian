#! /usr/bin/env python

from __future__ import print_function
import os
try:
    from ConfigParser import RawConfigParser, NoSectionError, NoOptionError
except ImportError:  # py3
    from configparser import RawConfigParser, NoSectionError, NoOptionError


__all__ = ['get_config']


def _find_config_dirs_posix():
    config_dirs = []
    if 'XDG_CONFIG_HOME' in os.environ:
        config_dirs.append(os.environ['XDG_CONFIG_HOME'])
    if 'XDG_CONFIG_DIRS' in os.environ:
        config_dirs.extend(os.environ['XDG_CONFIG_DIRS'].split(':'))
    home_config = os.path.expanduser('~/.config')
    if home_config not in config_dirs:
        config_dirs.append(home_config)
    return config_dirs


def find_config_dirs():
    if os.name == 'posix':
        return _find_config_dirs_posix()
    return None


def find_config_file(config_dirs=None):
    if config_dirs is None:
        config_dirs = find_config_dirs()
    for d in config_dirs:
        ml_conf_file = os.path.join(d, 'm_librarian.conf')
        if os.path.exists(ml_conf_file):
            return ml_conf_file
    else:
        return None


_ml_config = None


class ConfigWrapper(object):
    def __init__(self, config):
        self.config = config

    def get(self, section, option, default=None):
        try:
            return self.config.get(section, option)
        except (NoSectionError, NoOptionError):
            return default

    def set(self, section, option, value):
        self.config.set(section, option, value)

    def getint(self, section, option, default=0):
        try:
            return self.config.getint(section, option)
        except (NoSectionError, NoOptionError):
            return default
        # Do not catch ValueError here, it must be propagated

    def getlist(self, section, option, default=None, sep=None):
        value = self.get(section, option)
        if not value:
            if default is None:
                return []
            return default
        return value.split(sep)

    def getpath(self, section, option, default=os.path.curdir):
        path = self.get(section, option, default=default)
        return os.path.expanduser(os.path.expandvars(path))


def get_config(config_path=None):
    global _ml_config
    if _ml_config is None:
        _ml_config = RawConfigParser()
        if config_path is None:
            config_path = find_config_file()
        if config_path is not None:
            _ml_config.read(config_path)
        _ml_config = ConfigWrapper(_ml_config)
    return _ml_config


def test():
    config_dirs = find_config_dirs()
    print("Config dirs:", config_dirs)
    print("Config file:", find_config_file(config_dirs))


if __name__ == '__main__':
    test()
