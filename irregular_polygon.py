from shapely import wkt

wcs_base_url = '''https://vortices.npm.ac.uk/thredds/wcs/CCI_ALL-v1.0-MONTHLY?crs=OGC:CRS84&service=WCS&format=NetCDF3&request=GetCoverage&version=1.0.0&bbox=%s,%s,%s,%s&coverage=chlor_a&time=2007-07-01/2007-08-01'''

wkt_poly = '''POLYGON((-29.35546875 60.369873046875, -33.57421875 56.678466796875, -34.1015625 55.096435546875, -30.76171875 52.108154296875, -27.94921875 48.416748046875, -28.125 45.428466796875, -29.1796875 41.385498046875, -31.46484375 38.748779296875, -34.8046875 36.287841796875, -7.20703125 36.463623046875, -9.66796875 37.869873046875, -10.37109375 39.627685546875, -9.140625 41.561279296875, -10.1953125 43.494873046875, -8.7890625 44.725341796875, -5.9765625 44.373779296875, -1.93359375 44.197998046875, -2.4609375 46.834716796875, -4.39453125 48.240966796875, -5.44921875 49.119873046875, -2.28515625 49.998779296875, -5.625 50.701904296875, -5.80078125 51.932373046875, -9.31640625 51.405029296875, -10.8984375 52.283935546875, -11.07421875 53.514404296875, -10.546875 55.272216796875, -9.31640625 55.623779296875, -7.734375 56.151123046875, -7.3828125 57.381591796875, -7.734375 59.315185546875, -7.20703125 60.369873046875, -29.35546875 60.369873046875))'''

wkt_poly2 = 'POLYGON((-15.380859375 51.976318359375, -14.501953125 50.262451171875, -12.83203125 50.833740234375, -12.12890625 52.064208984375, -10.9423828125 50.174560546875, -11.9091796875 49.339599609375, -9.052734375 47.098388671875, -5.4052734375 46.263427734375, -5.537109375 43.978271484375, -9.4921875 44.154052734375, -15.732421875 45.340576171875, -16.34765625 48.021240234375, -15.380859375 51.976318359375))'

wkt_line = 'LINESTRING(-4.21875 50.174560546875, -6.15234375 46.307373046875, -9.4921875 45.252685546875, -11.77734375 40.858154296875, -11.953125 35.584716796875, -14.58984375 29.783935546875, -19.3359375 24.686279296875, -18.28125 17.655029296875, -22.32421875 10.623779296875, -23.90625 3.592529296875, -26.015625 -5.899658203125, -30.234375 -13.282470703125, -36.2109375 -28.399658203125, -39.7265625 -38.243408203125, -39.7265625 -42.813720703125)'


def create_wcs_url(bounds):
   return wcs_base_url % (bounds[0],bounds[1],bounds[2],bounds[3])




loaded_poly = wkt.loads(wkt_line)

from shapely.geometry import mapping
import json
open("buffer.geojson", "wb").write(json.dumps(mapping(loaded_poly)))

wcs_envelope = loaded_poly.envelope

print wcs_envelope
bounds =  wcs_envelope.bounds

wcs_url = wcs_base_url % (bounds[0],bounds[1],bounds[2],bounds[3])

print wcs_url

import urllib

testfile=urllib.URLopener()
testfile.retrieve(wcs_url,"chlor.nc")

import netCDF4

regular = netCDF4.Dataset('./chlor.nc', 'r')
for v in regular.variables:
   print v
   print regular.variables[v]

for d in regular.dimensions:
   print d
   print regular.dimensions[d]

import numpy as np

chl = regular.variables['chlor_a'][:]
#print chl[:]

lat_pt, lon_pt = -33.57421875, 56.678466796875

latvals = regular.variables['lat'][:]
lonvals = regular.variables['lon'][:]


poly = wkt_line[11:-1]
poly = poly.split(',')
poly = [x.split() for x in poly]


print poly
from PIL import Image, ImageDraw

def find_closest(arr, val):
   """
  Finds the position in the array where the array value matches
  the value specified by the user
  """
   current_closest = 120310231023
   current_idx = None
   for i in range(len(arr)):
      if abs(arr[i]-val)<current_closest:
         current_closest = abs(arr[i]-val)
         current_idx=i
   return current_idx

found_lats = [find_closest(latvals, float(x[1])) for x in poly]
found_lons = [find_closest(lonvals, float(x[0])) for x in poly]

found = zip(found_lons,found_lats)
print found
print chl[:,found_lats,found_lons]

img = Image.new('L', (chl.shape[2],chl.shape[1]), 0)


ImageDraw.Draw(img).line(found,  fill=255)

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

masker = np.array(img)

print masker.shape
print chl.shape
masked_chl = np.ma.masked_array(chl[0,:], [x != 255 for x in masker])
#plt.imshow(chl[0,:])
#plt.show()
plt.imshow(masked_chl)
plt.show()
#plt.savefig('masked_chl2.png')

print masker