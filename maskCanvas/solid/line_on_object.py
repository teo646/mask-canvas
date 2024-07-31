import random
from maskCanvas import Point, Polyline
from math import cos
import numpy as np
#this function will draw lines on the object and rotate the lines to
def line_on_object(canvas, obj, line_distance, degree, pen):
    for i,x in enumerate(np.arange(0, canvas.x/cos(degree), line_distance)):
        points = []
        for y in np.arange(0, canvas.y, 1):
            z = obj.get_z(x, y)
            points.append(Point(x, y, z))
        polyline = Polyline(points, pen)
        polyline.rotate(1, degree)
        canvas.draw_polyline(polyline)

