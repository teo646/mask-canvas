from maskCanvas import Canvas, Polyline, Mask, Point, Arc, Graph, Regular_polygone
from maskCanvas import Pen, draw_linear_background, AxidrawInterface, Perlin, dot_object
from math import cos, sin, pi, atan
import math
import numpy as np
import random

def main():
    #size of a3
    c= Canvas(297,210,10,frame=False, paper_color= (255,255,255))

    pen1 = Pen((0,0,0),0.2)

    perlin = Perlin()
    perlin.scale(0.1)

    dot_object(c, perlin, 20000, pen1)

    c.show_bitmap(50)

    ai = AxidrawInterface(c)

if __name__ == "__main__":
    main()
