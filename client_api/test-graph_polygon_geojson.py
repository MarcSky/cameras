import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
from shapely.geometry import LineString, Point, Polygon

from server.camera_utils.camera import Camera

WORLD = (
    (50, 50),
    (50, 950),
    (950, 950),
    (950, 50),

)
DATA = [
    (
        (100, 100),
        (100, 800),
        (200, 800),
        (200, 100),
    ),
    (
        (800, 100),
        (800, 800),
        (900, 800),
        (900, 100),
    ),
    (
        (500, 100),
        (500, 300),
        (600, 300),
        (600, 100),
    ),
    (
        (500, 700),
        (500, 800),
        (600, 800),
        (600, 700),
    ),
    (
        (500, 400),
        (500, 500),
        (600, 500),
        (600, 400),
    ),
]

# image = Image.new("RGB", size=(1200, 1000), color=(255,255,255,0))
#
# draw = ImageDraw.Draw(image)
#
# for start, end in tuple(zip(WORLD[:-1], WORLD[1:])):
#     draw.line(start + end, fill=128, width=3)

cameras = []

c = Camera(Point(1000, 400), LineString([(0, 0), (1, 1)]))
c.refresh_polygon()
cameras.append(c)

c = Camera(Point(800, 600), LineString([(0, 0), (-3, -1)]))
c.refresh_polygon()
cameras.append(c)

for points in DATA:
    for c in cameras:
        c.screen_building(Polygon(points))

polygons = []
for c in cameras:
    polygons.append(c.polygon)


def getGeoJson(polygons):
    return {"type": "FeatureCollection", "features": polygons}


def getGeoJsonPolygon(coordinates):
    return {"type": "Feature", "properties": {}, "geometry": {
        "type": "Polygon", "coordinates": coordinates}}


def polygonsToGeoJson(polygons):
    geoJsonPolygons = []
    for polygon in polygons:
        coordinates = []
        for point in polygon.exterior.coords:
            coordinates.append([point[0], point[1]])
        geoJsonPolygons.append(getGeoJsonPolygon(coordinates))
    return geoJsonPolygons


print(getGeoJson(polygonsToGeoJson(polygons)))