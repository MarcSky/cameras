import shapefile

file = "data/green/green.shp"
# sf = shapefile.Reader("data/green/green.shp")
# sf = shapefile.Reader("data/ntopoly/ntopoly.shp")
# shapes = sf.shapes()
# print(len(shapes))
# for i in range(len(shapes)):
#     print(type(shapes[i]))
#     print(shapes[i].shapeType)
#     print(shapes[i].parts)
#     print(shapes[i].points)
#     print(type(shapes[i].points))


from osgeo import ogr
file = ogr.Open(file)
shape = file.GetLayer(0)
#first feature of the shapefile
feature = shape.GetFeature(0)

# first = feature.ExportToJson()
print (feature) # (GeoJSON format)
# {"geometry": {"type": "LineString", "coordinates": [[0.0, 0.0], [25.0, 10.0], [50.0, 50.0]]}, "type": "Feature", "properties": {"FID": 0.0}, "id": 0}
