#!/usr/bin/env python

import os, glob, argparse
import numpy as np
from micasense.image import Image
from micasense.panel import Panel
import micasense.plotutils as plotutils


parser = argparse.ArgumentParser(
    prog='check_panels',
    description='Checks images for presense of panels',  
    formatter_class=argparse.ArgumentDefaultsHelpFormatter  
)
parser.add_argument('path2panels', default=os.getcwd(), type=str, help="Path to project")
parser.add_argument('-f', '--filename', default='IMG_0000_', type=str, help="Name of panel image files")
parser.add_argument('-n', '--nbands', default=10, type=int, help="Number of bands")
args=parser.parse_args()

imagePath = args.path2panels

countOK=0
countNoAlbedo=0
countTotal=0
countFailed=0
countNoQR=0
failed=[]
panels_albedo=[]
panels_irradiance = []
corr_fact = []

for i in  range(0,args.nbands):
    panelName=f'{imagePath}/{args.filename}{str(i+1)}.tif'
    countTotal += 1
    img = Image(panelName)
    panel = Panel(img)

    print(f"\n{os.path.basename(panelName)}, {img.band_name}")
    if not panel.panel_detected():
        print("Error: Panel not detected!")
        panels_albedo.append(np.nan)
        panels_irradiance.append(np.nan)
        corr_fact.append(np.nan)
        failed.append(os.path.basename(panelName))
        countFailed += 1
        countNoQR += 1
        continue
    if not hasattr(panel,"panel_albedo"):
        print("Error: Cannot read albedo!")
        panels_albedo.append(np.nan)
        panels_irradiance.append(np.nan)
        corr_fact.append(np.nan)
        failed.append(os.path.basename(panelName))
        countNoAlbedo += 1
        countFailed += 1
        continue
    else:
        mean, std, num, sat_count = panel.raw()
        print(f'Serial: {panel.serial}, \nAlbedo: {panel.panel_albedo:.4f}')
        print(f'Mean: {mean:.1f}, SD: {std:.1f}')
        print(f'Panel Pixel Count: {num}')
        print(f'Saturated Pixel Count: {sat_count}')
        print(f'Panel Mean Irradiance: {panel.irradiance_mean(panel.panel_albedo):.4f}') 
        print(f'Panel Albedo: {panel.panel_albedo:.4f}') 
        panels_albedo.append(panel.panel_albedo)
        panels_irradiance.append(panel.irradiance_mean(panel.panel_albedo)) 
        corr=panel.reflectance_mean()/panel.panel_albedo
        corr_fact.append(corr)
        img.reflectance(img.horizontal_irradiance * corr ) 
        print(f'Corrected Mean Reflectance: {panel.reflectance_mean():.4f}') 
        countOK += 1

print("\n")
if countTotal == 0:
    print("Panels not found")
if countNoAlbedo > 0:
    print(f'Error: could not read albedo from {countNoAlbedo} panel(s)')
if countNoQR > 0:
    print(f'Error: {countNoQR} panel(s) not detected:')  
if countFailed > 0:
    print(f'Error: {countFailed} panel(s) failed:')
if countFailed == 0:
    print("All panels OK")
print("\n")

print("Albedo:")
for i in panels_albedo:
    print(f'{i:.4f}, ', end='')
print("\nIrradiance:")
for i in panels_irradiance:
    print(f'{i:.4f}, ', end='')
print("\nIrradiance correction factors:")
for i in corr_fact:
    print(f'{i:.4f}, ', end='')
print("\n")

