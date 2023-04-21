"""
This script moves podcasts between folders and updates/adds tags for each file.
It relies on a database created by the 'db_creation.py' script to determine the current track numbers
and uses this information to properly tag new podcast episodes.
"""

import os
from mutagen.easyid3 import EasyID3
import json

INPUT_PATH = 'input'
DEST_PATH = 'destination'
DB_PATH = 'db/podcast_db.json'

# Loop through folders to extract file names
for dirpath, dirs, files in os.walk(INPUT_PATH):
    for file in files:
        # Ignore cover art (jpg & png)
        if not file.endswith((".jpg", ".png")):
            # Load the database created by the db_creation.py script
            with open(DB_PATH, "r", encoding='utf-8') as database:
                db = json.load(database)

                current_file = f'{dirpath}\\{file}'
                podcast_folder = dirpath.split(os.sep)[1]
                podcast = EasyID3(current_file)

                # Get the new tags from file path, existing mp3, or the database file
                artist = db[podcast_folder]['artist_cleaned']
                track = (db[podcast_folder]['current_track']) + 1
                genre = 'Podcast'
                date = file.split(' - ')[0]
                album = date[:4]  # Group episodes by year
                title = podcast['title'][0]

                # Update/add the tags for the current file
                podcast['albumartist'] = artist
                podcast['artist'] = artist
                podcast['album'] = album
                podcast['tracknumber'] = str(track)  # tracknumber must also be a string
                podcast['genre'] = genre
                podcast['date'] = date
                podcast['title'] = title

                # Save the tag info
                podcast.save()

                # Move the podcasts from temp dir to destination
                os.rename(current_file, f'{DEST_PATH}\\{podcast_folder}\\{file}')

                # Update the highest track number in the database file
                db[podcast_folder]['current_track'] = track
                with open(DB_PATH, "w", encoding='utf-8') as jsonFile:
                    json.dump(db, jsonFile, ensure_ascii=False, indent=4)
