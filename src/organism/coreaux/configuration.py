# coding: utf-8

# Organism - A highly modular and extensible outliner.
# Copyright (C) 2011-2013 Dario Giovannetti <dev@dariogiovannetti.net>
#
# This file is part of Organism.
#
# Organism is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Organism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Organism.  If not, see <http://www.gnu.org/licenses/>.

import os
import errno
from datetime import datetime

import configfile

__author__ = "Dario Giovannetti <dev@dariogiovannetti.net>"

_ROOT_DIR = 'src/organism'
_CORE_INFO = os.path.join(_ROOT_DIR, 'coreaux', 'core.info')
_CONFIG_FILE = os.path.join(_ROOT_DIR, 'organism.conf')
_USER_CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.config',
                                 'organism', 'organism.conf')
_USER_FOLDER_PERMISSIONS = 0750
_DESCRIPTION_LONG = 'Organism is a highly modular outliner whose '\
                    'functionality can be widely extended through the '\
                    'installation of addons.'
_COPYRIGHT_V1 = 'Copyright (C) 2011-{} Dario Giovannetti '\
                '<dev@dariogiovannetti.net>'.format(datetime.now().year)
_COPYRIGHT_V2 = 'Copyright © 2011-{} Dario Giovannetti'.format(datetime.now(
                                                                         ).year)
_DISCLAIMER_SHORT = \
'''This program comes with ABSOLUTELY NO WARRANTY.
This is free software, you are welcome to redistribute it under the
conditions of the GNU General Public License version 3 or later.
See <http://gnu.org/licenses/gpl.html> for details.'''
_DISCLAIMER = \
'''Organism is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Organism is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Organism.  If not, see <http://www.gnu.org/licenses/>.'''

info = configfile.ConfigFile(_CORE_INFO, inherit_options=False)
user_config_file = _USER_CONFIG_FILE
config = None


def load_default_config():
    global config
    config = configfile.ConfigFile(_CONFIG_FILE, inherit_options=False)


def load_user_config(cliargs):
    if cliargs.configfile != None:
        global user_config_file
        user_config_file = os.path.expanduser(cliargs.configfile)
        config.upgrade(user_config_file)
    else:
        try:
            config.upgrade(_USER_CONFIG_FILE)
        except configfile.InvalidFileError:
            pass

    try:
        os.makedirs(os.path.dirname(user_config_file),
                    mode=_USER_FOLDER_PERMISSIONS)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
