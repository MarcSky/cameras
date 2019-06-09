from random import choice

import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
from shapely.geometry import LineString, Point, Polygon

from server.camera_utils import Building, Camera

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


image = Image.new("RGB", size=(1200, 1000), color=(255,255,255,0))

draw = ImageDraw.Draw(image)

# print(tuple(zip(WORLD[:-1], WORLD[1:])) + ((WORLD[0], WORLD[-1])))
for start, end in tuple(zip(WORLD[:-1], WORLD[1:])):
    draw.line(start + end, fill=128, width=3)

cameras = []

# c = Camera(Point(400, 400), LineString([(0, 0), (1, 1)]))
# c.refresh_polygon()
# cameras.append(c)
#
# c = Camera(Point(500, 350), LineString([(0, 0), (1, -1)]))
# c.refresh_polygon()
# cameras.append(c)
#
# c = Camera(Point(300, 300), LineString([(0, 0), (-1, 0)]))
# c.refresh_polygon()
# cameras.append(c)
#
# c = Camera(Point(700, 200), LineString([(0, 0), (1, -1)]))
# c.refresh_polygon()
# cameras.append(c)
#
# c = Camera(Point(500, 600), LineString([(0, 0), (1, 1)]))
# c.refresh_polygon()
# cameras.append(c)
#
# c = Camera(Point(800, 600), LineString([(0, 0), (-3, -1)]))
# c.refresh_polygon()
# cameras.append(c)


buildings = []
for points in DATA:
    building = Building(Polygon(points))
    building.refresh()
    buildings.append(building)
    draw.polygon(points, fill=200)
    for p in building.allowed_wall_points:
        draw.ellipse([(p.x - 5, p.y - 5), (p.x + 5, p.y + 5)], fill=256, width=3)
        cameras.extend(building.get_allowed_cameras(p))
        # c = Camera(p, building.get_forward_wall_camera_direction(p))
        # c.refresh_polygon()
        # cameras.append(c)

# b = choice(buildings)
# p = choice(b.allowed_wall_points)
# cameras.extend(b.get_allowed_cameras(p))

for c in cameras:
    for b in buildings:
        c.screen_building(b.polygon)

for c in cameras:
    # p = c.point
    # draw.ellipse([(p.x - 10, p.y - 10), (p.x + 10, p.y + 10)], fill=512, width=3)
    # print((c.point.x, c.point.y))
    # print(list(c.center.coords))
    # print(list(c.direction.coords))
    # draw.line(list(c.center.coords), fill=100)
    draw.polygon(c.polygon.exterior.coords, outline=1)

image.show()
