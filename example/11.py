from maskCanvas import Canvas, Polyline, Mask, Point, Arc, Graph, Regular_polygone
from maskCanvas import Pen, draw_linear_background, noise_polylines, AxidrawInterface
from math import cos, sin, pi, atan
import math
import numpy as np
import random

def main():
    #size of a3
    c= Canvas(291,202,10,frame=False, paper_color= (255,255,255))

    pen1 = Pen((0,0,0),0.2)
    pen2 = Pen((0,255,0),0.2)
    pen3 = Pen((0,0,255),0.2)
    pen4 = Pen((0,255,255),0.2)
    blue_pen = Pen((250,100,100),0.3)
    ultramarin_pen = Pen((143, 10, 18), 0.3)
    light_blue_pen = Pen((210, 196, 153), 0.3)
    cadmium_red_pen=Pen((34,0,227), 0.3)
    black_pen = Pen((0,0,0), 0.3)
    orange_pen = Pen((0,102,255), 0.3)
    warm_grey_pen = Pen((168, 181, 194), 0.1)
    burnt_sianna_pen=Pen((42,42,165), 0.3)
    green_pen=Pen((0,202,0), 0.3)
    dark_green_pen=Pen((30,202,30), 0.3)
    colors = [green_pen, ultramarin_pen, dark_green_pen, cadmium_red_pen, black_pen, orange_pen]

    for i in range(404):
        line = Polyline([Point(0, i*0.5), Point(291, i*0.5)], pen1)
        c.draw_polyline(line)

    c.show_bitmap(50)
    ai = AxidrawInterface(c)

if __name__ == "__main__":
    main()
