from maskCanvas import Canvas, Polyline, Mask, Point, Arc, Graph, Regular_polygone
from maskCanvas import Pen, draw_linear_background, AxidrawInterface, ObjFile
from maskCanvas import dot_object, line_on_object
from math import cos, sin, pi, atan
import math
import numpy as np
import random

def main():
    #size of a3
    c= Canvas(300,200,10,frame=False, paper_color= (255,255,255))

    pen1 = Pen((0,0,0),0.2)

    budha = ObjFile("./obj/Buda_head_OBJ.obj")

    budha.rotate(1, pi/2)
    budha.rotate(2, pi/2)
    budha.squeeze(0, 50, 250)
    budha.squeeze(1, 20, 180)
    budha.squeeze(2, -50, 50)
    budha.slice(2, 0)

    budha.setup(interval = 0.5)

    line_on_object(c, budha, 1, pi/6, pen1)

    c.show_bitmap(50)
    #ai = AxidrawInterface(c)

if __name__ == "__main__":
    main()
