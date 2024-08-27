from maskCanvas import Canvas, Polyline, Mask, Point, Arc, Graph, Regular_polygone, Rectangle
from maskCanvas import Pen, draw_linear_background, noise_polyline
from maskCanvas import Obj
from maskCanvas import AxidrawInterface
from math import cos, sin, pi
from copy import deepcopy
import numpy as np
import random

def main():
    #size of a3
    c= Canvas(400,300,20,frame=False, paper_color= (250,250,250))

    pen = Pen((30,30,30),0.3)

    of = Obj("./obj/screaming_face.obj")
    of.rotate(1, pi)
    of.rotate(2, pi/2)
    of.scale(0, 1000)
    of.scale(1, 1000)
    of.scale(2, 3)
    of.slice(2, 0.05)
    of.move(0, 200)
    of.move(1, 150)
    of.move(2, -0.05)
    of.show_points()
    field = of.generate_field(0.6)
#    field.show_points()
    for i in range(297):
        line = Polyline([Point(0, i), Point(420, i)], pen)
        c.draw_polyline(line)
    for i in range(420):
        line = Polyline([Point(i, 0), Point(i, 297)], pen)
        c.draw_polyline(line)
    for i in range(1000):
        line = Polyline([Point(i, 0), Point(0, i)], pen)
        c.draw_polyline(line)
    for i in range(-404, 582):
        line = Polyline([Point(i, 0), Point(1000, 1000-i)], pen)
        c.draw_polyline(line)
    c.polylines = field.noise_polylines(c.polylines)
    c.show_bitmap(50)
#    of.show_points()

    ac = AxidrawInterface(c)

if __name__ == "__main__":
    main()
