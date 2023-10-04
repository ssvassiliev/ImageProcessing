#!/usr/bin/env python

# # Panels
# This notebook shows usage for the Panel class.  This type is useful for detecting MicaSense calibration panels and extracting information about the lambertian panel surface.


import os, glob
from micasense.image import Image
from micasense.panel import Panel
import micasense.plotutils as plotutils

imagePath = "/home/svassili/projects/def-svassili/svassili/ODM/panels"
imageFile='IMG_0000_7.tiff'

imageName = os.path.join(imagePath,imageFile)
img = Image(imageName)
panel = Panel(img)

if not panel.panel_detected():
    raise IOError("Panel Not Detected!")

print("Detected panel serial: {}".format(panel.serial))
mean, std, num, sat_count = panel.raw()
print(f"File: {imageFile}")
print("Extracted Panel Statistics:")
print("Mean: {}".format(mean))
print("Standard Deviation: {}".format(std))
print("Panel Pixel Count: {}".format(num))
print("Saturated Pixel Count: {}".format(sat_count))

fig = plotutils.plotwithcolorbar(img.raw(), title='Raw image values with colorbar')

