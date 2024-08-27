import random
from maskCanvas import Point, Polyline
from math import cos, pi
import numpy as np
from tqdm import tqdm

class MarchingSquares(Polyline):

    def __init__(self):
        self.line_segments = []

    def add_square(self, line_segment):
        self.line_segments.append(line_segment)

    def march(self):
        pass

def put_contours_on_object(obj, values):
    contours = []
    for value in tqdm(values):
        contours.append(put_countour_on_object(obj, value))
    return contours

def put_contour_on_object(obj, value):
    marching_squares = MarchingSquares()
    x_length = len(obj.grid)
    y_length = len(obj.grid[0])
    for x_index in range(x_length-1):
        for y_index in range(y_length-1):



