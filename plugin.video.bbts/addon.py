#!/usr/local/bin/python
# coding: utf-8

import urllib
import urllib2
import sys
import re
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmc
import os
import updater

def unwrapValue(entry, key, default):
    v = None
    if key in entry:
        v = entry[key]
    if v == None:
        return default
    return v

def addVideoItem(name, url, iconimage, description):
    addon_handle = int(sys.argv[1])
    item = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    item.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
    item.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=item, isFolder=False)


def showFolderEntries(entries):
    for e in entries:
        title = unwrapValue(e,'title', 'Unknown')
        url = unwrapValue(e,'url', '')
        icon = unwrapValue(e,'tvg-logo', 'DefaultVideo.png')
        addVideoItem(title.strip(), url, icon, title)


def addFolders(folders):
    for f in folders:
        if f['icon'] == '':
            icon = 'DefaultFolder.png'
        else:
            icon = f['icon']
        url = sys.argv[0] + '?folder=' + urllib.quote_plus(f['name'])
        li = xbmcgui.ListItem(f['name'], iconImage=icon)
        li.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

update_status = updater.check_update()

if update_status == '':
    import generator
else:
    xbmcgui.Dialog().ok("Error", update_status)
    sys.exit(-1)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')

# xbmcgui.Dialog().ok("DEBUG", "[" + sys.argv[2] + "]")

entries = generator.parseList()

if "?folder=" in sys.argv[2]:
    name = sys.argv[2].split("=")[1]
    entries = generator.entriesInFolder(entries,urllib.unquote(name))
    #entries.sort(key=lambda x: x['title'])
    showFolderEntries(entries)
else:
    folders = generator.getFolders(entries)
    #folders.sort()
    addFolders(folders)
xbmcplugin.endOfDirectory(addon_handle)
