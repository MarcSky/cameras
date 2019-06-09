from shapely.geometry import LineString

from .consts import WALL_CAMERA_DISTANCE, ALLOWED_DISTANCE_ERROR


class Building:
    def __init__(self, building_polygon):
        self.polygon = building_polygon
        # Points where cameras are allowed to be placed.
        self.allowed_wall_points = []

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
        points = self.polygon.exterior.coords
        for wall in zip(points[:-1], points[1:]):
            self.allowed_wall_points.extend(self.calculate_wall_points(LineString(tuple(wall))))
