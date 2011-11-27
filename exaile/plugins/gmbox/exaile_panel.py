#!/usr/bin/env python
# -*- coding: utf-8 -*-

# gmbox - Google music box
# Copyright (C) 2010 gmbox team
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

from mainwin import GMBoxPanel
from xl import xdg, trax

class ExailePanel(GMBoxPanel):
       
    def __init__(self, exaile):
        GMBoxPanel.__init__(self)
        self.name = "GMBox"
        self.exaile = exaile
        self.parent = exaile.gui.main.window
        self._child = None

    def get_panel(self):
        if not self._child:
            self.main_window.remove(self.main_vbox)
            self._child = self.main_vbox
        return (self._child, self.name)

    def __del__(self):
        import xlgui
        try:
            xlgui.controller().remove_panel(self._child)
        except ValueError:
            pass
        
    def add_to_playlist(self, tracks):
        playlist_handle = self.exaile.gui.main.get_selected_playlist().playlist
        exaile_tracks = []
        for track in tracks:
            if track.url is not None:
                exaile_track = trax.Track(track.url)
                exaile_track.set_tag_raw('title', track.title)
                exaile_track.set_tag_raw('artist', track.artist)
                exaile_track.set_tag_raw('album', track.album)
                exaile_tracks.append(exaile_track)  
            else:
                print track.name, track.url           
        playlist_handle.add_tracks(exaile_tracks)
        fail_num = len(tracks) - len(exaile_tracks)
        if fail_num == 0:
            status_text = "添加完成，共 %d 个音轨。" % len(exaile_tracks)
        elif fail_num == len(tracks):
            status_text = "获取音轨地址失败，可能是网络问题。"
        else:
            status_text = "有 %d 个音轨地址获取失败，可能请求过于频繁，谷歌使用了验证码，请稍后再试。" % fail_num            
        self.status_label.set_text(status_text)  
