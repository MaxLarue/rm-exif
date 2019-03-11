#!python
from PIL.ExifTags import TAGS
from PIL import Image
import argparse

"""
    A command line utility to remove exif data from an image and transform it so that it
    display nicely everywhere.

    usage 
        rm-exif -s ./file.jpg -d ./out.jpg
    or
        rm-exif -s ./in-directory/* -d ./out-directory/*

    Requires Pillow

"""

"""
    Exif tags define these angles as the device orientation when the photo
    was taken. This dict links the angle id to the rotation that'll cancel
    the transformation
"""
ORIENTATION_ANGLES = {
    #angle to undo modification
    3 : 180,
    5 : 360-270,
    6 : 360-90,
    7 : 360-90,
    8 : 360-270
}

"""
    Exif tags can specify a combination of horizontal/vertical mirror.
"""
MIRROR_ANGLE = {
    #0= horizontal, 1=vertical
    2 : 0,
    4 : 1,
    5 : 0,
    7 : 0
}

def getExifTransformation(orientation):
    angle = 0
    mirror = None
    if(orientation in ORIENTATION_ANGLES.keys()):
        angle = ORIENTATION_ANGLES[orientation]
    if(orientation in MIRROR_ANGLE.keys()):
        mirror = MIRROR_ANGLE[orientation]
    return (angle, mirror)


def getExif(i):
    ret = {}
    info = i._getexif()
    if(info):
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        return ret
    #else
    return None

def getExifOrientation(exif):
    return exif["Orientation"]

def rotateIfExif(image):
    img = image
    exif = getExif(img)
    hasExif = True if not exif is None else False
    try:
        if(hasExif):
            orientation = getExifOrientation(exif)
    except KeyError:
        hasExif = False
    if(hasExif):
        angle, mirror = getExifTransformation(orientation)
        img2 = img.rotate(angle, expand=True)
        if(not mirror is None):
            if(mirror == 0):
                img2 = img2.transpose(Image.FLIP_LEFT_RIGHT)
            else:
                img2 = img2.transpose(Image.FLIP_TOP_BOTTOM)
        return img2

"""
    Removing exif
"""

def process(name, file):
    ext = name.split(".")[-1].upper()
    imgType = ext.upper()
    if(ext.upper() == 'JPG' or ext.upper() == "JPEG"):
        imgType = 'JPEG'
    #removing exif
    if(imgType == 'JPEG'):
        tmp = rotateIfExif(file)
        if(not tmp is None):
            return tmp
        #exif rotation failed
        return file
    #not an image or no exif
    return content

"""

  Actual script interface

"""

parser = argparse.ArgumentParser(description='Remove exif data from a picture, rotating it so that it display nicely everywhere')
#source image path
parser.add_argument('-s', '--source', nargs='*', dest='path', help='the original image from which to remove exif data')
#destination path
parser.add_argument('-d', '--destination', nargs='*', dest='dest', help='where to save the resulting image')

#collecting and converting args into a dict
args = parser.parse_args()
args = vars(args)

def rmExif(origin, destination):
  with Image.open(origin) as image:
    image = process(origin, image)
    image.save(destination)

assert(len(args['path']) == len(args['dest']))

for i in range(len(args['path'])):
  rmExif(args['path'][i], args['dest'][i])