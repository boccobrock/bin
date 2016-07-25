#!/usr/bin/env python

import sys
import os
import subprocess
import ConfigParser
from time import sleep
from gmusicapi import Mobileclient
from optparse import OptionParser
from random import shuffle

api = None
player = None
tracklist = []

def findPlaylist(playlist, playlists):
    plfound = None
    if(playlist.isdigit()):
        plfound = playlists[int(playlist)]
    else:
        for pl in playlists:
            if(pl['name'] == playlist):
                plfound = pl
    return plfound

def findTrack(track, playlist):
    item = None
    if(track.isdigit()):
        item = playlist['tracks'][int(track)]
    else:
        for sg in playlist['tracks']:
            if(sg['track']['title'] == track):
                item = sg
    return item

def printTrack(id, track):
    print str(id).ljust(3)[:3].encode('UTF-8') + ' ' + track['title'].ljust(30)[:30].encode('UTF-8') + ' ' + track['artist'].ljust(20)[:20].encode('UTF-8') + ' ' + track['album'].ljust(25)[:25].encode('UTF-8')
    sys.stdout.flush()

def play(url):
    with open(os.devnull, 'w') as temp:
        process = subprocess.Popen(["mpv", "--force-window=no", "--msg-level=all=no,statusline=status", "%s" % url])
        return process

def playTrack(tracklist, api):
    track = tracklist.pop(0)
    printTrack("", track)
    url = api.get_stream_url(track['trackId'])
    player = play(url)

def main():
    global player
    global api

    parser = OptionParser()
    parser.add_option("-p", "--playlist", dest="playlist", help="Playlist (Name or ID)")
    parser.add_option("-t", "--track", dest="track", help="Track (Name or ID)")
    parser.add_option("-l", "--listen", action="store_true", dest="listen", help="Start listening")
    parser.add_option("-c", "--continue", action="store_true", dest="cont", help="Continue playlist after track")
    parser.add_option("-s", "--shuffle", action="store_true", dest="shuffle", help="Randomize playlist")

    (opts, args) = parser.parse_args()

    config = ConfigParser.RawConfigParser()
    directory = os.path.dirname(os.path.realpath(sys.argv[0]))
    config.read(directory + '/.gmusicpy')
    username = config.get('gmusic', 'username')
    password = config.get('gmusic', 'password')

    api = Mobileclient()
    api.login(username, password, Mobileclient.FROM_MAC_ADDRESS)

    if not api.is_authenticated():
        print "Bad username/password"
        return

    id = 0

    try:
        if(opts.playlist):
            playlists = api.get_all_user_playlist_contents()
            playlist = findPlaylist(opts.playlist, playlists)
            
            if(playlist is None):
                print 'Playlist not found'
                return

            if(opts.track):
                item = findTrack(opts.track, playlist)

                if(item is None):
                    print 'Track not found'
                    return

                track = item['track']
                track['trackId'] = item['trackId']
                tracklist.append(track)

            else:
                for item in playlist['tracks']:
                    track = item['track']
                    track['trackId'] = item['trackId']
                    tracklist.append(track)

            if(opts.shuffle):
                shuffle(tracklist)

            if(opts.listen):
                track = tracklist.pop(0)
                printTrack("", track)
                url = api.get_stream_url(track['trackId'])
                player = play(url)
            else:
                for track in tracklist:
                    printTrack(id, track)
                    id = id + 1

        else:
            playlists = api.get_all_playlists()
            for playlist in playlists:
                print str(id) + ' ' + playlist['name']
                id = id + 1

        while(True):
            if player == None:
                break
            if isinstance(player, subprocess.Popen) and player.poll() != None:
                if(len(tracklist) > 0):
                    track = tracklist.pop(0)
                    printTrack("", track)
                    url = api.get_stream_url(track['trackId'])
                    player = play(url)
                else:
                    break;
            sleep(0.2)

    finally:
        if isinstance(player, subprocess.Popen):
            player.terminate()
        api.logout()

if __name__ == '__main__':
    main()
