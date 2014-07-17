import irregular_polygon as ip
import unittest
import shapely
from shapely import wkt


class irregularTest(unittest.TestCase):

   def setUp(self):
      print 'setting up tests'
      self.wcs_url =  'https://vortices.npm.ac.uk/thredds/wcs/CCI_ALL-v1.0-MONTHLY?crs=OGC:CRS84&service=WCS&format=NetCDF3&request=GetCoverage&version=1.0.0&bbox=-22.8515625,41.572265625,-8.96484375,54.580078125&coverage=chlor_a&time=2007-07-01/2007-08-01'
      self.wcs_base_url = '''https://vortices.npm.ac.uk/thredds/wcs/CCI_ALL-v1.0-MONTHLY?crs=OGC:CRS84&service=WCS&format=NetCDF3&request=GetCoverage&version=1.0.0&bbox=%s,%s,%s,%s&coverage=chlor_a&time=2007-07-01/2007-08-01'''
      self.wkt_poly = '''POLYGON((-29.35546875 60.369873046875, -33.57421875 56.678466796875, -34.1015625 55.096435546875, -30.76171875 52.108154296875, -27.94921875 48.416748046875, -28.125 45.428466796875, -29.1796875 41.385498046875, -31.46484375 38.748779296875, -34.8046875 36.287841796875, -7.20703125 36.463623046875, -9.66796875 37.869873046875, -10.37109375 39.627685546875, -9.140625 41.561279296875, -10.1953125 43.494873046875, -8.7890625 44.725341796875, -5.9765625 44.373779296875, -1.93359375 44.197998046875, -2.4609375 46.834716796875, -4.39453125 48.240966796875, -5.44921875 49.119873046875, -2.28515625 49.998779296875, -5.625 50.701904296875, -5.80078125 51.932373046875, -9.31640625 51.405029296875, -10.8984375 52.283935546875, -11.07421875 53.514404296875, -10.546875 55.272216796875, -9.31640625 55.623779296875, -7.734375 56.151123046875, -7.3828125 57.381591796875, -7.734375 59.315185546875, -7.20703125 60.369873046875, -29.35546875 60.369873046875))'''
      self.wkt_poly2 = 'POLYGON((-15.380859375 51.976318359375, -14.501953125 50.262451171875, -12.83203125 50.833740234375, -12.12890625 52.064208984375, -10.9423828125 50.174560546875, -11.9091796875 49.339599609375, -9.052734375 47.098388671875, -5.4052734375 46.263427734375, -5.537109375 43.978271484375, -9.4921875 44.154052734375, -15.732421875 45.340576171875, -16.34765625 48.021240234375, -15.380859375 51.976318359375))'
      self.wkt_line = 'LINESTRING(-4.21875 50.174560546875, -6.15234375 46.307373046875, -9.4921875 45.252685546875, -11.77734375 40.858154296875, -11.953125 35.584716796875, -14.58984375 29.783935546875, -19.3359375 24.686279296875, -18.28125 17.655029296875, -22.32421875 10.623779296875, -23.90625 3.592529296875, -26.015625 -5.899658203125, -30.234375 -13.282470703125, -36.2109375 -28.399658203125, -39.7265625 -38.243408203125, -39.7265625 -42.813720703125)'
      self.envelope = None
      self.loaded_poly = None
  

   def tearDown(self):
      pass

   def test_wcs_url(self):
      self.assertEquals(ip.get_wcs(self.wcs_base_url), self.wcs_url)
      pass

   def test_file_fetch(self):
      pass

   def test_netcdf_bounds(self):
      pass

   def test_poly_parse(self):
      self.loaded_poly = wkt.loads(self.wkt_poly)
      self.assertEqual(type(self. loaded_poly),shapely.geometry.polygon.Polygon)

   def test_poly_envelope(self):
      loaded_poly = wkt.loads(self.wkt_poly)
      envelope = loaded_poly.envelope
      self.assertEqual(type(envelope),shapely.geometry.polygon.Polygon)

   def test_3line_parse(self):
      loaded_line = wkt.loads(self.wkt_line)
      self.assertEqual(type(loaded_line) ,shapely.geometry.linestring.LineString)
      

   def test_line_envelope(self):
      pass

   def test_mask(self):
      pass

   def test_avg_with_mask(self):
      pass






if __name__ == '__main__':
    unittest.main()