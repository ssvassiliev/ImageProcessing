import sys
from PIL import Image
from PIL.ExifTags import TAGS
from lxml import etree

#img = Image.open(sys.argv[1])
img = Image.open("IMG_0386_3.tif")
img_exif = img.getexif()

#for key, val in img_exif.items():
#    if key in TAGS:
#        print(f'{TAGS[key]}:{val}')

list = []
for key, val in img_exif.items():
    if key in TAGS:
        if TAGS[key]=="XMLPacket":
            root = etree.fromstring(val)
            print(f'{TAGS[key]}:{etree.tostring(root, pretty_print=True).decode()}')
        else:
            print(f'{TAGS[key]}:{val}')
            




