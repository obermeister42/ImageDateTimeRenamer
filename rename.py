import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS
from os.path import join
from glob import glob
import argparse

def renameImage(imagename):
    # extract EXIF data
    image = Image.open(imagename)
    exifdata = image.getexif()
    # iterating over all EXIF data fields
    for tag_id in exifdata:
     # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        if tag == "DateTimeOriginal":
            data = exifdata.get(tag_id)
            sList = data.split()
            data = sList[0] + "_" + sList[1]
            data = data.replace(":", "_")
            image.close()
            filename, fileextension = os.path.splitext(imagename)
            newFileName = os.path.dirname(imagename) + "\\" + data + fileextension
            print(imagename + " ---> " + newFileName)
            try:
                os.rename(imagename, newFileName)
            except IOError as e:
                print ("error: " + e.errno + " " + e)
        else:
            print("Image time not found: " + imagename)
                
        

parser = argparse.ArgumentParser(description='Examines all images in directory, extracts time photo was taken from metadata, and renames the file with this timestamp.')
parser.add_argument('path', metavar='path', nargs='?',
                    help='path to files, defaults to current directory')
args = parser.parse_args()
fpath = str(os.getcwd())
if str(args.path) != "None":
    fpath = str(args.path)
print("Searching for matching images in: " + str(fpath))
files = []
for ext in ('*.gif', '*.png', '*.jpg', '*.jpeg','*.jpe','*.jif','*.jfif','*.jfi','*.tiff','*.tif','*.bmp','*.dib'):
   files.extend(glob(join(fpath, ext)))
for f in files:
    print(f)   
print ("")
print ("There were " + str(len(files)) + " files found. Rename? (Y/N)")  
ack = input()
if ack.upper() == "Y":
    for f in files:
        renameImage(f)
print("done")
