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

listing_map = [
("最新音乐", (
        ("华语新歌", "chinese_new_songs_cn", 3),
        ("欧美新歌", "ea_new_songs_cn", 3),
        ("华语最新专辑", "chinese_new-release_albums_cn", 4),
        ("欧美最新专辑", "ea_new-release_albums_cn", 4),
        ("最新专辑", "new-release_albums_cn", 4),
        ("天翼爱音乐排行榜", "chinatelecom_love_music_songs_cn", 3),
    )
),
("华语", (
        ("华语热歌", "chinese_songs_cn", 3),
        ("华语新歌", "chinese_new_songs_cn", 3),
        ("华语热碟", "chinese_albums_cn", 4),
        #"华语歌手", ("chinese_artists_cn", 4)
    )
),
("欧美", (
        ("欧美热歌", "ea_songs_cn", 3),
        ("欧美新歌", "ea_new_songs_cn", 3),
        ("欧美热碟", "ea_albums_cn", 4),
        #("欧美歌手", "ea_artists_cn", 5),
    )
),
("日韩", (
        ("日韩热歌", "jk_songs_cn", 3),
        ("日韩热碟", "jk_albums_cn", 4),
        #"日韩歌手", "jk_artists_cn", 4)
    )
),
("流行", (
        ("流行热歌", "pop_songs_cn", 3),
        ("流行新碟", "pop_new_albums_cn", 4),
        ("流行热碟", "pop_albums_cn", 4),
    )
),
("摇滚", (
        ("摇滚热歌", "rock_songs_cn", 3),
        ("摇滚新碟", "rock_new_albums_cn", 4),
        ("摇滚热碟", "rock_albums_cn", 4),
    )
),
("嘻哈", (
        ("嘻哈热歌", "hip-hop_songs_cn", 3),
        ("嘻哈新碟", "hip-hop_new_albums_cn", 4),
        ("嘻哈热碟", "hip-hop_albums_cn", 4),
    )
),
("影视", (
        ("影视热歌", "soundtrack_songs_cn", 3),
        ("影视新碟", "soundtrack_new_albums_cn", 4),
        ("影视热碟", "soundtrack_albums_cn", 4),
    )
),
("民族", (
        ("民族热歌", "ethnic_songs_cn", 3),
        ("民族热碟", "ethnic_albums_cn", 4),
    )
),
("拉丁", (
        ("拉丁热歌", "latin_songs_cn", 3),
        ("拉丁热碟", "latin_albums_cn", 4),
    )
),
("R&B", (
        ("R&B热歌", "rnb_songs_cn", 3),
        ("R&B热碟", "rnb_albums_cn", 4),
    )
),
("乡村", (
        ("乡村热歌", "country_songs_cn", 3),
        ("乡村热碟", "country_albums_cn", 4),
    )
),
("民谣", (
        ("民谣热歌", "folk_songs_cn", 3),
        ("民谣热碟", "folk_albums_cn", 4),
    )
),
("灵歌", (
        ("灵歌热歌", "soul_songs_cn", 3),
        ("灵歌热碟", "soul_albums_cn", 4),
    )
),
("轻音乐", (
        ("轻音乐热歌", "easy-listening_songs_cn", 3),
        ("轻音乐热碟", "easy-listening_albums_cn", 4),
    )
),
("爵士蓝调", (
        ("爵士蓝调热歌", "jnb_songs_cn", 3),
        ("爵士蓝调热碟", "jnb_albums_cn", 4),
    )
)]

def create_listing_map_dict():     
    listing_map_dict = {}
    for listing_parent in listing_map:
        for listing in listing_parent[1]:
            listing_map_dict[listing[0]] = listing[1]
    return listing_map_dict

listing_map_dict = create_listing_map_dict()

list_url_template = 'http://www.google.cn/music/chartlisting?q=%s&cat=song&start=%d'
albums_list_url_template = 'http://www.google.cn/music/chartlisting?q=%s&cat=album&start=%d'
album_song_list_url_template = 'http://www.google.cn/music/album?id=%s'
xml_album_song_list_url_template = 'http://www.google.cn/music/album?id=%s&output=xml'
search_url_template = 'http://www.google.cn/music/search?q=%s&cat=song&start=%d'
albums_search_url_template = 'http://www.google.cn/music/search?q=%s&cat=album&start=%d'
song_url_template = 'http://www.google.cn/music/top100/musicdownload?id=%s'
song_streaming_url_template = 'http://www.google.cn/music/songstreaming?id=%s&cad=pl_player&sig=%s&output=xml'
flash_player_key = 'c51181b7f9bfce1ac742ed8b4a1ae4ed'
