from maskCanvas import Canvas, Polyline, Mask, Point, Arc, Graph, Regular_polygone
from maskCanvas import Pen, draw_linear_background, AxidrawInterface, ObjFile
from maskCanvas import dot_object, put_polylines_on_object
from math import cos, sin, pi, atan
import math
import numpy as np
import random

def main():
    #size of a3
    c= Canvas(420,297,15,frame=False, paper_color= (255,255,255))

    pen1 = Pen((0,0,0),0.2)
    pen2 = Pen((0,0,200), 0.2)
    x_from = 30
    x_to = 390
    y_from = 27
    y_to = 269

    head = ObjFile("./obj/Buda_head_OBJ.obj")
    
    head.rotate(1, pi/2)
    head.rotate(2, pi/2)
    head.rotate(0, -pi/6)
    head.rotate(1, -pi/10)

    head.squeeze(0, x_from, x_to)
    head.squeeze(1, y_from, y_to)
    head.squeeze(2, 1, 5)

    head.back_space_cull()
    head.setup(interval = 1)

    polylines = []

    for x in np.arange(10, 410, 3):
        for y in np.arange(10, 287, 3):
            z = head.get_z(x, y)
            if(z):
                polygone = Regular_polygone(4-z, 5, pen2)
            else:
                polygone = Regular_polygone(3, 5, pen2)
            polygone.rotate(2, random.random()*2*pi/5)
            polygone.move(x, y)
            c.draw_polyline(polygone)

    for x in np.arange(10, 410, 1.5):
        for y in np.arange(10, 287, 1.5):
            z = head.get_z(x, y)
            if(z):
                polygone = Regular_polygone(z, 7, pen1)
            else:
                polygone = Regular_polygone(0.3, 7, pen1)
            polygone.rotate(2, random.random()*2*pi/5)
            polygone.move(x, y)
            c.draw_polyline(polygone)
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
    ai = AxidrawInterface(c)

if __name__ == "__main__":
    main()
