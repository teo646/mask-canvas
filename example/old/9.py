from maskCanvas import Canvas, Polyline, Mask, Point, Arc, Graph, Regular_polygone, Rectangle
from maskCanvas import Pen, draw_linear_background, noise_polyline
from maskCanvas import AxidrawInterface
from math import cos, sin, pi
from copy import deepcopy
import numpy as np
import random

def main():
    #size of a3
    c= Canvas(420,297,0,frame=False, paper_color= (250,250,250))

    blue_pen = Pen((250,100,100),0.3)
    ultramarin_pen = Pen((143, 10, 18), 0.3)
    light_blue_pen = Pen((210, 196, 153), 0.3)
    cadmium_red_pen=Pen((34,0,227), 0.3)
    black_pen = Pen((0,0,0), 0.3)
    orange_pen = Pen((0,102,255), 0.3)
    warm_grey_pen = Pen((168, 181, 194), 0.1)
    burnt_sianna_pen=Pen((42,42,165), 0.3)
    black_pen=Pen((0,0,0), 0.3)


    for i in range(1,3):#69
        for j in range(1, 3):#49
            #square = Rectangle(5,5,orange_pen)
            square = Rectangle(5,5,black_pen)
            #circle = Arc(1.5, orange_pen, precision=0.3)
            square.move(2+i*6, 2+j*6)
            #circle.move(2+i*6, 2+j*6)
            c.draw_polyline(square)

            

    c.show_bitmap(50)
    
    ac = AxidrawInterface(c)

if __name__ == "__main__":
    main()
