import sys
import matplotlib.pyplot as plt
from osgeo import gdal

f=plt.figure()
dataset = gdal.Open(sys.argv[1], gdal.GA_ReadOnly)

band=[]

b1 = dataset.GetRasterBand(1)
arr = b1.ReadAsArray()
band.append(arr)

b2 = dataset.GetRasterBand(2)
arr = b2.ReadAsArray()
band.append(arr)

b3 = dataset.GetRasterBand(3)
arr = b3.ReadAsArray()
band.append(arr)

b4 = dataset.GetRasterBand(4)
arr = b4.ReadAsArray()
band.append(arr)

b5 = dataset.GetRasterBand(5)
arr = b4.ReadAsArray()
band.append(arr)

b6 = dataset.GetRasterBand(6)
arr = b4.ReadAsArray()
band.append(arr)

b7 = dataset.GetRasterBand(7)
arr = b4.ReadAsArray()
band.append(arr)

b8 = dataset.GetRasterBand(8)
arr = b4.ReadAsArray()
band.append(arr)

b9 = dataset.GetRasterBand(9)
arr = b4.ReadAsArray()
band.append(arr)

b10 = dataset.GetRasterBand(10)
arr = b4.ReadAsArray()
band.append(arr)

f, axarr = plt.subplots(3,3)

axarr[0][0].imshow(band[0])
axarr[0][1].imshow(band[1])
axarr[0][2].imshow(band[2])
axarr[1][0].imshow(band[3])      
axarr[1][1].imshow(band[4])
axarr[1][2].imshow(band[5])
axarr[2][0].imshow(band[6])   
axarr[2][1].imshow(band[7])
axarr[2][2].imshow(band[8])

plt.tight_layout()

plt.show()
