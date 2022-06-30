# a small script to move podcasts between folders and update/add tags
import os
from mutagen.easyid3 import EasyID3
import json

INPUT_PATH = 'input'
DEST_PATH = 'destination'
DB_PATH = 'db/podcast_db.json'

# loop through folders to extract file names
for dirpath, dirs, files in os.walk(INPUT_PATH):
    for file in files:
        # ignore cover art (jpg & png)
        if not file.endswith((".jpg", ".png")):
            # load database which was created by the db_creation.py script
            # needed to store the current track number
            with open(DB_PATH, "r", encoding='utf-8') as database:
                db = json.load(database)

                current_file = f'{dirpath}\\{file}'
                podcast_folder = dirpath.split(os.sep)[1]
                podcast = EasyID3(current_file)

                # get the new tags from either file path, existing mp3 or the database file
                # instead of the podcast title, you adjust the next line to actually use the artist names
                artist = db[podcast_folder]['artist_cleaned']
                track = (db[podcast_folder]['current_track'])+1
                genre = 'Podcast'
                date = file.split(' - ')[0]
                # album = db[podcast_folder]['artist_cleaned'] # if you want the album title and podcast name to be the same
                # album = year of episode to group episodes by year
                album = date[:4]
                title = podcast['title'][0]

                # update/add the tags for the current file
                podcast['albumartist'] = artist
                podcast['artist'] = artist
                podcast['album'] = album
                podcast['tracknumber'] = str(track) # traknumber must also be a string
                podcast['genre'] = genre
                podcast['date'] = date
                podcast['title'] = title

                # save the tag info
                podcast.save()

                # move the podcasts from temp dir to destination
                os.rename(current_file, f'{DEST_PATH}\\{podcast_folder}\\{file}')

                # update the highes tracknumber in database file
                db[podcast_folder]['current_track'] = track
                with open(DB_PATH, "w",  encoding='utf-8') as jsonFile:
                    json.dump(db, jsonFile, ensure_ascii=False, indent=4)