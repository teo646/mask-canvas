from maskCanvas import Canvas, Polyline, Mask, Point, Arc, Graph, Regular_polygone, Rectangle
from maskCanvas import Pen, draw_linear_background, noise_polyline
from maskCanvas import AxidrawController
from math import cos, sin, pi
from copy import deepcopy
import numpy as np
import random

def main():
    #size of a3
    c= Canvas(297,297,0,frame=False, paper_color= (250,250,250))

    blue_pen = Pen((250,100,100),0.3)
    black_pen = Pen((0,0,0), 0.3)
    orange_pen = Pen((0,102,255), 0.3)


    for i in range(1,49):
        for j in range(1, 49):
            square = Rectangle(5,5,orange_pen)
            square.move(2+i*6, 2+j*6)
            circle = Arc(2, orange_pen)
            circle.move(2+i*6, 2+j*6)
            square = noise_polyline(square, amplitude=j/15)
            circle = noise_polyline(circle, amplitude=j/15)
            
            c.draw_polyline(square)
            c.draw_polyline(circle)

    c.show_bitmap(50)
    
    ac = AxidrawController(c)
#    ac.draw(True, True)

if __name__ == "__main__":
    main()
