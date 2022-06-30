# run once for the existing data; check if everything is correct; double check 'cleaned' title + track number
import os
from mutagen.easyid3 import EasyID3
import json

db = {}
ROOT_PATH = 'E:\podcasts'

# loop through the existing podcast directory
for subdir, dirs, files in os.walk(ROOT_PATH):
    for dir in dirs:
        episodes = sorted(next(os.walk(os.path.join(subdir, dir)), (None, None, []))[2])
        # ignore cover art (jpg & png)
        episodes = [fi for fi in episodes if not fi.endswith((".jpg", ".png", ".m4b", ".ogg"))]
        # after listing and ordering all files, pick the last (newest) one
        newest_episode = EasyID3(f'{os.path.join(subdir, dir)}/{episodes[-1]}')

        try:
            cleaned_title = newest_episode['artist'][0]
        except KeyError:
            cleaned_title = 'NA'
        try:
            track = int(newest_episode["tracknumber"][0])
        except KeyError:
            track = 0
        except ValueError:
            track = newest_episode["tracknumber"][0]
            
        info = {dir: {'dest_path': os.path.join(subdir, dir),
                        'artist_messy': dir,
                        'artist_cleaned': cleaned_title,
                        'current_track': track
                        }
                  }
        db.update(info)

with open('db/podcast_db.json', 'w', encoding='utf-8') as jsonFile:
    json.dump(db, jsonFile, ensure_ascii=False, indent=4)