import os
import time
from exif import Image

# set location for pictures to be read
location = 'H:\Pictures\\2021 Wedding\\3_Reception'

# add pictures to array for manipulation
pictures = []
for (dirpath, dirnames, picturenames) in os.walk(location):
    pictures.extend(picturenames)
    break

print(pictures)

# current naming convention, length, and dictionary to hold pictures for better sorting (by number instead of char)
pictureNameStart = '3_Reception_'
pictureNameStartLength = len(pictureNameStart)
picturesDictionary = {}

# add pictures to dictionary using picture:number as key:value
for picture in pictures:
    pictureNameEndIndex = len(picture) - 4
    picturesDictionary[picture] = int(picture[pictureNameStartLength:pictureNameEndIndex])

# sort pictures and store in new dictionary
print(picturesDictionary)
sortedPicturesDictionary = sorted(picturesDictionary.items(), key=lambda x: x[1], reverse=False)
print(sortedPicturesDictionary)

# update the names of pictures by adding a number to the end
def updatePictureNames(picturesDictionary):
    # value to start numbering at
    counter = 1000
    for picture, number in picturesDictionary:
        # set picture location with picture name
        oldPicturePath = location + '\\' + str(picture)
        newPicturePath = location + '\\3_Reception_' + str(counter) + '.jpg'
        print('Old picture name/path: ' + oldPicturePath)
        print('New picture name/path: ' + newPicturePath)
        os.rename(oldPicturePath, newPicturePath)
        counter = counter + 1000

# update the last modified date times and EXIF date taken times on pictures
def updateTimes(picturesDictionary):
    # time to start at
    lastModifiedEpoch = 1625100000 # 12:40AM

    for picture, number in picturesDictionary:
        # set picture location with picture name
        picturePath = location + '\\' + picture
        print('Picture name/path: ' + picturePath)

        # get the last modified property from the picture
        stinfo = os.stat(picturePath)
        print("Current modified time: %s" %stinfo.st_mtime)

        # last modified on the picture uses epoch, while the EXIF data uses a datetime format
        lastModifiedEpoch += 60
        lastModifiedDateTime = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(lastModifiedEpoch))

        print("New modified epoch time: " + str(lastModifiedEpoch))
        print("New date time: " + lastModifiedDateTime)
        os.utime(picturePath, (lastModifiedEpoch, lastModifiedEpoch))

        # update EXIF data
        image = Image(picturePath)
        if image.has_exif:
            image.datetime_digitized = lastModifiedDateTime
            image.datetime_original = lastModifiedDateTime
            print("datetime_digitized: " + image.get('datetime_digitized'))
            print("datetime_original: " + image.get('datetime_original'))

            # save updated picture to new location
            with open('H:\Pictures\\2021 Wedding\\3_Reception_new\\' + picture, 'wb') as updatedFile:
                updatedFile.write(image.get_file())

updatePictureNames(sortedPicturesDictionary)
updateTimes(sortedPicturesDictionary)