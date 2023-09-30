import sys
import matplotlib.pyplot as plt
from osgeo import gdal

band=int(sys.argv[2])
dataset = gdal.Open(sys.argv[1], gdal.GA_ReadOnly)

b1 = dataset.GetRasterBand(band)
arr = b1.ReadAsArray()

plt.imshow(arr)
plt.show()
