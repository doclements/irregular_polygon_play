irregular_polygon_play
======================

does what it says on the tin

~~playing with cmd_line~~
 * ~~gdal_rasterize  -burn 1 -of netcdf -ts 300 300 buffer.geojson poly_raster.nc~~
 
Scrapped the idea of booting out to a subprocess. Found a mechanism using PIL to produce a raster from my polygon. this is then read into a numpy array and used as a mask for creating the final masked array.
