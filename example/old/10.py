from maskCanvas import Canvas, Polyline, Mask, Point, Arc, Graph, Regular_polygone, Rectangle
from maskCanvas import Pen, draw_linear_background, noise_polylines
from maskCanvas import AxidrawInterface
from math import cos, sin, pi
from copy import deepcopy
import numpy as np
import random

def main():
    #size of a3
    c= Canvas(420,297,10,frame=False, paper_color= (250,250,250))

    blue_pen = Pen((250,100,100),0.3)
    ultramarin_pen = Pen((143, 10, 18), 0.3)
    light_blue_pen = Pen((210, 196, 153), 0.3)
    cadmium_red_pen=Pen((34,0,227), 0.3)
    black_pen = Pen((0,0,0), 0.3)
    orange_pen = Pen((0,102,255), 0.3)
    warm_grey_pen = Pen((168, 181, 194), 0.1)
    burnt_sianna_pen=Pen((42,42,165), 0.3)
    colors = [blue_pen, ultramarin_pen, light_blue_pen, cadmium_red_pen, black_pen, orange_pen, warm_grey_pen, burnt_sianna_pen]


    for i in range(1,300):
        circle = Arc(i*0.3, colors[0], precision=0.03)
        circle.rotate(2, random.random()*2*pi)
        circle.move(210, 148.5)
        c.draw_polyline(circle)

            

    c.polylines = noise_polylines(c.polylines, scale=0.08, amplitude=12)
    c.show_bitmap(50)
    
    ac = AxidrawInterface(c)

if __name__ == "__main__":
    main()
