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

import gtk
import gobject
import os
import sys
import traceback
               
def create_icon_dict():
    
        if hasattr(sys, "frozen"):
            module_path = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
        else:
            module_path = os.path.dirname(unicode(os.path.abspath(__file__), sys.getfilesystemencoding()))
        
        names = {"Track":"track.png",
                 "Album":"album.png",
                 "Holder":"refresh.png",
                 "Search":"listing.png",
                 "Error":"missing.png"}
    
        icon_dict = {}
        iconTheme = gtk.icon_theme_get_default()
        for key in names.keys():
            try:
                inon_path = module_path + "/pixbufs/" + names[key]
                icon_dict[key] = gtk.gdk.pixbuf_new_from_file(inon_path)
            except:
                icon_dict[key] = None
        return icon_dict
    
icon_dict = create_icon_dict()

class TreeItem():
    
    def __init__(self, id):
        self.id = id
        
class Track(TreeItem):
    
    STATUS_NOT_DOWNLOAD = "未下载"
    STATUS_WAITING = "等待中"
    STATUS_GETTING_URL = "获取地址中"
    STATUS_GET_URL_FAIL = "获取地址失败，换个IP或稍后重试"
    STATUS_DOWNLOADING = "下载中"
    STATUS_DOWNLOADED = "已完成" 
    STATUS_DOWNLOAD_FAIL = "下载失败"
    STATUS_NO_LYRIC = "歌词可能不存在"
    STATUS_DUPLICATE = "同名歌曲已在列表中"
    STATUS_EXIST = "同名歌曲已下载"
    
    def __init__(self, id, title, artist, album):
        TreeItem.__init__(self, id)
        if album != "":
            self.name = "%s - %s - %s" % (title, artist, album)
        else:
            self.name = "%s - %s" % (title, artist)
        self.name1 = "%s - %s" % (title, artist)
        self.filename = "%s - %s" % (artist, title)
        self.title = title
        self.artist = artist
        self.album = album
        self.icon = icon_dict["Track"]
        self.url = ""
        self.process = "0%"
        self.status = Track.STATUS_NOT_DOWNLOAD
        self.from_album = False
        self.download_lyric = True
        self.download_cover = True
        self.in_downlist = False
        self.in_playlist = False
        self.cover = ""
        
class Album(TreeItem):
    
    def __init__(self, id, title, memo):
        TreeItem.__init__(self, id)
        self.title = title
        self.memo = memo
        self.name = "%s - %s" % (title, memo.split(".")[0])
        self.icon = icon_dict["Album"]
        self.text = "" 
        self.path = None
        self.expanded = False
        
        self.company = ""  
        self.artist = ""             
        self.cover = ""    
        self.time = ""

class Holder(TreeItem):
        
    def __init__(self, id, name):
        TreeItem.__init__(self, id)
        self.name = name
        self.type = 0
        self.text = ""
        self.page = ""
        self.icon = icon_dict["Holder"]
        self.loaded = False
        
class Search(TreeItem):
        
    def __init__(self, id, name, type=0):
        TreeItem.__init__(self, id)
        self.name = name
        self.type = type
#        self.text = name.decode('utf8')
        self.text = name
        if type == 3:
            self.icon = icon_dict["Track"]
        elif type == 4:
            self.icon = icon_dict["Album"]
        else:
            self.icon = icon_dict["Search"]
        self.expanded = False
        
class GmTreeview(gtk.TreeView):
    
    def __init__(self):
        gtk.TreeView.__init__(self)
        self.liststore = gtk.ListStore(gobject.TYPE_PYOBJECT) 
        self.modelsort = gtk.TreeModelSort(self.liststore)
        self.set_model(self.modelsort)
        self.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
               
    def modelsort_sort_func(self, model, iter1, iter2, data=None):
        if iter1 and iter2:
            track1 = model.get_value(iter1, 0)
            track2 = model.get_value(iter2, 0)
            if track1 is None or track2 is None:
                return 1
            else:
                return cmp(getattr(track1, data), getattr(track2, data))
        else:
            return 1       
        
    def create_column_text(self, id, text, data, cell_func=None):
        renderer = gtk.CellRendererText()            
        column = gtk.TreeViewColumn(text, renderer) 
        if cell_func is None:
            column.set_cell_data_func(renderer, self.text_cell_data_func, data)
        else:
            column.set_cell_data_func(renderer, cell_func, data)
        column.set_sort_column_id(id)
        column.set_resizable(True)
        self.modelsort.set_sort_func(id, self.modelsort_sort_func, data)
        return column  
    
    def create_column_pixbuf_text(self, id, text, data, cell_func=None): 
        renderer = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn(text)
        column.pack_start(renderer, False)
        column.set_cell_data_func(renderer, self.pixbuf_cell_data_func, "icon")
        
        renderer = gtk.CellRendererText()
        column.pack_start(renderer)
        if cell_func is None:
            column.set_cell_data_func(renderer, self.text_cell_data_func, data)
        else:
            column.set_cell_data_func(renderer, cell_func, data)
        column.set_sort_column_id(id)
        column.set_resizable(True)
        self.modelsort.set_sort_func(id, self.modelsort_sort_func, data)
        return column
                    
    def pixbuf_cell_data_func(self, column, cell, model, iter, data=None):
        if iter:
            try:
                track = model.get_value(iter, 0)
                cell.set_property("pixbuf", getattr(track, data))
            except:
                traceback.print_exc()
                cell.set_property("pixbuf", icon_dict["Error"])
        else:
            cell.set_property("pixbuf", icon_dict["Error"])
            
    def text_cell_data_func(self, column, cell, model, iter, data=None):
        if iter:
            try:
                track = model.get_value(iter, 0)
                cell.set_property("text", getattr(track, data))
            except:
                traceback.print_exc()
                cell.set_property("text", "出现未知错误")
        else:
            cell.set_property("text", "出现未知错误")

class ResultTreeview(GmTreeview):
    
    def __init__(self):
        GmTreeview.__init__(self)
               
        column = self.create_column_pixbuf_text(0, " ", "name", self.column_cell_data_func)
        self.append_column(column)               
        self.set_headers_visible(False)         
        
    def column_cell_data_func(self, column, cell, model, iter, data=None):
        treeitem = model.get_value(iter, 0)
        if isinstance(treeitem, Track) and model.iter_depth(iter) != 0:
            cell.set_property("text", treeitem.name1)
        else:
            cell.set_property("text", treeitem.name)
        
class ListingTreeview(GmTreeview):
    
    def __init__(self):
        GmTreeview.__init__(self)
               
        column = self.create_column_pixbuf_text(0, " ", "name")
        self.append_column(column)               
        self.set_headers_visible(False)

class DownloadTreeview(GmTreeview):
    
    def __init__(self):
        GmTreeview.__init__(self)      
        
        column = self.create_column_pixbuf_text(0, "标题", "title")
        self.append_column(column)               

        text = ["歌手", "进度", "状态"]
        data = ["artist", "process", "status"]        
        for i in range(3):
            column = self.create_column_text(i + 1, text[i], data[i])
            self.append_column(column)
        
class PlaylistTreeview(GmTreeview):
    
    def __init__(self):
        GmTreeview.__init__(self)  
                
        column = self.create_column_pixbuf_text(0, "标题", "title")
        self.append_column(column)       

        text = ["歌手", "专辑"]
        data = ["artist", "album"]
        
        for i in range(2):
            column = self.create_column_text(i + 1, text[i], data[i])
            self.append_column(column)
