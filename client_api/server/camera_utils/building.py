from shapely.geometry import LineString, Point
from shapely.affinity import rotate

from .consts import WALL_CAMERA_DISTANCE, ALLOWED_DISTANCE_ERROR
from .utils import scale_line_length


class Building:
    def __init__(self, building_polygon):
        self.polygon = building_polygon
        # Points where cameras are allowed to be placed.
        self.allowed_wall_points = []
        self.wall2points = {}
        self.point2wall = {}

    @staticmethod
    def calculate_wall_points(wall):
        if wall.length - WALL_CAMERA_DISTANCE < ALLOWED_DISTANCE_ERROR:
            # Get middle of the wall.
            return [wall.interpolate(0.5, normalized=True)]

        points_count = int(wall.length // WALL_CAMERA_DISTANCE)
        return [wall.interpolate((i / points_count), normalized=True) for i in range(1, points_count)]

    def refresh(self):
        self.refresh_allowed_points()

    def refresh_allowed_points(self):
        self.allowed_wall_points = []
        self.wall2points = {}
        self.point2wall = {}
        points = self.polygon.exterior.coords
        for wall in zip(points[:-1], points[1:]):
            pts = self.calculate_wall_points(LineString(tuple(wall)))
            self.wall2points[tuple(wall)] = pts
            for pt in pts:
                self.point2wall[(pt.x, pt.y)] = wall
            self.allowed_wall_points.extend(pts)

    def get_forward_wall_camera_direction(self, point):
        wall = self.point2wall[(point.x, point.y)]
        vector0 = scale_line_length(LineString([(point.x, point.y), wall[0]]), ALLOWED_DISTANCE_ERROR)
        vector1 = scale_line_length(LineString([(point.x, point.y), wall[1]]), ALLOWED_DISTANCE_ERROR)
        for v in (vector0, vector1):
            u = rotate(v, 90, origin=point, use_radians=False)
            if not self.polygon.contains(Point(u.coords[1])):
                p1, p2 = u.coords
                return Point(p2[0] - p1[0], p2[1] - p1[1])
