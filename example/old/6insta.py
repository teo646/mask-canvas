from maskCanvas import Canvas, Polyline, Mask, Point, Circle, Graph, Regular_polygone
from maskCanvas import Pen, draw_linear_background
from math import cos, sin, pi
from copy import deepcopy
import numpy as np
def main():
    #size of a3
    c= Canvas(270,480,5,frame=False, paper_color= (25,15,14))
    paper_center=Point(c.x/2, c.y/2)
    pen = Pen((220,220,250),0.2)


    #------------------------------------------------------------------------------- 
    graph = Graph((lambda t: 1*cos(t)+7.3*cos(-11*t)),\
                  (lambda t: 1*sin(t)+7.3*sin(-11*t)), pen, t_range=[0,3*pi])
    graph.rotate(2, pi/12)
    graph.move_center(paper_center)
    c.draw_polyline(graph)
    #------------------------------------------------------------------------------- 
    graph = Graph((lambda t: 3*cos(t)+2.5*cos(-11*t)**3),\
                  (lambda t: 3*sin(t)+2.5*sin(-11*t)**3), pen, t_range=[0,3*pi])
    graph.move_center(paper_center)
    c.draw_polyline(graph)
    #------------------------------------------------------------------------------- 
    num_circles = 12
    path = Regular_polygone(45, num_circles, pen)
    path.move_center(paper_center)

    circle = Regular_polygone(35, 140,pen)
    points_on_circles = []

    for center in path.path[:-1]:
        circle.move_center(center)
        circle.rotate(2, pi/3)
        points_on_circles.append(deepcopy(circle.path[:-1]))

    path1 = []
    for row in np.array(points_on_circles).T:
        for ele in row:
            path1.append(ele)

    c.draw_polyline(Polyline(path1, pen))
    #------------------------------------------------------------------------------- 

    for center in path.path[:-1]:
        circle.move_center(center)
        c.register_mask(deepcopy(circle.get_mask()))

    circle.move_center(paper_center)
    c.register_mask(deepcopy(circle.get_mask()))

    c= draw_linear_background(c, Pen((200,200,170), 0.5), 80, 60)
    c= draw_linear_background(c, Pen((210, 200, 170), 0.5), 80, 60)
    c= draw_linear_background(c, Pen((250, 200, 150), 0.3), 80, 60)

    c.show_bitmap(20)

if __name__ == "__main__":
    main()
