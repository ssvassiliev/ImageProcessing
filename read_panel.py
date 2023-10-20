#!/usr/bin/env python

import os, glob, argparse
from micasense.image import Image
from micasense.panel import Panel
import micasense.plotutils as plotutils

panelCorners = [[809,613],[648,615],[646,454],[808,452]]


parser = argparse.ArgumentParser(
    prog='check_panels',
    description='Checks images for presense of panels',  
    formatter_class=argparse.ArgumentDefaultsHelpFormatter  
)
parser.add_argument('filename', default='IMG_0000_1.tif', type=str, help="Panel file")
parser.add_argument('-a', '--albedo', type=float, nargs='+', help="List of panel albedos")
args=parser.parse_args()

img = Image(args.filename)

panel = Panel(img, panelCorners = panelCorners) 
mean, std, num, sat_count = panel.raw()
print("Extracted Panel Statistics:")
print(f'Mean: {mean}')
print(f'Standard Deviation: {std}')
print(f'Panel Pixel Count: {num}')
print(f'Saturated Pixel Count: {sat_count}') 
panel_irradiance=panel.irradiance_mean(args.albedo)  


print(f'Panels reflectance: {args.albedo}')
print(f'Panels irradiance: {panel_irradiance}')



