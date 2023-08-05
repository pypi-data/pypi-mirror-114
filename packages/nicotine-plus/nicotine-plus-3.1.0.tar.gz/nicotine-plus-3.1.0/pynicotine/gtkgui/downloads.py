# COPYRIGHT (C) 2020-2021 Nicotine+ Team
# COPYRIGHT (C) 2016-2017 Michael Labouebe <gfarmerfr@free.fr>
# COPYRIGHT (C) 2016-2018 Mutnick <mutnick@techie.com>
# COPYRIGHT (C) 2013 eL_vErDe <gandalf@le-vert.net>
# COPYRIGHT (C) 2008-2012 Quinox <quinox@users.sf.net>
# COPYRIGHT (C) 2009 Hedonist <ak@sensi.org>
# COPYRIGHT (C) 2006-2009 Daelstorm <daelstorm@gmail.com>
# COPYRIGHT (C) 2003-2004 Hyriand <hyriand@thegraveyard.org>
#
# GNU GENERAL PUBLIC LICENSE
#    Version 3, 29 June 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

from gi.repository import Gtk

from pynicotine.config import config
from pynicotine.gtkgui.transferlist import TransferList
from pynicotine.gtkgui.utils import open_file_path
from pynicotine.gtkgui.widgets.dialogs import option_dialog


class Downloads(TransferList):

    def __init__(self, frame, tab_label):

        TransferList.__init__(self, frame, type='download')
        self.tab_label = tab_label

        self.popup_menu_clear.setup(
            ("#" + _("Finished / Aborted / Filtered"), self.on_clear_finished_aborted),
            ("", None),
            ("#" + _("Finished"), self.on_clear_finished),
            ("#" + _("Aborted"), self.on_clear_aborted),
            ("#" + _("Failed"), self.on_clear_failed),
            ("#" + _("Filtered"), self.on_clear_filtered),
            ("#" + _("Queued..."), self.on_try_clear_queued),
            ("", None),
            ("#" + _("Clear All..."), self.on_try_clear_all),
        )

    def on_try_clear_queued(self, *args):

        option_dialog(
            parent=self.frame.MainWindow,
            title=_('Clear Queued Downloads'),
            message=_('Are you sure you wish to clear all queued downloads?'),
            callback=self.on_clear_response,
            callback_data="queued"
        )

    def on_try_clear_all(self, *args):

        option_dialog(
            parent=self.frame.MainWindow,
            title=_('Clear All Downloads'),
            message=_('Are you sure you wish to clear all downloads?'),
            callback=self.on_clear_response,
            callback_data="all"
        )

    def folder_download_response(self, dialog, response_id, msg):

        dialog.destroy()

        if response_id == Gtk.ResponseType.OK:
            self.frame.np.transfers.folder_contents_response(msg)

    def download_large_folder(self, username, folder, numfiles, msg):

        option_dialog(
            parent=self.frame.MainWindow,
            title=_("Download %(num)i files?") % {'num': numfiles},
            message=_("Are you sure you wish to download %(num)i files from %(user)s's folder %(folder)s?") % {
                'num': numfiles, 'user': username, 'folder': folder},
            callback=self.folder_download_response,
            callback_data=msg
        )

    def on_open_directory(self, *args):

        downloaddir = config.sections["transfers"]["downloaddir"]
        incompletedir = config.sections["transfers"]["incompletedir"] or downloaddir

        transfer = next(iter(self.selected_transfers), None)

        if not transfer:
            return

        if transfer.status == "Finished":
            if os.path.exists(transfer.path):
                final_path = transfer.path
            else:
                final_path = downloaddir
        else:
            final_path = incompletedir

        # Finally, try to open the directory we got...
        command = config.sections["ui"]["filemanager"]
        open_file_path(final_path, command)

    def on_play_files(self, *args):

        downloaddir = config.sections["transfers"]["downloaddir"]

        for transfer in self.selected_transfers:

            playfile = None

            if transfer.file is not None and os.path.exists(transfer.file.name):
                playfile = transfer.file.name
            else:
                # If this file doesn't exist anymore, it may have finished downloading and have been renamed
                # try looking in the download directory and match the original filename.
                basename = str.split(transfer.filename, '\\')[-1]

                if transfer.path:
                    # Custom download path specified
                    path = os.sep.join([transfer.path, basename])
                else:
                    path = os.sep.join([downloaddir, basename])

                if os.path.exists(path):
                    playfile = path

            if playfile:
                command = config.sections["players"]["default"]
                open_file_path(playfile, command)

    def on_browse_folder(self, *args):

        requested_users = set()
        requested_folders = set()

        for transfer in self.selected_transfers:
            user = transfer.user
            folder = transfer.filename.rsplit('\\', 1)[0]

            if user not in requested_users and folder not in requested_folders:
                self.frame.np.userbrowse.browse_user(user, folder=folder)

                requested_users.add(user)
                requested_folders.add(folder)

    def on_clear_aborted(self, *args):
        self.clear_transfers(["Aborted", "Cancelled"])

    def on_clear_finished_aborted(self, *args):
        self.clear_transfers(["Aborted", "Cancelled", "Finished", "Filtered"])

    def on_clear_failed(self, *args):
        self.clear_transfers(["Cannot connect", "Local file error", "Remote file error", "File not shared"])

    def on_clear_filtered(self, *args):
        self.clear_transfers(["Filtered"])
