import os, glob, cv2, subprocess, argparse
import numpy as np
import micasense.capture as capture

parser = argparse.ArgumentParser(
    prog='undistort',
    description='Converts raw images to reflectance using DLS and Panels',  
    formatter_class=argparse.ArgumentDefaultsHelpFormatter  
)
parser.add_argument('-d', default='data', type=str, help="Path to project")
parser.add_argument('-i', default='raw_images', type=str, help="Path to images")
parser.add_argument('-p', default='panels', type=str, help="Path to panel images")
parser.add_argument('-t', default='images', type=str, help="Output path")
parser.add_argument('-m', default='images', type=str, help="Path to CSV metadata file")
parser.add_argument('-o', default='log.csv', type=str, help="Name of CSV file")
parser.add_argument('-f', default='IMG_', type=str, help="Name of image files")
parser.add_argument('-n', default=0, type=int, help="File sequence number of the panels")
parser.add_argument('-s', default=1, type=int, help="File sequence number of the first image")
parser.add_argument('-e', default=100, type=int, help="File sequence number of the last image")
args=parser.parse_args()

def decdeg2dms(dd):
   is_positive = dd >= 0
   dd = abs(dd)
   minutes,seconds = divmod(dd*3600,60)
   degrees,minutes = divmod(minutes,60)
   degrees = degrees if is_positive else -degrees
   return (degrees,minutes,seconds)

header = "SourceFile,\
GPSDateStamp,GPSTimeStamp,\
GPSLatitude,GpsLatitudeRef,\
GPSLongitude,GPSLongitudeRef,\
GPSAltitude,GPSAltitudeRef,\
FocalLength,\
XResolution,YResolution,ResolutionUnits\n"

imagePath = os.path.join(args.d,args.i)
panelPath = os.path.join(args.d,args.p)
outputPath = os.path.join(args.d,args.t)
csvPath =  os.path.join(args.d,args.m)
csvName = os.path.join(csvPath, args.o)

prefix=args.f
panel_id=args.n
panelBasename=f'{prefix}{panel_id:04n}_'
first_image=args.s
last_image=args.e

# Write metadata header
csvfile = open(csvName, 'w')
csvfile.writelines(header)

# Read panels
print(f'Loading panels: {panelBasename}*.tif ')
panelNames = glob.glob(os.path.join(panelPath, f'{panelBasename}*.tif'))
panelCap = capture.Capture.from_filelist(panelNames)
panel_reflectance_by_band = panelCap.panel_albedo()
panel_irradiance = panelCap.panel_irradiance(panel_reflectance_by_band)  

print('Undistorting captures:')
for i in range(first_image,last_image):
    imageBasename=f'{prefix}{i:04n}'
    if os.path.isfile(os.path.join(imagePath,f'{imageBasename}_1.tif')):
        print(f'{i} ', end='', flush=True)

        imageNames = glob.glob(os.path.join(imagePath,f'{imageBasename}_*.tif'))
        imageCap = capture.Capture.from_filelist(imageNames)
        dls_irradiances=imageCap.dls_irradiance()

        dls_correction = np.array(panel_irradiance)/dls_irradiances
        imageCap.compute_undistorted_reflectance(dls_irradiances*dls_correction)

        #get lat,lon,alt,time
        lat,lon,alt = imageCap.location()
        #write to csv in format:
        # IMG_0199_1.tif,"33 deg 32' 9.73"" N","111 deg 51' 1.41"" W",526 m Above Sea Level
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
            linestr = '"{}",'.format(outputImageFilename)
            linestr += imageCap.utc_time().strftime("%Y:%m:%d,%H:%M:%S,")
            linestr += '"{:d} deg {:d}\' {:.2f}"" {}",{},'.format(int(latdeg),int(latmin),latsec,latdir[0],latdir)
            linestr += '"{:d} deg {:d}\' {:.2f}"" {}",{},{:.1f} m Above Sea Level,Above Sea Level,'.format(int(londeg),int(lonmin),lonsec,londir[0],londir,alt)
            linestr += '{}'.format(imageCap.images[0].focal_length)
            linestr += '{},{},mm'.format(resolution,resolution)
            linestr += '\n' # when writing in text mode, the write command will convert to os.linesep

            csvfile.writelines(linestr)
            cv2.imwrite(outputImageFilename, imageCap.images[i-1].undistorted_reflectance())
            imageCap.clear_image_data()

csvfile.close()

#Inject metadata from CSV
print("\nUpdating metadata ..")
cmd=f'exiftool -csv={csvName} -overwrite_original {outputPath}'
subprocess.run(cmd, shell=True)

