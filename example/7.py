from maskCanvas import Canvas, Polyline, Mask, Point, Arc, Graph, Regular_polygone
from maskCanvas import Pen, draw_linear_background
from maskCanvas import AxidrawController
from math import cos, sin, pi
from copy import deepcopy
import numpy as np

def z_function(t):
    x_value=200*cos(t)+200*cos(pi*t)
    y_value=200*sin(t)+200*sin(pi*t)
    return np.sqrt(x_value**2 + y_value**2)/30

def main():
    #size of a3
    c= Canvas(420,297,10,frame=False, paper_color= (250,250,250))

    pen = Pen((250,100,100),0.3)

    graph6 = Graph((lambda t: 200*cos(t)+200*cos(pi*t)),\
            (lambda t: 200*sin(t)+200*sin(pi*t)), Pen((10,10,10), 0.3), t_range=[0,150*pi], z_func=z_function)
    graph6.move(210, 148)

    for index, point in enumerate(graph6.path):
        if(index%3 == 0):
            circle = Arc(point.coordinate[2]*2, pen)
            circle.move_center(point)
            c.draw_polyline(circle)

    c.show_bitmap(50)
    
    ac = AxidrawController(c)
    #ac.draw(False, True)

if __name__ == "__main__":
    main()
