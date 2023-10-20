#!/usr/bin/env python

import os, glob, argparse
from micasense.image import Image
from micasense.panel import Panel
import micasense.plotutils as plotutils

parser = argparse.ArgumentParser(
    prog='read_panel',
    description='Calculates panel irradiance',  
    formatter_class=argparse.ArgumentDefaultsHelpFormatter  
)
parser.add_argument('filename', default='IMG_0000_1.tif', type=str, help="Panel path")
parser.add_argument('-a', '--albedo', required=True, type=float, nargs='+', help="Panel albedo")
parser.add_argument('-c', '--corners', required=True, type=int, nargs='+', help="Panel corners, [xmin ymin xmax ymax]")
args=parser.parse_args()

img = Image(args.filename)

panelCorners=[]
if args.corners is not None:
    panelCorners.append([args.corners[0],args.corners[1]])
    panelCorners.append([args.corners[2],args.corners[1]])
    panelCorners.append([args.corners[0],args.corners[3]])
    panelCorners.append([args.corners[2],args.corners[3]]) 
    panel = Panel(img, panelCorners = panelCorners) 
else:
    panel = Panel(img)

mean, std, num, sat_count = panel.raw()
print("Extracted Panel Statistics:")
print(f'Mean: {mean}')
print(f'Standard Deviation: {std}')
print(f'Panel Pixel Count: {num}')
print(f'Saturated Pixel Count: {sat_count}') 

panel_irradiance=panel.irradiance_mean(args.albedo)  
print(f'Panels reflectance: {args.albedo}')
print(f'Panels irradiance: {panel_irradiance}')



