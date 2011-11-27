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

from lib.core import gmbox
from lib.const import listing_map
from treestuff import *
import gtk
import gobject
import os
import sys
import threading
import urllib
import subprocess
import traceback

class GMBoxPanel():
       
    def __init__(self):
        
        if hasattr(sys, "frozen"):
            self.module_path = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
        else:
            self.module_path = os.path.dirname(unicode(os.path.abspath(__file__), sys.getfilesystemencoding()))
        
        builder = gtk.Builder()
        builder.add_from_file(self.module_path + "/gmbox.glade")
        builder.connect_signals(self)
        for widget in builder.get_objects():
            if issubclass(type(widget), gtk.Buildable):
                name = gtk.Buildable.get_name(widget)
                setattr(self, name, widget)

        # setting dict
        self.cfg = {"working": self.module_path + "/gmbox.cfg",
                          "home": os.path.expanduser("~/.gmbox.cfg")}
        save_folder = os.path.join(os.path.expanduser("~"), "gmbox_download")
        self.settings = {"save_folder": save_folder,
                                 "player_path": "vlc",
                                 "download_lyric": True,
                                 "download_conver": True}
        self.result_pages = [{}, {}, {}, {}, {}]
     
        self.init_main_notebook()
        self.init_setting()
        self.setup_listing_page()

    def init_main_notebook(self):
        
        # window logo
        if __name__ == "__main__":
            icon_path = self.module_path + "/pixbufs/gmbox.png"
            logo_icon = gtk.gdk.pixbuf_new_from_file(icon_path)
            self.main_window.set_icon(logo_icon)
        
        # playlist page, remove in exaile plugin mode
        if __name__ != "__main__":
            self.main_notebook.remove_page(1)
        else:
            self.playlist_page = PlaylistPage(self)
            for children in self.playlist_vbox.get_children():
                self.playlist_vbox.remove(children)                
            self.playlist_vbox.add(self.playlist_page)        
        
        # download page
        self.download_page = DownloadPage(self)
        for children in self.download_vbox.get_children():
            self.download_vbox.remove(children)                
        self.download_vbox.add(self.download_page)
    
    def init_setting(self):
        
        def read_setting_from_file(settings, url):
            try:
                config_file = open(url)
                config_text = config_file.read()
                for line in config_text.split("\n"):
                    settting = line.split("=")
                    if len(settting) == 2:
                        if settting[1] in ["True", "False"]:
                            settings[settting[0]] = settting[1] == "True"
                        else:
                            settings[settting[0]] = settting[1]
            except:
                pass
            return settings        

        if os.path.exists(self.cfg["working"]):
            self.settings = read_setting_from_file(self.settings,
                                                   self.cfg["working"])
        if os.path.exists(self.cfg["home"]):
            self.settings = read_setting_from_file(self.settings,
                                                   self.cfg["home"])

        self.save_folder_entry.set_text(self.settings["save_folder"])
        self.player_path_entry.set_text(self.settings["player_path"])
        self.download_lyric_checkbutton.set_active(self.settings["download_lyric"])
        self.download_cover_checkbutton.set_active(self.settings["download_conver"])
        
        # disable in exaile plugin mode
        if __name__ != "__main__":
            # run in exaile
            self.player_path_label.set_sensitive(False)
            self.player_path_entry.set_text("exaile")
            self.player_path_entry.set_sensitive(False)
            self.player_path_button.set_sensitive(False)

    def setup_listing_page(self):
        page = ListingPage(self)
        page_label = gtk.Label("<b>排行榜</b>")
        page_label.set_use_markup(True)
        self.browser_notebook.remove_page(0)                
        self.browser_notebook.append_page(page, page_label)
    
    def on_browser_notebook_tab_button_press_event(self, widget, event, data=None):
        if event.type == gtk.gdk._2BUTTON_PRESS or event.button == 2:
            index = self.browser_notebook.page_num(widget.page)
            self.browser_notebook.remove_page(index)

    def on_search_entry_activate(self, widget, data=None):
        if self.track_radiobutton.get_active():
            type = 1
        else:
            type = 2    
        text = self.search_entry.get_text()
        
        if text == "":
            self.status_label.set_text("查找字符串不能为空。")
            return
        
        self.create_search_tab(type, text)
    
    def on_search_entry_icon_press(self, widget, position, event, data=None):
        if position == gtk.ENTRY_ICON_SECONDARY:
            widget.set_text("")
        self.search_entry.emit("activate")      
        
    def create_search_tab(self, type, text):
        if text in self.result_pages[type].keys():
            page = self.result_pages[type][text]
            index = self.browser_notebook.page_num(page)
            if index == -1:
                page_label = PageLabel(page)
                page_label.connect("button-press-event",
                                self.on_browser_notebook_tab_button_press_event)
                index = self.browser_notebook.append_page(page, page_label)                
        else:        
            self.status_label.set_text("正在查找，请等待……")              
            page = ResultPage(type, text, self)
            self.result_pages[type][text] = page
            page_label = PageLabel(page)
            page_label.connect("button-press-event",
                                self.on_browser_notebook_tab_button_press_event)
            index = self.browser_notebook.append_page(page, page_label)
            
        self.browser_notebook.set_current_page(index)
        
    def get_tracks_url(self, tracks, action):        
        if action == "playlist":
            self.status_label.set_text("正在获取音轨地址，请等待……")       
            track_url_geter = TrackUrlGeter(tracks, self.add_to_playlist)
            track_url_geter.start()
        elif action == "downlist":
            self.add_to_downlist(tracks)
                   
    def add_to_playlist(self, tracks): 
        for track in tracks:
            self.playlist_page.add_track(track)
        self.status_label.set_text("已添加 %d 个文件到播放列表" % len(tracks))     
    
    def call_player(self, url):
        player = self.player_path_entry.get_text()
        player_runner = PlayerRunnerer(url, player)
        player_runner.start()
        self.status_label.set_text("就绪")
             
    def add_to_downlist(self, tracks):
        for track in tracks:
            track.folder = self.save_folder_entry.get_text()
            self.download_page.add_track(track)
        self.status_label.set_text("已添加 %d 个文件到下载列表" % len(tracks))      
    
    def get_redirected_url(self, url):
        import httplib
        from urlparse import urlparse
        
        try:
            url_parsed = urlparse(url)
            conn = httplib.HTTPConnection(url_parsed.netloc)
            non_netloc = "%s?%s" % (url_parsed.path, url_parsed.query)
            conn.request("HEAD", non_netloc)
            res = conn.getresponse()
            redirect_url = res.getheader("location")
            return redirect_url
        except:
            return None
    
    def on_save_folder_button_clicked(self, widget, data=None):
        dialog = gtk.FileChooserDialog("选择一个文件", None,
                               gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                               (gtk.STOCK_OPEN, gtk.RESPONSE_OK,
                                gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.save_folder_entry.set_text(dialog.get_filename())
        dialog.destroy()
        
    def on_player_path_button_clicked(self, widget, data=None):
        dialog = gtk.FileChooserDialog("选择播放器执行文件", None,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_OPEN, gtk.RESPONSE_OK,
                                gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.player_path_entry.set_text(dialog.get_filename())
        dialog.destroy()
        
    def on_save_settings_button_clicked(self, widget, data=None):
        
        def save_setting_to_file(settings, url):
            config_file = open(url, "w")   
            for key in self.settings.keys():            
                config_file.write("%s=%s\n" % (key, self.settings[key]))
                config_file.flush()
                config_file.close
        
        self.settings["save_folder"] = self.save_folder_entry.get_text()
        self.settings["download_lyric"] = self.download_lyric_checkbutton.get_active()
        self.settings["download_conver"] = self.download_cover_checkbutton.get_active()
        
        if __name__ == "__main__":
            self.settings["player_path"] = self.player_path_entry.get_text()
         
        errors = []
        try:
            save_setting_to_file(self.settings, self.cfg["working"])
        except Exception, error:
            errors.append(str(error))
            try:
                save_setting_to_file(self.settings, self.cfg["home"])
            except Exception, error:
                errors.append(str(error))
                errors_text = "\n".join(errors)
                dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
                                           gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                           "写入配置文件出错！\n%s" % errors_text)
                dialog.run()
                dialog.destroy()
                    
    def on_main_window_destroy(self, widget, data=None):
        gtk.main_quit()
    
class PageLabel(gtk.EventBox):
    
    def __init__(self, page):
        gtk.EventBox.__init__(self)
        self.page = page
        self.add(gtk.Label(page.text))
        self.show_all()
        
class PlaylistPage(gtk.ScrolledWindow):
    
    def __init__(self, gmbox_panel):
        gtk.ScrolledWindow.__init__(self)
        
        self.gmbox_panel = gmbox_panel
        
        self.treeview = PlaylistTreeview()
        self.liststore = self.treeview.liststore
        self.setup_treeview()

        self.menu = gtk.Menu()
        self.play_menuitem = gtk.MenuItem("播放")
        self.remove_menuitem = gtk.MenuItem("移除")
        self.clear_menuitem = gtk.MenuItem("清空")
        self.setup_menu()          
        self.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.add(self.treeview)
        
        self.downloading_filenames = []
        
        self.menu.show_all()        
        self.show_all()
        
    def add_track(self, track):
        if not track.in_playlist:
            self.liststore.append((track,))
            track.in_playlist = True
    
    def setup_menu(self):
        self.menu.append(self.play_menuitem)
        self.menu.append(self.remove_menuitem)
        self.menu.append(self.clear_menuitem)
        self.menu.connect("selection-done", self.on_menu_selection_done)
        self.play_menuitem.connect("activate", self.on_play_menuitem_activate)
        self.remove_menuitem.connect("activate", self.on_remove_menuitem_activate)
        self.clear_menuitem.connect("activate", self.on_clear_menuitem_activate)

    def on_play_menuitem_activate(self, widget, data=None):
        tracks = self.analyze_available_tracks()
        if len(tracks) > 0:
            self.gmbox_panel.call_player(tracks[0].url)
        self.treeview.get_selection().unselect_all()
        
    def on_remove_menuitem_activate(self, widget, data=None):
        model, rows = self.treeview.get_selection().get_selected_rows()
        if len(rows) > 0:            
            for path in rows:
                source_path = model.convert_path_to_child_path(path)
                iter = self.liststore.get_iter(source_path)
                self.liststore.remove(iter)     
                           
    def on_clear_menuitem_activate(self, widget, data=None):
        self.liststore.clear()
        
    def setup_treeview(self):     
        self.treeview.connect("button-press-event", self.on_treeview_button_press_event)
            
    def on_treeview_button_press_event(self, widget, event, data=None):
        if event.type == gtk.gdk._2BUTTON_PRESS:
            tracks = self.analyze_available_tracks()
            if len(tracks) > 0:
                self.gmbox_panel.call_player(tracks[0].url)
        elif event.button == 3:
            self.menu.popup(None, None, None, event.button, event.time)
            return True
        
    def analyze_available_tracks(self):
        model, rows = self.treeview.get_selection().get_selected_rows()
        tracks = []
        if len(rows) > 0:            
            for path in rows:
                iter = model.get_iter(path)
                track = model.get_value(iter, 0)
                tracks.append(track)
        return tracks          

    def on_menu_selection_done(self, widget, data=None):
        self.treeview.queue_draw()       
         
class DownloadPage(gtk.ScrolledWindow):
    
    def __init__(self, gmbox_panel):
        gtk.ScrolledWindow.__init__(self)
        
        self.gmbox_panel = gmbox_panel
        
        self.treeview = DownloadTreeview()
        self.liststore = self.treeview.liststore
        self.setup_treeview()

        self.menu = gtk.Menu()
        self.playlist_menuitem = gtk.MenuItem("播放")
        self.retry_menuitem = gtk.MenuItem("重试")
        self.clean_menuitem = gtk.MenuItem("清除已完成")
        self.setup_menu()          
        self.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.add(self.treeview)
        
        self.downloading_filenames = []
        self.waiting_tracks = []
        self.thread_num = 0
        
        self.menu.show_all()        
        self.show_all()
    
    def add_track(self, track):
        if not track.in_downlist:
            self.liststore.append((track,))
            track.in_downlist = True
            if track.from_album:
                self.start_downloader(track)
            elif track.filename not in self.downloading_filenames:
                self.start_downloader(track)
                self.downloading_filenames.append(track.filename)
            else:
                track.status = Track.STATUS_DUPLICATE
                track.process = "100%"
        
    def retry_track(self, tracks):
        for track in tracks:
            self.start_downloader(track)
        
    def start_downloader(self, track):
        if self.thread_num < 3:
            # setup download setting
            track.download_lyric = self.gmbox_panel.download_lyric_checkbutton.get_active()
            track.download_cover = self.gmbox_panel.download_cover_checkbutton.get_active()
            
            # start download thread 
            self.running = threading.Event()
            self.running.set()
            downloader = Downloader(track, self.running, self);
            downloader.start()
            #TODO not safe #1
            self.thread_num += 1
        else:
            track.status = Track.STATUS_WAITING
            self.waiting_tracks.append(track)
    
    def downloader_notify(self):
        #TODO not safe #2
        self.thread_num -= 1
        if len(self.waiting_tracks) != 0:
            self.start_downloader(self.waiting_tracks.pop(0))
    
    def setup_menu(self):
        self.menu.append(self.playlist_menuitem)
        self.menu.append(self.retry_menuitem)
        self.menu.append(self.clean_menuitem)
        self.menu.connect("selection-done", self.on_menu_selection_done)
        self.playlist_menuitem.connect("activate", self.on_playlist_menuitem_activate)
        self.retry_menuitem.connect("activate", self.on_retry_menuitem_activate)
        self.clean_menuitem.connect("activate", self.on_clean_menuitem_activate)

    def on_playlist_menuitem_activate(self, widget, data=None):
        tracks = self.analyze_available_tracks(Track.STATUS_DOWNLOADED, Track.STATUS_EXIST)
        if len(tracks) > 0:
            self.gmbox_panel.add_to_playlist(tracks)
        self.treeview.get_selection().unselect_all()

    def on_retry_menuitem_activate(self, widget, data=None):
        tracks = self.analyze_available_tracks(Track.STATUS_NOT_DOWNLOAD,
                                                Track.STATUS_DOWNLOAD_FAIL,
                                                Track.STATUS_GET_URL_FAIL)
        if len(tracks) > 0:
            self.retry_track(tracks)
        self.treeview.get_selection().unselect_all() 
        
    def on_clean_menuitem_activate(self, widget, data=None):
        need_clean = (Track.STATUS_DOWNLOADED, Track.STATUS_DUPLICATE, Track.STATUS_EXIST)
        for row in self.liststore:
            track = row[0]
            if track.status in need_clean:
                self.liststore.remove(row.iter)
                track.in_downlist = False
                
    def setup_treeview(self):        
        self.treeview.connect("button-press-event", self.on_treeview_button_press_event)

    def on_treeview_button_press_event(self, widget, event, data=None):
        if event.type == gtk.gdk._2BUTTON_PRESS:
            tracks = self.analyze_available_tracks(Track.STATUS_DOWNLOADED, Track.STATUS_EXIST)
            if len(tracks) > 0:
                self.gmbox_panel.add_to_playlist(tracks)
        elif event.button == 3:
            self.menu.popup(None, None, None, event.button, event.time)
            return True
        
    def analyze_available_tracks(self, *status):
        model, rows = self.treeview.get_selection().get_selected_rows()
        tracks = []
        if len(rows) > 0:            
            for path in rows:
                iter = model.get_iter(path)
                track = model.get_value(iter, 0)
                if track.status in status:
                    tracks.append(track)
        return tracks          

    def on_menu_selection_done(self, widget, data=None):
        self.treeview.queue_draw()
        
class ListingPage(gtk.ScrolledWindow):
    
    def __init__(self, gmbox_panel):
        gtk.ScrolledWindow.__init__(self)
        
        self.gmbox_panel = gmbox_panel
        
        self.treeview = ListingTreeview()
        self.treestore = gtk.TreeStore(gobject.TYPE_PYOBJECT) 
        self.setup_treeview()

        self.menu = gtk.Menu()
        self.get_listing_menuitem = gtk.MenuItem("获取")
        self.setup_menu()          
        self.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.add(self.treeview)
        
        self.menu.show_all()        
        self.show_all()
    
    def setup_menu(self):
        self.menu.append(self.get_listing_menuitem)
        self.menu.connect("selection-done", self.on_menu_selection_done)
        self.get_listing_menuitem.connect("activate", self.on_get_listing_menuitem_activate)
    
    def on_get_listing_menuitem_activate(self, widget, data=None):
        model, rows = self.treeview.get_selection().get_selected_rows()
        if len(rows) > 0:
            for path in rows:
                iter = model.get_iter(path)
                search = model.get_value(iter, 0)
                self.gmbox_panel.create_search_tab(search.type, search.text)
        self.treeview.get_selection().unselect_all()
        
    def setup_treeview(self):        
        for listing_parent in listing_map:
            parent_search = Search(None, listing_parent[0], 0)
            index = self.treestore.append(None, (parent_search,))
            for listing in listing_parent[1]:
                search = search = Search(listing[1], listing[0], listing[2])       
                self.treestore.append(index, (search,))         
            
        self.treeview.set_model(self.treestore)
        self.treeview.connect("button-press-event", self.on_treeview_button_press_event)
           
    def on_treeview_button_press_event(self, widget, event, data=None):
        if event.type == gtk.gdk._2BUTTON_PRESS:
            model, rows = self.treeview.get_selection().get_selected_rows()
            if len(rows) > 0:
                for path in rows:
                    iter = model.get_iter(path)
                    search = model.get_value(iter, 0)      
                    if search.type != 0:     
                        self.gmbox_panel.create_search_tab(search.type, search.text)
        elif event.button == 3:
            self.menu.popup(None, None, None, event.button, event.time)
            return True          

    def on_menu_selection_done(self, widget, data=None):
        self.treeview.queue_draw()

class ResultPage(gtk.ScrolledWindow):
    
    def __init__(self, type, text, gmbox_panel):
        gtk.ScrolledWindow.__init__(self)
        
        self.type = type
        self.text = text
        self.gmbox_panel = gmbox_panel        
        self.albumholder = Holder("album", "正在获取专辑信息")
        
        self.treeview = ResultTreeview()
        self.treestore = gtk.TreeStore(gobject.TYPE_PYOBJECT)         
        self.setup_treeview()                

        self.menu = gtk.Menu()
        self.playlist_menuitem = gtk.MenuItem("试听")
        self.downlist_menuitem = gtk.MenuItem("下载")
        self.setup_menu()   
        self.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.add(self.treeview)
        
        self.start_search_thread() 
        self.menu.show_all()
        self.show_all()
        
    def setup_menu(self):
        self.menu.append(self.playlist_menuitem)
        self.menu.append(self.downlist_menuitem)
        self.menu.connect("selection-done", self.on_menu_selection_done)
        self.playlist_menuitem.connect("activate", self.on_playlist_menuitem_activate)
        self.downlist_menuitem.connect("activate", self.on_downlist_menuitem_activate)

    def start_search_thread(self):
        if self.type == 1 or self.type == 3:
            track_searcher = TrackSearcher(self.type, self.text, 1, self.track_result_callback)
            track_searcher.start()
        elif self.type == 2 or self.type == 4:
            album_searcher = AlbumSearcher(self.type, self.text, 1, self.album_result_callback)
            album_searcher.start()
            
    def setup_treeview(self):        
        self.treeview.set_model(self.treestore)
        self.treeview.connect("row-expanded", self.on_treeview_row_expanded)
        self.treeview.connect("button-press-event", self.on_treeview_button_press_event)
       
    def on_treeview_row_expanded(self, widget, iter, path, data=None):
        model = self.treeview.get_model()
        album = model.get_value(iter, 0)
        album.path = path
        if not album.expanded:
            album_track_geter = AlbumTrackGeter(album, self.albumtrack_result_callback)
            album_track_geter.start()                  
            
    def on_treeview_button_press_event(self, widget, event, data=None):
        if event.type == gtk.gdk._2BUTTON_PRESS:
            tracks = self.analyze_available_tracks()
            if len(tracks) > 0:
                self.gmbox_panel.get_tracks_url(tracks, "playlist")                       
        elif event.button == 3:
            self.menu.popup(None, None, None, event.button, event.time)
            return True  
        
    def analyze_available_tracks(self):
        model, rows = self.treeview.get_selection().get_selected_rows()
        tracks = []
        if len(rows) > 0:            
            for path in rows:
                iter = model.get_iter(path)
                treeitem = model.get_value(iter, 0)
                if isinstance(treeitem, Track):
                    # is a track
                    tracks.append(treeitem)
                elif isinstance(treeitem, Album) and treeitem.expanded:
                    # is a album parent node, get all tracks children
                    first_child_iter = model.iter_children(iter)
                    tracks.append(model.get_value(first_child_iter, 0))
                    next_child_iter = model.iter_next(first_child_iter)                    
                    while next_child_iter is not None:
                        tracks.append(model.get_value(next_child_iter, 0))  
                        next_child_iter = model.iter_next(next_child_iter)
                elif isinstance(treeitem, Holder) and not treeitem.loaded:
                    treeitem.loaded = True
                    self.gmbox_panel.status_label.set_text("正在载入下一页，请等待……")
                    if treeitem.type == 1 or treeitem.type == 3:                        
                        track_searcher = TrackSearcher(treeitem.type, treeitem.text, treeitem.page,
                                                       self.track_result_callback)
                        track_searcher.start()
                    else:
                        album_searcher = AlbumSearcher(treeitem.type, treeitem.text, treeitem.page,
                                                       self.album_result_callback)
                        album_searcher.start()
        return tracks
            
    def albumtrack_result_callback(self, songlist, album):
        parent_iter = self.treestore.get_iter(album.path)
        refresh_iter = self.treestore.iter_children(parent_iter)
        self.treestore.remove(refresh_iter)
        for song in songlist:
            track = Track(song["id"], song["title"], song["artist"], song["album"])
            track.from_album = True
            track.cover = album.cover
            self.treestore.append(parent_iter, (track,))
        album = self.treestore.get_value(parent_iter, 0)
        album.expanded = True
        self.treeview.expand_to_path(album.path)     

    def on_menu_selection_done(self, widget, data=None):
        self.treeview.queue_draw()
    
    def on_playlist_menuitem_activate(self, widget, data=None):
        tracks = self.analyze_available_tracks()
        if len(tracks) > 0:
            self.gmbox_panel.get_tracks_url(tracks, "playlist")
        self.treeview.get_selection().unselect_all()
    
    def on_downlist_menuitem_activate(self, widget, data=None):
        tracks = self.analyze_available_tracks()
        if len(tracks) > 0:
            self.gmbox_panel.get_tracks_url(tracks, "downlist")
        self.treeview.get_selection().unselect_all()       
                            
    def track_result_callback(self, songlist, type, text, next_page):
        if len(songlist) == 0:
            self.gmbox_panel.status_label.set_text("查找结束，没有找到任何结果。")
            return
        
        for song in songlist:
            # song["album"][1:-1] to remove the <> sign
            track = Track(song["id"], song["title"], song["artist"], song["album"][1:-1])
            self.treestore.append(None, (track,))
        self.gmbox_panel.status_label.set_text("查找结束，共找到 %d 个结果。" % len(songlist))
        
        if next_page != 0:
            more_holder = Holder("more", "第 %d 页" % next_page)
            more_holder.type = type
            more_holder.text = text
            more_holder.page = next_page
            self.treestore.append(None, (more_holder,))
    
    def album_result_callback(self, albumlist, type, text, next_page):
        if len(albumlist) == 0:
            self.gmbox_panel.status_label.set_text("查找结束，没有找到任何结果。")
            return
        
        for album in albumlist:
            album = Album(album["id"], album["name"], album["memo"])
            album.text = text
            parent_iter = self.treestore.append(None, (album,))
            # force to display expand "+" icon 
            self.treestore.append(parent_iter, (self.albumholder,))
        self.gmbox_panel.status_label.set_text("查找结束，共找到 %d 个结果。" % len(albumlist))   
                        
        if next_page != 0:
            more_holder = Holder("more", "第 %d 页" % next_page)
            more_holder.type = type
            more_holder.text = text
            more_holder.page = next_page
            self.treestore.append(None, (more_holder,))

class TrackSearcher(threading.Thread):
    
    def __init__(self, type, text, page, callback):
        threading.Thread.__init__(self)
        self.type = type
        self.text = text
        self.page = page
        self.callback = callback
        
    def run(self):
        has_more = False
        if self.type == 1:
            has_more = gmbox.search(self.text, self.page)
        else:
            has_more = gmbox.get_list(self.text, self.page)
        if has_more:
            next_page = self.page + 1
        else:
            next_page = 0
        self.callback(gmbox.songlist, self.type, self.text, next_page)

class TrackUrlGeter(threading.Thread):
    
    def __init__(self, tracks, callback):
        threading.Thread.__init__(self)
        self.tracks = tracks
        self.callback = callback
        
    def run(self):
        for track in self.tracks:
            track.url = gmbox.get_stream_url(track.id)
            self.callback([track])
        
class AlbumSearcher(threading.Thread):
    
    def __init__(self, type, text, page, callback):
        threading.Thread.__init__(self)
        self.type = type
        self.text = text
        self.page = page
        self.callback = callback
        
    def run(self):
        has_more = False
        if self.type == 2:
            has_more = gmbox.searchalbum(self.text, self.page)
        else:
            has_more = gmbox.get_album_IDs(self.text, self.page)
        if has_more:
            next_page = self.page + 1
        else:
            next_page = 0
        self.callback(gmbox.albumlist, self.type, self.text, next_page)
        
class AlbumTrackGeter(threading.Thread):
    
    def __init__(self, album, callback):
        threading.Thread.__init__(self)
        self.album = album
        self.callback = callback
        
    def run(self):
        gmbox.get_albumlist(self.album.id)
        # some extra info
        self.album.company = gmbox.albuminfo["company"]   
        self.album.artist = gmbox.albuminfo["artist"]             
        self.album.cover = gmbox.albuminfo["cover"]    
        self.album.time = gmbox.albuminfo["time"]
        self.callback(gmbox.songlist, self.album)
        
class Downloader(threading.Thread):
    
    def __init__(self, track, running, parent):
        threading.Thread.__init__(self)
        self.track = track
        self.running = running
        self.parent = parent
            
    def run(self):
        if self.running.isSet(): 
            if self.track.from_album and self.track.download_cover: 
                self.download_cover()   
            if self.track.download_lyric: 
                self.download_lyric()            
            self.download_mp3()       
        self.parent.treeview.queue_draw()
        self.running.clear()
        self.parent.downloader_notify()
        
    def all_files_exists(self, *urls):
        for url in urls:
            if not os.path.exists(url):
                return False
        return True
    
    def get_safe_path(self, url):
        not_safe_chars = '''\/:*?<>|'"'''
        if len(url) > 243:
            url = url[:238]
        for char in not_safe_chars:
            url = url.replace(char, "")
        return url        
        
    def download_cover(self):
        # create folder
        if self.track.from_album:
            path = os.path.join(self.track.folder, self.get_safe_path(self.track.album))
        else:
            path = self.track.folder               
        if not os.path.exists(path):
            #TODO: it is not safe, other thread may have created
            try:
                os.makedirs(path)
            except:
                return              
        
        filename = "cover.jpg"
        local_url = os.path.join(path, filename)
        unfinish_url = local_url + ".part"            
        
        # check download
        if not self.all_files_exists(local_url, unfinish_url):        
            # get url
            url = self.track.cover
            if url != "":
                try:                                                   
                    urllib.urlretrieve(url, unfinish_url)
                    if self.all_files_exists(local_url, unfinish_url):
                        os.remove(unfinish_url)
                    elif os.path.exists(unfinish_url):
                        os.rename(unfinish_url, local_url)
                except:
                    traceback.print_exc()
        
    def download_lyric(self):
        # create folder
        if self.track.from_album:
            path = os.path.join(self.track.folder, self.get_safe_path(self.track.album))
        else:
            path = self.track.folder               
        if not os.path.exists(path):
            os.makedirs(path)       
        
        filename = self.get_safe_path(self.track.filename) + ".lrc"
        local_url = os.path.join(path, filename)
        unfinish_url = local_url + ".part"            
        
        # check download
        if not self.all_files_exists(local_url, unfinish_url):           
            # get url
            url = gmbox.get_lyric_url(self.track.id)
            if url is None:
                self.track.status = Track.STATUS_NO_LYRIC
            else:
                try:                                                   
                    urllib.urlretrieve(url, unfinish_url)
                    if self.all_files_exists(local_url, unfinish_url):
                        os.remove(unfinish_url)
                    elif os.path.exists(unfinish_url):
                        os.rename(unfinish_url, local_url)
                except:
                    traceback.print_exc()
        
    def download_mp3(self):
        # create folder
        if self.track.from_album:
            path = os.path.join(self.track.folder, self.get_safe_path(self.track.album))
        else:
            path = self.track.folder               
        if not os.path.exists(path):
            os.makedirs(path)       
        
        filename = self.get_safe_path(self.track.filename) + ".mp3"
        local_url = os.path.join(path, filename)
        unfinish_url = local_url + ".part"            
        
        # check download
        if self.all_files_exists(local_url, unfinish_url):    
            self.track.status = Track.STATUS_EXIST
            self.track.url = local_url
            self.track.process = "100%"
        else:            
            # get url
            url = gmbox.find_final_uri(self.track.id)
            if url is None:
                self.track.status = Track.STATUS_GET_URL_FAIL
            else:
                self.track.status = Track.STATUS_DOWNLOADING
                try:                                                   
                    urllib.urlretrieve(url, unfinish_url, self.process)
                    if self.all_files_exists(local_url, unfinish_url):
                        os.remove(unfinish_url)
                    elif os.path.exists(unfinish_url):
                        os.rename(unfinish_url, local_url)
                        self.track.status = Track.STATUS_DOWNLOADED
                        self.track.url = local_url
                        self.track.process = "100%"
                except:
                    traceback.print_exc()
                    self.track.status = Track.STATUS_DOWNLOAD_FAIL
                    self.track.process = "0%"
               
    def process(self, block, block_size, total_size):
        if total_size < 0.5 * 1024 * 1024:
            print "Too small file size， %dKB" % (total_size / 1024)
            raise
        downloaded_size = block * block_size
        percent = float(downloaded_size) / total_size
        if percent >= 1:
            process = "100%"
        elif percent <= 0:
            process = "0%"
        elif percent < 0.1:
            process = str(percent)[3:4] + "%"
        else:
            process = str(percent)[2:4] + "%"            
        self.track.process = process
        self.parent.treeview.queue_draw()

class PlayerRunnerer(threading.Thread):
    
    def __init__(self, url, player):
        threading.Thread.__init__(self)
        self.url = url.decode("utf-8").encode(sys.getfilesystemencoding())
        self.player = player
            
    def run(self):     
        cmd = [self.player, self.url]
        retcode = subprocess.call(cmd)
        print "Player thread has stoped"    

if __name__ == '__main__':
    gtk.gdk.threads_init()
    GMBoxPanel().main_window.show()
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
