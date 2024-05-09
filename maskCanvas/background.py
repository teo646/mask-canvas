import random
from .polyline import Polyline
from .components import Point
from math import sin, cos, pi, atan2

def draw_linear_background(canvas, pen, line_number, max_cut):
    canvas_center = Point(canvas.x/2, canvas.y/2)
    criteria_angle = atan2(canvas.y, canvas.x)
    for index in range(line_number):
        angle = random.random()*2*pi # 0~2*pi
        if((angle>criteria_angle and angle < pi-criteria_angle) or \
                (angle>pi+criteria_angle and angle < 2*pi-criteria_angle)):
            max_length = canvas.y/2/abs(sin(angle))
        else:
            max_length = canvas.x/2/abs(cos(angle))

        cut = random.random()*max_cut
        length = max_length-cut
        canvas.draw_polyline(Polyline([canvas_center, Point(canvas.x/2+length*cos(angle),\
                canvas.y/2+length*sin(angle))], pen))

    return canvas

