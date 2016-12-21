# m3truid
# Version: 0.1
# License: GNU GPLv3
# Description: Converts Android audio playlists to standard m3u
# Dependencies: Python 2.x, slugify
#	pip install slugify
# Run: in console
#	python m3truid.py
#   or launch the .py file

# Input: Android database at /data/data/com.android.providers.media
# adb root
# adb pull /data/data/com.android.providers.media/databases/external.db

import sqlite3
import codecs
from slugify import slugify
import os

# Not supported for now: audio.duration reliable?
keepDuration = False

defaultDatabase = "external.db"
databaseFile = raw_input("Database filename ("+defaultDatabase+"): ")
if databaseFile is "":
	databaseFile = defaultDatabase

lastPlaylist=None
try:
	db = sqlite3.connect(databaseFile)
	db.row_factory = sqlite3.Row
	
	cursor_findprefix = db.cursor()
	cursor_findprefix.execute('''SELECT audio._data FROM audio_playlists_map AS apm INNER JOIN audio_playlists AS ap INNER JOIN audio WHERE apm.playlist_id=ap._id AND apm.audio_id=audio._id ORDER BY RANDOM() LIMIT 20''')
	rand_paths = cursor_findprefix.fetchall()
	COLUMN = 0
	rand_paths_list=[elt[COLUMN] for elt in rand_paths]

	suggestPrefix = os.path.commonprefix(rand_paths_list) # TODO: Check if ends with \ or / 
	cropPrefix = raw_input("Media absolute base path ("+suggestPrefix+"): ")
	if cropPrefix is "":
		cropPrefix = defaultDatabase

	
	cursor_playlists = db.cursor()
	cursor_playlists.execute('''SELECT * FROM audio_playlists AS ap''')
	all_playlists = cursor_playlists.fetchall()
	for playlist in all_playlists:
	
		# Already a file playlist
		if playlist['_data']:
			continue

		print playlist['_id'],playlist['name']

		playlistFilename = slugify(playlist['name'])+".m3u"
		with codecs.open(playlistFilename, "w", encoding="utf8") as m3u_file:
			m3u_file.write(u'#EXTM3U\r\n')
		
			cursor_playlist_items = db.cursor()
			cursor_playlist_items.execute('''SELECT audio._data,artist,album,title,playlist_id FROM audio_playlists_map AS apm INNER JOIN audio WHERE apm.playlist_id=? AND apm.audio_id=audio._id ORDER BY apm.playlist_id''',(playlist['_id'],))
			all_tracks = cursor_playlist_items.fetchall()
			 
			for track in all_tracks:
				m3u_file.write(u'#EXTINF:-1,'+track['artist']+' - '+track['title']+'\r\n')
				track_path=track['audio._data']
				if cropPrefix:
					track_path=track_path.replace(cropPrefix,'',1)
				m3u_file.write(track_path+'\r\n')
				#print "\t",track['title']

			m3u_file.close()

except sqlite3.Error as e:
    #db.rollback()
    raise e
finally:
    db.close()