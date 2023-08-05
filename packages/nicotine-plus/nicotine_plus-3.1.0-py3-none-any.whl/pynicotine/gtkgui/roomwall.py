# COPYRIGHT (C) 2020-2021 Nicotine+ Team
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

from pynicotine import slskmessages
from pynicotine.config import config
from pynicotine.gtkgui.utils import load_ui_elements
from pynicotine.gtkgui.widgets.dialogs import dialog_hide
from pynicotine.gtkgui.widgets.dialogs import dialog_show
from pynicotine.gtkgui.widgets.dialogs import generic_dialog
from pynicotine.gtkgui.widgets.textview import append_line
from pynicotine.gtkgui.widgets.theme import update_widget_visuals


class RoomWall:

    def __init__(self, frame, room):

        self.frame = frame
        self.room = room

        load_ui_elements(self, os.path.join(self.frame.gui_dir, "ui", "dialogs", "roomwall.ui"))

        self.dialog = generic_dialog(
            parent=frame.MainWindow,
            content_box=self.Main,
            quit_callback=self.hide,
            title=_("Room Wall"),
            width=800,
            height=600
        )

    def update_message_list(self):
        tickers = self.room.tickers.get_tickers()
        append_line(
            self.RoomWallList, "%s" % ("\n".join(["[%s] %s" % (user, msg) for (user, msg) in tickers])),
            showstamp=False, scroll=False)

    def clear_room_wall_message(self, update_list=True):

        entry_text = self.RoomWallEntry.get_text()
        self.RoomWallEntry.set_text("")

        login = config.sections["server"]["login"]
        self.room.tickers.remove_ticker(login)

        self.RoomWallList.get_buffer().set_text("")

        if update_list:
            self.frame.np.queue.append(slskmessages.RoomTickerSet(self.room.room, ""))
            self.update_message_list()

        return entry_text

    def on_set_room_wall_message(self, *args):

        entry_text = self.clear_room_wall_message(update_list=False)
        self.frame.np.queue.append(slskmessages.RoomTickerSet(self.room.room, entry_text))

        if entry_text:
            login = config.sections["server"]["login"]
            append_line(self.RoomWallList, "[%s] %s" % (login, entry_text), showstamp=False, scroll=False)

        self.update_message_list()

    def on_icon_pressed(self, entry, icon_pos, *args):

        if icon_pos == Gtk.EntryIconPosition.PRIMARY:
            self.on_set_room_wall_message()
            return

        self.clear_room_wall_message()

    def update_visuals(self):

        for widget in list(self.__dict__.values()):
            update_widget_visuals(widget)

    def hide(self, *args):

        self.RoomWallList.get_buffer().set_text("")
        dialog_hide(self.dialog)
        return True

    def show(self):

        self.update_message_list()

        login = config.sections["server"]["login"]

        for user, msg in self.room.tickers.get_tickers():
            if user == login:
                self.RoomWallEntry.set_text(msg)
                self.RoomWallEntry.select_region(0, -1)

        dialog_show(self.dialog)
