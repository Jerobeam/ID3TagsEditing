# encoding: Cp1252

import eyed3
import os

# directory = raw_input("Please provide the filepath to the folder in which the mp3 files should be edited: ")

directory = "C:\Users\Sebastian\Desktop\Musik"

version22counter = 0

for dirName, subdirList, files in os.walk(directory, topdown=False):
    for fname in files:

        filepath = os.path.join(dirName, fname)
        print filepath

        if fname.lower().endswith('.mp3'):
            mp3 = eyed3.load(filepath)
        else:
            # Skip iteration for non mp3 files
            continue

        # Try to edit tags if possible (not working for ID3 V 2.2.0)
        if mp3.tag.version != (2, 2, 0):
            title = mp3.tag.title
            artist = mp3.tag.artist
            album = mp3.tag.album

            # edit title
            if title is None:
                mp3.tag.title = u"" + os.path.splitext(fname)[0].decode("Cp1252")
                mp3.tag.save()

        else:
            version22counter += 1

print("-----------")
print "Amount of MP3 Files with ID3 V 2.2.0: ", version22counter
