from maskCanvas import Canvas, Polyline, Mask, Point, Arc, Graph, Regular_polygone
from maskCanvas import Pen, draw_linear_background, AxidrawInterface, ObjFile
from maskCanvas import dot_object, put_polylines_on_object, GridifiedObj
from math import cos, sin, pi, atan
import math
import numpy as np
import random

def main():
    #size of a3
    c= Canvas(200,100,0,frame=False, paper_color= (255,255,255))

    pen1 = Pen((0,0,0),0.2)
    pen2 = Pen((0,0,200), 0.2)
    x_from = 14
    x_to = 14 + 60
    y_from = 12
    y_to = 12+40

    head = ObjFile("./obj/valentini_torso.obj")

    head.rotate(2, pi+pi/2)
    head.scale(0, 30)
    head.scale(1, 30)
    head.scale(2, 30)
    head.move(0, 23)
    head.move(1, 30)
    #head.slice(0, 10)
    #head.show()

    grid_head = GridifiedObj(head, 0.1)
    #grid_head.show()
    #exit()
    polylines = []
    for x in np.arange(head.range[0][0], head.range[0][1], 0.3):
        polylines.append(Polyline([Point(x, head.range[1][0]), Point(x, head.range[1][1])], pen1))

    polylines1 = put_polylines_on_object(polylines, grid_head, mask=True)

    
    offset = 3
    head.move(1, offset)
    head.scale(2, 0.5)
    grid_head = GridifiedObj(head, 0.1)
    polylines = []
    for y in np.arange(head.range[1][0], head.range[1][1], 0.5):
        polylines.append(Polyline([Point(head.range[0][0], y), Point(head.range[0][1], y)], pen2))

    polylines = put_polylines_on_object(polylines, grid_head, mask=True)

    for i, polyline in enumerate(polylines):
        polyline.rotate(0, -pi/10)
        polyline.rotate(1, -pi/10)
        c.draw_polyline(polyline)

    for i, polyline in enumerate(polylines1):
        polyline.rotate(0, -pi/10)
        polyline.rotate(1, -pi/10)
        c.draw_polyline(polyline)
    
    c.show_bitmap(50)
    #ai = AxidrawInterface(c)

if __name__ == "__main__":
    main()
