from shapely.geometry import LineString, Point
from shapely.affinity import rotate, scale

from .consts import WALL_CAMERA_DISTANCE, ALLOWED_DISTANCE_ERROR, VIEWING_ANGLE
from .utils import scale_line_length


class Building:
    def __init__(self, building_polygon):
        self.polygon = building_polygon
        # Points where cameras are allowed to be placed on walls.
        self.allowed_wall_points = []
        # Walls along with their points.
        self.wall2points = {}
        # Point along with its wall.
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

    def get_allowed_wall_cameras(self, point):
        from . import Camera
        try:
            direction = self.get_forward_wall_camera_direction(point)
        except:
            return []
        cameras = [Camera(point, direction)]
        turn_angle = int(90 - VIEWING_ANGLE / 2)
        v = LineString([(0, 0), (direction.x, direction.y)])
        for angle in (-turn_angle, turn_angle):
            u = rotate(v, angle, origin=(0, 0), use_radians=False)
            c = Camera(point, Point(u.coords[1]))
            cameras.append(c)
        return cameras

    def get_allowed_corner_cameras(self, point):
        from . import Camera
        try:
            direction = self.get_forward_corner_camera_direction(point)
        except:
            return []
        cameras = [Camera(point, direction)]
        return cameras

    def get_forward_wall_camera_direction(self, point):
        wall = self.point2wall[(point.x, point.y)]
        vector0 = scale_line_length(LineString([(point.x, point.y), wall[0]]), ALLOWED_DISTANCE_ERROR)
        vector1 = scale_line_length(LineString([(point.x, point.y), wall[1]]), ALLOWED_DISTANCE_ERROR)
        for v in (vector0, vector1):
            u = rotate(v, 90, origin=point, use_radians=False)
            if not self.polygon.contains(Point(u.coords[1])):
                p1, p2 = u.coords
                return Point(p2[0] - p1[0], p2[1] - p1[1])

        raise NotImplementedError

    def get_forward_corner_camera_direction(self, point):
        points = self.polygon.exterior.coords
        indexes = [
            index for index, p in enumerate(points[1:])
            if p == (point.x, point.y)
        ]
        if not indexes:
            return None

        index = indexes[0]
        p1, p2 = points[index - 1], points[index + 1]
        line1 = LineString([p1, points[index]])
        line2 = LineString([points[index], p2])
        line1 = scale_line_length(line1, line2.length)
        p1 = line1.coords[1]
        vector = LineString([p1, p2])
        vector = scale(vector, 0.5, 0.5, origin=p1)
        target = LineString([points[index], vector.coords[1]])
        target = rotate(target, 180, origin=target.coords[0], use_radians=False)
        target = scale_line_length(target, ALLOWED_DISTANCE_ERROR)
        p = target.coords[1]
        return Point(p[0] - points[index][0], p[1] - points[index][1])
