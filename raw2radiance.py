import micasense.metadata as metadata
import micasense.utils as msutils
import micasense.plotutils as plotutils
import cv2
import matplotlib.pyplot as plt

imageName="../images/IMG_0001_1.tif" 
# get image metadata
meta = metadata.Metadata(imageName)
imageRaw=cv2.imread(imageName, cv2.IMREAD_UNCHANGED)

cameraMake = meta.get_item('EXIF:Make')
cameraModel = meta.get_item('EXIF:Model')
firmwareVersion = meta.get_item('EXIF:Software')
bandName = meta.get_item('XMP:BandName')
print('{0} {1} firmware version: {2}'.format(cameraMake, 
                                             cameraModel, 
                                             firmwareVersion))
print('Exposure Time: {0} seconds'.format(meta.get_item('EXIF:ExposureTime')))
print('Imager Gain: {0}'.format(meta.get_item('EXIF:ISOSpeed')/100.0))
print('Size: {0}x{1} pixels'.format(meta.get_item('EXIF:ImageWidth'),meta.get_item('EXIF:ImageHeight')))
print('Band Name: {0}'.format(bandName))
print('Center Wavelength: {0} nm'.format(meta.get_item('XMP:CentralWavelength')))
print('Bandwidth: {0} nm'.format(meta.get_item('XMP:WavelengthFWHM')))
print('Capture ID: {0}'.format(meta.get_item('XMP:CaptureId')))
print('Flight ID: {0}'.format(meta.get_item('XMP:FlightId')))
print('Focal Length: {0}'.format(meta.get_item('XMP:FocalLength')))

radianceImage, L, V, R = msutils.raw_image_to_radiance(meta, imageRaw)
plotutils.plotwithcolorbar(V,'Vignette Factor');
plotutils.plotwithcolorbar(R,'Row Gradient Factor');
plotutils.plotwithcolorbar(V*R,'Combined Corrections');
plotutils.plotwithcolorbar(L,'Vignette and row gradient corrected raw values');
plotutils.plotwithcolorbar(radianceImage,'All factors applied and scaled to radiance');
