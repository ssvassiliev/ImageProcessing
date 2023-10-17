import os, glob, cv2, subprocess, argparse
import numpy as np
import micasense.capture as capture

parser = argparse.ArgumentParser(
    prog='undistort',
    description='Converts raw images to reflectance using DLS and Panels',  
    formatter_class=argparse.ArgumentDefaultsHelpFormatter  
)
parser.add_argument('-x', '--config', default=f'{os.getcwd()}/pix4d.config', type=str, help="Path to pix4d.config")
parser.add_argument('-d', '--project', default='data', type=str, help="Path to project")
parser.add_argument('-i', '--images', default='raw_images', type=str, help="Path to images")
parser.add_argument('-p', '--panels', default='panels', type=str, help="Path to panel images")
parser.add_argument('-t', '--output', default='images', type=str, help="Output path")
parser.add_argument('-f', '--filename', default='IMG_', type=str, help="Name of image files")
parser.add_argument('-n', '--panelId', default=0, type=int, help="File sequence number of the panels")
parser.add_argument('-s', '--first', default=1, type=int, help="File sequence number of the first image")
parser.add_argument('-e', '--last', default=100, type=int, help="File sequence number of the last image")
parser.add_argument('-a', '--albedo', type=float, nargs='+', help="List of panel albedos")
args=parser.parse_args()

def decdeg2dms(dd):
   is_positive = dd >= 0
   dd = abs(dd)
   minutes,seconds = divmod(dd*3600,60)
   degrees,minutes = divmod(minutes,60)
   degrees = degrees if is_positive else -degrees
   return (degrees,minutes,seconds)

imagePath = os.path.join(args.project,args.images)
panelPath = os.path.join(args.project,args.panels)
outputPath = os.path.join(args.project,args.output)

prefix=args.filename
panel_id=args.panelId
panelBasename=f'{prefix}{panel_id:04n}_'
first_image=args.first
last_image=args.last

# Read panels
print(f'Loading panels: {panelBasename}*.tif ')
panelNames = glob.glob(os.path.join(panelPath, f'{panelBasename}*.tif'))
panelCap = capture.Capture.from_filelist(panelNames)
if args.albedo is not None:
    panel_reflectance_by_band = args.albedo
else:
    panel_reflectance_by_band = panelCap.panel_albedo()
print(f'Panel albedos:') 
for i in panel_reflectance_by_band:
    print(f'{i:.4f} ', end='')
panel_irradiance = panelCap.panel_irradiance(panel_reflectance_by_band)  

print('\nCalibrating images:')
c=0
for i in range(first_image,last_image):
    imageBasename=f'{prefix}{i:04n}'
    if os.path.isfile(os.path.join(imagePath,f'{imageBasename}_1.tif')):
        print(f'{i} ', end='', flush=True)

        imageNames = glob.glob(os.path.join(imagePath,f'{imageBasename}_*.tif'))
        imageCap = capture.Capture.from_filelist(imageNames)
        dls_irradiances=imageCap.dls_irradiance()

        dls_correction = np.array(panel_irradiance)/dls_irradiances
        imageCap.compute_undistorted_reflectance(dls_irradiances*dls_correction)

        lat,lon,alt = imageCap.location()
        latdeg, latmin, latsec = decdeg2dms(lat)
        londeg, lonmin, lonsec = decdeg2dms(lon)
        latdir = 'North'
        if latdeg < 0:
            latdeg = -latdeg
            latdir = 'South'
        londir = 'East'
        if londeg < 0:
            londeg = -londeg
            londir = 'West'
        resolution = imageCap.images[0].focal_plane_resolution_px_per_mm

        for i in range(1,imageCap.num_bands+1):
            outputImageFilename = os.path.join(outputPath, f'c{imageBasename}_{i}.tif')
            cmd  = f'exiftool -config {args.config} -q '
            cmd += f'-XMP-camera:BandName="{imageCap.band_names()[i-1]}" '
            cmd += f'-GPSDateStamp={imageCap.utc_time().strftime("%Y:%m:%d")} '
            cmd += f'-GPSTimeStamp={imageCap.utc_time().strftime("%H:%M:%S")} '
            cmd += f'-GPSLatitude="{int(latdeg):d} deg {int(latmin):d} {latsec:.2f} {latdir[0]}" '
            cmd += f'-GpsLatitudeRef={latdir} '
            cmd += f'-GPSLongitude="{int(londeg):d} deg {int(lonmin):d} {lonsec:.2f} {londir[0]}" '
            cmd += f'-GPSLongitudeRef={londir} '
            cmd += f'-GPSAltitude="{alt:.1f} m Above Sea Level" '
            cmd += f'-GPSAltitudeRef="Above Sea Level" '
            cmd += f'-FocalLength={imageCap.images[0].focal_length} '
            cmd += f'-XResolution={resolution[0]} -YResolution={resolution[1]} -ResolutionUnit=cm '
            cmd += f'{outputImageFilename}'
            cv2.imwrite(outputImageFilename, imageCap.images[i-1].undistorted_reflectance().astype('float32'))
            subprocess.run(cmd, shell=True)
            imageCap.clear_image_data()
            c+=1
print(f'\nFinished processing {c} files')
