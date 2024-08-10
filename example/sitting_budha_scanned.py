from maskCanvas import Canvas, Polyline, Mask, Point, Arc, Graph, Regular_polygone
from maskCanvas import Pen, draw_linear_background, AxidrawInterface, ObjFile
from maskCanvas import dot_object, put_polylines_on_object
from math import cos, sin, pi, atan
import math
import numpy as np
import random

def main():
    #size of a3
    c= Canvas(420,297,0,frame=False, paper_color= (255,255,255))

    pen1 = Pen((0,0,0),0.2)
    pen2 = Pen((0,0,200), 0.2)
    x_from = 30+60
    x_to = 390+60
    y_from = 30+20
    y_to = 267+20

    head = ObjFile("./obj/sitting_budha_scanned.obj")
    
    head.rotate(2, pi/2)
    head.rotate(1, -pi/8)
    head.squeeze(0, x_from, x_to)
    head.squeeze(1, y_from, y_to)
    head.squeeze(2, 0, 150)

    head.rotate(0, -pi/10)
    head.rotate(1, -pi/10)
    head.back_space_cull()
    head.rotate(1, pi/10)
    head.rotate(0, pi/10)
    head.setup(interval = 0.3)
    head.show()

    polylines = []
    for x in np.arange(x_from, x_to, 0.4):
        polylines.append(Polyline([Point(x, y_from), Point(x, y_to)], pen1))

    polylines = put_polylines_on_object(polylines, head, mask=True)

    for i, polyline in enumerate(polylines):
        polyline.rotate(0, -pi/10)
        polyline.rotate(1, -pi/10)
        c.draw_polyline(polyline)
    '''
    offset =0 
    head.move(1, offset)
    head.squeeze(2, 0, 25)
    head.setup(interval = 3)
    polylines = []
    for y in np.arange(y_from+offset, y_to+offset, 0.5):
        polylines.append(Polyline([Point(x_from, y), Point(x_to, y)], pen2))

    polylines = put_polylines_on_object(polylines, head, mask=True)

    for i, polyline in enumerate(polylines):
        polyline.rotate(0, pi/6)
        polyline.rotate(1, pi/6)
        c.draw_polyline(polyline)
    '''
    c.show_bitmap(50)
    #ai = AxidrawInterface(c)

if __name__ == "__main__":
    main()
