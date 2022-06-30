A script very specific for my use case.
I run an UNRAID server with an instant of gpodder to download podcasts. However, gpodder is not properly tagging the mp3 files.
Therefore, I wrote a script to tag new podcasts (including the correct track number) in a watched folder and move them to a destination folder.

To create a database of already existing podcasts, run 'db_creation.py' first. The script will iterate over your podcasts and extract information, used to tag future episode (done by 'tagging_moving_podcasts.py').
