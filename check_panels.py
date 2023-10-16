#!/usr/bin/env python

import os, glob, argparse
from micasense.image import Image
from micasense.panel import Panel
import micasense.plotutils as plotutils

parser = argparse.ArgumentParser(
    prog='check_panels',
    description='Checks images for presense of panels',  
    formatter_class=argparse.ArgumentDefaultsHelpFormatter  
)
parser.add_argument('path2panels', default=os.getcwd(), type=str, help="Path to project")
args=parser.parse_args()

imagePath = args.path2panels

count_good=0
count_bad=0
for i in  sorted(glob.glob(os.path.join(imagePath,'*.*'))):
    img = Image(i)
    panel = Panel(img)

    print(f"\nFile: {i}")
    if not panel.panel_detected():
        print("Panel Not Detected!")
        count_bad += 1
    else:
        print("Panel detected, serial: {}".format(panel.serial)) 
        mean, std, num, sat_count = panel.raw()
        print("Extracted Panel Statistics:")
        print("Mean: {}".format(mean))
        print("Standard Deviation: {}".format(std))
        print("Panel Pixel Count: {}".format(num))
        print("Saturated Pixel Count: {}".format(sat_count))
        count_good += 1

print(f'\n{count_good} panels OK, {count_bad} panels not detected')
