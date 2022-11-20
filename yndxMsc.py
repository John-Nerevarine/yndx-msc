from yandex_music import Client
from yandex_music.exceptions import UnauthorizedError
import time
import vlc
import os
import sys
import random


clear = lambda: os.system('cls')

def getClient():
    try:
        with open ('token.txt') as file:
            token = file.readline()

        client = Client(token).init()
        print('Success Authorization.')
    except UnauthorizedError:
        print('Your OAuth token is likely expired')
        sys.exit()
    except:
        print("Can't read \"token.txt\"")
        sys.exit()

    return client


client = getClient()
userPlaylist = client.users_likes_tracks()
tracks = len(userPlaylist.tracks)
tracks = list(range(tracks))
random.shuffle(tracks)

trackIndex = 0

songs = [{'name': '', 'track': userPlaylist[tracks[trackIndex]].fetch_track()},
    {'name': '', 'track': None}]

while not(songs[0]['track'].available):
    trackIndex += 1
    songs[0]['track'] = userPlaylist[tracks[trackIndex]].fetch_track()

    if trackIndex >= len(tracks):
        print("All track unavailable.")
        input('Press <Enter> to exit')
        sys.exit()


clear()
print('Downloading...')
songs[0]['track'].download('song0.mp3')
name = ''
for artist in songs[0]['track'].artists:
    name += (artist.name + ', ')
name = name[0:-2]
    
songs[0]['name'] = f"{name} - {songs[0]['track'].title}"

queue = 0
while True:
    clear()
    print(songs[queue]['name'])
    player = vlc.MediaPlayer('song'+ str(queue) +'.mp3')
    player.play()
    
    queue = (queue + 1) % 2
    trackIndex += 1

    songs[queue]['track'] = userPlaylist[tracks[trackIndex]].fetch_track()
    while not(songs[queue]['track'].available):
        trackIndex += 1
        songs[queue]['track'] = userPlaylist[tracks[trackIndex]].fetch_track()

        if trackIndex >= len(tracks):
            trackIndex = 0
            songs[queue]['track'] = userPlaylist[tracks[trackIndex]].fetch_track()

    songs[queue]['track'].download('song'+ str(queue) +'.mp3')
    
    name = ''
    for artist in songs[queue]['track'].artists:
        name += (artist.name + ', ')
    name = name[0:-2]
    
    songs[queue]['name'] = f"{name} - {songs[queue]['track'].title}"

    length = player.get_length()

    while not(length):
        time.sleep(1)
        length = player.get_length()

    position = player.get_position()
    time.sleep((1 - position) * length / 1000)