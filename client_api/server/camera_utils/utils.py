import numpy as np
from numpy import arccos, clip, dot
from numpy.linalg import norm
from shapely.affinity import scale


def calculate_angle(v, u):
    v = scale_line_length(v, 1.)
    u = scale_line_length(u, 1.)
    cos = dot(u, v) / norm(v) / norm(u)  # -> cosine of the angle
    return np.degrees(arccos(clip(cos, -1, 1)))


def scale_line_length(u, target_length):
    length = u.length
    return scale(u, target_length / length, target_length / length, origin=u.coords[0])
