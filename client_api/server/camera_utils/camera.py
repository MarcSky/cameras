from functools import reduce
from itertools import combinations

import numpy as np
from shapely.affinity import rotate, scale, translate
from shapely.geometry import LineString, LinearRing, Point, Polygon

from .consts import ALLOWED_DISTANCE_ERROR, VIEWING_ANGLE, VIEWING_DISTANCE, VIEWING_POINTS


class Camera:
    def __init__(self, point, direction_vector):
        self.point = point
        direction = LineString([(0, 0), (direction_vector.x, direction_vector.y)])
        length = direction.length
        self.direction = scale(direction, 1 / length, 1 / length, origin=(0, 0))
        self.center = None
        self.polygon = None
        self.polyline = None

    @staticmethod
    def common_area(cameras):
        polygons = [c.polygon for c in cameras]
        multi_polygon = reduce(lambda x, y: x.union(y), polygons)
        return multi_polygon.area

    @staticmethod
    def intersection_area(cameras):
        polygons = [c.polygon.buffer(0.1) for c in cameras]
        area = 0.
        for p1, p2 in combinations(polygons, 2):
            if p1 == p2 or not p1.intersects(p2):
                continue
            p = p1.intersection(p2)
            area += p.area
        return area

    def __hash__(self):
        return hash(((self.point.x, self.point.y), self.direction.coords[1]))

    @property
    def area(self):
        if self.polygon is None:
            return 0.
        return self.polygon.area

    def refresh_polygon(self):
        self.center = scale(self.direction, VIEWING_DISTANCE, VIEWING_DISTANCE, origin=(0, 0))
        self.center = translate(self.center, self.point.x, self.point.y)
        points = [self.point.coords[0]]
        angles = np.linspace(-VIEWING_ANGLE / 2, VIEWING_ANGLE / 2, VIEWING_POINTS)
        for angle in angles:
            v = rotate(self.center, angle, origin=self.center.coords[0], use_radians=False)
            points.append(v.coords[1])
        self.polyline = LinearRing(points)
        self.polygon = Polygon(points)

    def screen_building(self, building):
        building_polyline = LinearRing(list(building.exterior.coords))
        points = [self.point.coords[0]]
        angles = np.linspace(-VIEWING_ANGLE / 2, VIEWING_ANGLE / 2, VIEWING_POINTS)
        is_sector_screened = False
        for angle in angles:
            v = rotate(self.center, angle, origin=self.center.coords[0], use_radians=False)
            intersection = building_polyline.intersection(v)
            if isinstance(intersection, Point):
                if intersection.distance(self.point) < ALLOWED_DISTANCE_ERROR:
                    # Camera is placed on this building.
                    points.append(v.coords[1])
                    continue
                points.append((intersection.x, intersection.y))
                is_sector_screened = True
            elif isinstance(intersection, LineString):
                lines = [LineString([(self.point.x, self.point.y), p]) for p in list(intersection.coords)]
                line = min(lines, key=lambda l: l.length)
                points.append(line.coords[1])
                is_sector_screened = True
            elif len(list(intersection)) > 1:
                pts = []
                for entity in intersection:
                    if isinstance(entity, Point):
                        pts.append(entity)
                    elif isinstance(entity, LineString):
                        for pt in entity.coords:
                            pts.append(Point(pt))
                    else:
                        continue
                lines = [LineString([(self.point.x, self.point.y), (p.x, p.y)]) for p in pts]
                line = min(lines, key=lambda l: l.length)
                points.append(line.coords[1])
                is_sector_screened = True
            else:
                points.append(v.coords[1])

        if not is_sector_screened:
            return

        self.polyline = LinearRing(points)
        self.polygon = Polygon(points)
