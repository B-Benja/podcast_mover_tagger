"""
This script generates a JSON file containing information about the latest episodes of podcasts 
from a given directory. It stores the information in 'podcast_db.json'.
"""

import os
from mutagen.easyid3 import EasyID3
import json

podcast_database = {}
ROOT_PATH = 'E:\podcasts'

# loop through the existing podcast directory
for subdir, dirs, files in os.walk(ROOT_PATH):
    for podcast_dir in dirs:
        episodes = sorted(next(os.walk(os.path.join(subdir, podcast_dir)), (None, None, []))[2])
        # Filter out non-audio files (cover art and non-supported formats)
        episodes = [file for file in episodes if not file.endswith((".jpg", ".png", ".m4b", ".ogg"))]
        # after listing and ordering all files, pick the last (newest) one
        latest_episode_metadata = EasyID3(f'{os.path.join(subdir, podcast_dir)}/{episodes[-1]}')

        try:
            cleaned_title = latest_episode_metadata['artist'][0]
        except KeyError:
            cleaned_title = 'NA'
        try:
            track = int(latest_episode_metadata["tracknumber"][0])
        except KeyError:
            track = 0
        except ValueError:
            track = latest_episode_metadata["tracknumber"][0]
            
        podcast_info = {podcast_dir: {'dest_path': os.path.join(subdir, podcast_dir),
                                      'artist_messy': podcast_dir,
                                      'artist_cleaned': cleaned_title,
                                      'current_track': track
                                      }
                        }
        podcast_database.update(podcast_info)

with open('db/podcast_db.json', 'w', encoding='utf-8') as jsonFile:
    json.dump(podcast_database, jsonFile, ensure_ascii=False, indent=4)
