import os, glob
import micasense.capture as capture

imagePath = "../images"
imageNames = glob.glob(os.path.join(imagePath,'IMG_0001_*.tif'))

capture = capture.Capture.from_filelist(imageNames)
