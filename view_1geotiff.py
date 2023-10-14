import sys
import matplotlib.pyplot as plt
from osgeo import gdal
import numpy as np

band=int(sys.argv[2])
dataset = gdal.Open(sys.argv[1], gdal.GA_ReadOnly)

b1 = dataset.GetRasterBand(band)
arr = b1.ReadAsArray()
arr[np.where(arr<0)]=0
#arr[np.where(arr>0.4)]=0.0

plt.imshow(arr)
plt.colorbar()
plt.show()
