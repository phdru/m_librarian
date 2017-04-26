#! /usr/bin/env python

from __future__ import print_function
import os
try:
    from ConfigParser import RawConfigParser
except ImportError:  # py3
    from configparser import RawConfigParser

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
    raise OSError("Unknow OS")


def find_config_file(config_dirs=None):
    if config_dirs is None:
        config_dirs = find_config_dirs()
    for d in config_dirs:
        ml_conf_file = os.path.join(d, 'm_librarian.conf')
        if os.path.exists(ml_conf_file):
            return ml_conf_file
    else:
        raise IOError("Cannot find m_librarian.conf in %s" % config_dirs)


_ml_config = None


def get_config(config_path=None):
    global _ml_config
    if _ml_config is None:
        if config_path is None:
            config_path = find_config_file()
        _ml_config = RawConfigParser()
        _ml_config.read(config_path)
    return _ml_config


def test():
    config_dirs = find_config_dirs()
    print("Config dirs:", config_dirs)
    print("Config file:", find_config_file(config_dirs))


if __name__ == '__main__':
    test()
