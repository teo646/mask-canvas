import random
from maskCanvas import Point, Polyline, Mask
from math import cos, pi
import numpy as np
from copy import deepcopy
from tqdm import tqdm

def put_polylines_on_object(polylines, obj, mask=False):
    polylines_on_object = []
    for polyline in polylines:
        polylines_on_object += put_polyline_on_object(polyline, obj)

    return polylines_on_object

def put_polyline_on_object(polyline, obj):
    polyline_paths = []
    polyline_path = []
    for p1, p2 in zip(polyline.path, polyline.path[1:]):
        vector = p2.coordinate[:2] - p1.coordinate[:2]
        normal_vector = vector/np.linalg.norm(vector)
        for length in np.arange(0, np.linalg.norm(vector), 0.3):
            coordinate = p1.coordinate[:2] + normal_vector*length
            z = obj.get_z(coordinate[0], coordinate[1])
            if(z):
                polyline_path.append(Point(coordinate[0], coordinate[1], z))
            else:
                 if(not len(polyline_path) == 0):
                    polyline_paths.append(polyline_path)
                    polyline_path = []

    if(not len(polyline_path) == 0):
        polyline_paths.append(polyline_path)

    polylines = []
    for polyline_path in polyline_paths:
        polylines.append(Polyline(polyline_path, polyline.pen))

    return polylines
