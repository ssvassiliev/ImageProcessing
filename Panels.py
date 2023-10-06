#!/usr/bin/env python

# # Panels
# This notebook shows usage for the Panel class.  This type is useful for detecting MicaSense calibration panels and extracting information about the lambertian panel surface.


import os, glob
from micasense.image import Image
from micasense.panel import Panel
import micasense.plotutils as plotutils

images = "/gpfs/project/6033915/svassili/ODM/ImageProcessing/data/panels/*"

for i in  sorted(glob.glob(images)):
    img = Image(i)
    panel = Panel(img)

    print(f"\nFile: {i}")
    if not panel.panel_detected():
        print("Panel Not Detected!")
    else:
        print("Detected panel serial: {}".format(panel.serial)) 
        mean, std, num, sat_count = panel.raw()
        print("Extracted Panel Statistics:")
        print("Mean: {}".format(mean))
        print("Standard Deviation: {}".format(std))
        print("Panel Pixel Count: {}".format(num))
        print("Saturated Pixel Count: {}".format(sat_count))


