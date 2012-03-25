# Organism - A simple and extensible outliner.
# Copyright (C) 2011 Dario Giovannetti <dev@dariogiovannetti.net>
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

import time
import os.path
import wx

import organism.coreaux_api as coreaux_api
from organism.coreaux_api import Event
import organism.core_api as core_api

import editor
import msgboxes
import tree

open_database_event = Event()
save_database_as_event = Event()
close_database_event = Event()


def create_database(deffname=None):
    dlg = msgboxes.create_db_ask()
    if not deffname:
        deffname = '.'.join(('new_database',
                             coreaux_api.get_standard_extension()))
    dlg.SetFilename(deffname)
    if dlg.ShowModal() == wx.ID_OK:
        filename = dlg.GetPath()
        if filename:
            try:
                core_api.create_database(filename)
            except core_api.DatabaseAlreadyOpenError:
                msgboxes.create_db_open(filename).ShowModal()
                return False
            except core_api.AccessDeniedError:
                msgboxes.create_db_access(filename).ShowModal()
                return False
            else:
                return filename
        else:
            return False
    else:
        return False


def open_database(filename=None, startup=False):
    if not filename:
        dlg = msgboxes.open_db_ask()
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
        else:
            return False
    if filename:
        try:
            core_api.open_database(filename)
        except core_api.DatabaseAlreadyOpenError:
            msgboxes.open_db_open(filename).ShowModal()
            return False
        except core_api.DatabaseNotAccessibleError:
            msgboxes.open_db_access(filename).ShowModal()
            return False
        except core_api.DatabaseNotValidError:
            msgboxes.open_db_incompatible(filename).ShowModal()
            return False
        else:
            tree.Database.open(filename)
            open_database_event.signal(filename=filename, startup=startup)
            return True
    else:
        return False


def save_database_as(origin):
    for tab in tuple(editor.tabs.copy()):
        if editor.tabs[tab].get_filename() == origin and \
                              not editor.tabs[tab].close_if_needed(warn=False):
            break
    else:
        currname = os.path.basename(origin).rpartition('.')
        deffname = ''.join((currname[0], '_copy', currname[1], currname[2]))
        destination = create_database(deffname)
        if destination:
            core_api.save_database_copy(origin, destination)
            close_database(origin, ask=False)
            open_database(destination)
    
            save_database_as_event.signal()


def save_database_backup(origin):
    currname = os.path.basename(origin).rpartition('.')
    deffname = time.strftime('{}_%Y%m%d%H%M%S{}{}'.format(currname[0],
                                                          currname[1],
                                                          currname[2]))
    destination = create_database(deffname)
    if destination:
        core_api.save_database_copy(origin, destination)


def close_database(filename, ask=True, exit_=False):
    # Do not use nb_left.select_tab() to get the tree, use tree.dbs
    nbl = wx.GetApp().nb_left
    nbr = wx.GetApp().nb_right
    
    for item in tuple(editor.tabs.keys()):
        if editor.tabs[item].get_filename() == filename:
            tab = editor.tabs[item].panel
            tabid = nbr.GetPageIndex(tab)
            nbr.SetSelection(tabid)
            if editor.tabs[item].close(ask=ask) == False:
                return False
    
    if ask and core_api.check_pending_changes(filename):
        save = msgboxes.close_db_ask(filename).ShowModal()
        if save == wx.ID_YES:
            core_api.save_database(filename)
        elif save == wx.ID_CANCEL:
            return False
    
    index = nbl.GetPageIndex(tree.dbs[filename])
    tree.dbs[filename].close()
    nbl.close_page(index)
    
    core_api.close_database(filename)
    
    close_database_event.signal(filename=filename, exit_=exit_)