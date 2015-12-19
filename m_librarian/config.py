#! /usr/bin/env python

__all__ = ['ml_conf']

import os
from ConfigParser import SafeConfigParser

config_dirs = []
if 'XDG_CONFIG_HOME' in os.environ:
    config_dirs.append(os.environ['XDG_CONFIG_HOME'])
if 'XDG_CONFIG_DIRS' in os.environ:
    config_dirs.extend(os.environ['XDG_CONFIG_DIRS'].split(':'))
home_config = os.path.expanduser('~/.config')
if home_config not in config_dirs:
    config_dirs.append(home_config)

for d in config_dirs:
    ml_conf_file = os.path.join(d, 'm_librarian.conf')
    if os.path.exists(ml_conf_file):
        ml_conf = SafeConfigParser()
        ml_conf.read(ml_conf_file)
        break
else:
    ml_conf = ml_conf_file = None

if __name__ == '__main__':
    print "Config dirs:", config_dirs
    print "Config file:", ml_conf_file
