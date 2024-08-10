from maskCanvas import Canvas, Polyline, Mask, Point, Arc, Graph, Regular_polygone
from maskCanvas import Pen, draw_linear_background, AxidrawInterface, ObjFile
from maskCanvas import dot_object, put_polylines_on_object
from math import cos, sin, pi, atan
import math
import numpy as np
import random

def main():
    #size of a3
    c= Canvas(100,80,0,frame=False, paper_color= (255,255,255))

    pen1 = Pen((0,0,0),0.2)
    pen2 = Pen((0,0,200), 0.2)

    head = ObjFile("./obj/vietnam_head.obj")

    head.rotate(2, 1.45)
    head.rotate(1, -0.3)
    head.rotate(0, 0.6)
    head.squeeze(0, 14, 82)
    head.squeeze(1, 12, 64)
    head.squeeze(2, -50, 50)
    head.slice(2, 0)

    head.setup(interval = 0.3)
    polylines = []
    for x in np.arange(14, 82, 0.3):
        polylines.append(Polyline([Point(x, 12), Point(x, 64)], pen1))

    polylines = put_polylines_on_object(polylines, head, mask=True)

    for i, polyline in enumerate(polylines):
        polyline.rotate(0, pi/12)
        polyline.rotate(1, pi/12)
        c.draw_polyline(polyline)

    offset =0 
    head.move(1, offset)
    head.squeeze(2, 0, 50)
    head.setup(interval = 0.3)
    polylines = []
    for y in np.arange(12+offset, 64+offset, 0.5):
        polylines.append(Polyline([Point(14, y), Point(82, y)], pen1))

    polylines = put_polylines_on_object(polylines, head, mask=True)

    for i, polyline in enumerate(polylines):
        polyline.rotate(0, pi/12)
        polyline.rotate(1, pi/12)
        c.draw_polyline(polyline)

    c.show_bitmap(50)
    ai = AxidrawInterface(c)

if __name__ == "__main__":
    main()
