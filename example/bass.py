from maskCanvas import Canvas, Polyline, Mask, Point, Arc, Graph, Regular_polygone
from maskCanvas import Pen, draw_linear_background, AxidrawInterface, ObjFile
from maskCanvas import dot_object, put_polylines_on_object, GridifiedObj
from math import cos, sin, pi, atan
import math
import numpy as np
import random

def main():
    #size of a3
    c= Canvas(100,80,0,frame=False, paper_color= (255,255,255))

    pen1 = Pen((0,0,0),0.2)
    pen2 = Pen((0,0,200), 0.2)
    x_from = 14
    x_to = 14 + 60/cos(pi/6)*6/5.5
    y_from = 12
    y_to = 12+40/cos(pi/10)*6/5.5

    head = ObjFile("./obj/bass.obj")

    #head.rotate(1, pi/2)
    head.rotate(2, pi)
    head.squeeze(0, x_from, x_to)
    head.squeeze(1, y_from, y_to)
    head.squeeze(2, 0, 20)
    #head.slice(2, 0)
    #head.show()

    grid_head = GridifiedObj(head, 1)
    #grid_head.show()
    polylines = []
    for x in np.arange(x_from, x_to, 0.3):
        polylines.append(Polyline([Point(x, y_from), Point(x, y_to)], pen1))

    polylines1 = put_polylines_on_object(polylines, grid_head, mask=True)

    
    offset =-4 
    head.move(1, offset)
    head.squeeze(2, 0, 13)
    grid_head = GridifiedObj(head, 0.3)
    polylines = []
    for y in np.arange(y_from+offset, y_to+offset, 0.5):
        polylines.append(Polyline([Point(x_from, y), Point(x_to, y)], pen2))

    polylines = put_polylines_on_object(polylines, grid_head, mask=True)

    for i, polyline in enumerate(polylines):
        polyline.rotate(0, pi/6)
        polyline.rotate(1, -pi/10)
        c.draw_polyline(polyline)

    for i, polyline in enumerate(polylines1):
        polyline.rotate(0, pi/6)
        polyline.rotate(1, -pi/10)
        c.draw_polyline(polyline)
    
    c.show_bitmap(50)
    #ai = AxidrawInterface(c)

if __name__ == "__main__":
    main()
