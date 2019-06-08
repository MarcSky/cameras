import shapefile

sf = shapefile.Reader("data/buildings/buildings.shp")
# sf = shapefile.Reader("data/ntopoly/ntopoly.shp")
shapes = sf.shapes()
for i in range(len(shapes)):
    print(type(shapes[i]))
    print(shapes[i].shapeType)
    print(shapes[i].parts)
    print(shapes[i].points)
    print(type(shapes[i].points))

