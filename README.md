## A custom script for managing podcast metadata and organization

This repository contains a set of scripts designed specifically for my use case. I run an UNRAID server with an instance of gPodder to download podcasts. However, gPodder does not properly tag the mp3 files with metadata. To address this issue, I created these scripts to tag new podcast episodes (including the correct track number) in a watched folder and move them to a destination folder.

### Scripts:
1. *db_creation.py*: To create a database of already existing podcasts, run this script first. The script will iterate over your podcasts and extract information, used to tag future episodes.

2. *tagging_moving_podcasts.py*: This script uses the information from the database created by db_creation.py to tag new podcast episodes with the appropriate metadata and move them to the destination folder.

### db_creation.py
This script moves podcast files between folders and updates or adds tags for each file. It relies on a database created by the db_creation.py script to determine the current track numbers and uses this information to properly tag new podcast episodes.

**Usage**:
1. Ensure that you have run the db_creation.py script first to create a database of your existing podcasts.
2. Place the new podcast files in the input folder.
3. Run this script (tagging_moving_podcasts.py) to update or add tags and move podcast files to the destination folder.

The script will read from the database, update the tags (including album, artist, track number, genre, and date), save the updated metadata, and move the files to their designated destination folders. The script also updates the highest track number in the database file.
