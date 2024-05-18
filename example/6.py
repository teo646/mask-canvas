from maskCanvas import Canvas, Polyline, Mask, Point, Arc, Graph, Regular_polygone
from maskCanvas import Pen, draw_linear_background
from maskCanvas import AxidrawController
from math import cos, sin, pi
from copy import deepcopy
import numpy as np
def main():
    #size of a3
    c= Canvas(420,297,10,frame=False, paper_color= (250,250,250))

    pen = Pen((250,100,100),0.3)

    #-------------------------------------------------------------------------------1
    center = Point(115, 200)
    scale = 1.2
    graph = Graph((lambda t: 1*cos(t)+7.3*cos(-11*t)),\
                  (lambda t: 1*sin(t)+7.3*sin(-11*t)), pen, t_range=[0,3*pi])
    graph.scale(scale)
    graph.rotate(2, pi/12)
    graph.move_center(center)
    c.draw_polyline(graph)
    #------------------------------------------------------------------------------- 
    graph = Graph((lambda t: 3*cos(t)+2.5*cos(-11*t)**3),\
                  (lambda t: 3*sin(t)+2.5*sin(-11*t)**3), pen, t_range=[0,2*pi])
    graph.scale(scale)
    graph.move_center(center)
    c.draw_polyline(graph)
    #------------------------------------------------------------------------------- 
    num_circles = 12
    path = Regular_polygone(45, num_circles, pen)
    path.scale(scale)
    path.move_center(center)

    circle = Regular_polygone(35, 120,pen)
    circle.scale(scale)
    points_on_circles = []

    for vertex in path.path[:-1]:
        circle.move_center(vertex)
        circle.rotate(2, pi/3)
        points_on_circles.append(deepcopy(circle.path))

    path1 = []
    for row in np.array(points_on_circles).T:
        for ele in row:
            path1.append(ele)

    c.draw_polyline(Polyline(path1, pen))
    #-------------------------------------------------------------------------------

    for vertex in path.path[:-1]:
        circle.move_center(vertex)
        c.register_mask(deepcopy(circle.get_mask()))

    circle.move_center(center)
    c.register_mask(deepcopy(circle.get_mask()))

    #-------------------------------------------------------------------------------2
    center = Point(270, 10)
    scale = 1
    graph = Graph((lambda t: 1*cos(t)+7.3*cos(-11*t)),\
                  (lambda t: 1*sin(t)+7.3*sin(-11*t)), pen, t_range=[0,3*pi])
    graph.scale(scale)
    graph.rotate(2, pi/12)
    graph.move_center(center)
    c.draw_polyline(graph)
    #------------------------------------------------------------------------------- 
    graph = Graph((lambda t: 3*cos(t)+2.5*cos(-11*t)**3),\
                  (lambda t: 3*sin(t)+2.5*sin(-11*t)**3), pen, t_range=[0,2*pi])
    graph.scale(scale)
    graph.move_center(center)
    c.draw_polyline(graph)
    #------------------------------------------------------------------------------- 
    num_circles = 12
    path = Regular_polygone(45, num_circles, pen)
    path.scale(scale)
    path.move_center(center)

    circle = Regular_polygone(35, 90,pen)
    circle.scale(scale)
    points_on_circles = []

    for vertex in path.path[:-1]:
        circle.move_center(vertex)
        circle.rotate(2, pi/3)
        points_on_circles.append(deepcopy(circle.path))

    path1 = []
    for row in np.array(points_on_circles).T:
        for ele in row:
            path1.append(ele)

    c.draw_polyline(Polyline(path1, pen))
    #-------------------------------------------------------------------------------

    for vertex in path.path[:-1]:
        circle.move_center(vertex)
        c.register_mask(deepcopy(circle.get_mask()))

    circle.move_center(center)
    c.register_mask(deepcopy(circle.get_mask()))

    #-------------------------------------------------------------------------------3
    center = Point(80, 110)
    scale = 0.6
    graph = Graph((lambda t: 1*cos(t)+7.3*cos(-11*t)),\
                  (lambda t: 1*sin(t)+7.3*sin(-11*t)), pen, t_range=[0,3*pi])
    graph.scale(scale)
    graph.rotate(2, pi/12)
    graph.move_center(center)
    c.draw_polyline(graph)
    #------------------------------------------------------------------------------- 
    graph = Graph((lambda t: 3*cos(t)+2.5*cos(-11*t)**3),\
                  (lambda t: 3*sin(t)+2.5*sin(-11*t)**3), pen, t_range=[0,2*pi])
    graph.scale(scale)
    graph.move_center(center)
    c.draw_polyline(graph)
    #------------------------------------------------------------------------------- 
    num_circles = 8
    path = Regular_polygone(45, num_circles, pen)
    path.scale(scale)
    path.move_center(center)

    circle = Regular_polygone(35, 90,pen)
    circle.scale(scale)
    points_on_circles = []

    for vertex in path.path[:-1]:
        circle.move_center(vertex)
        circle.rotate(2, pi/2)
        points_on_circles.append(deepcopy(circle.path))

    path1 = []
    for row in np.array(points_on_circles).T:
        for ele in row:
            path1.append(ele)

    c.draw_polyline(Polyline(path1, pen))
    #-------------------------------------------------------------------------------

    for vertex in path.path[:-1]:
        circle.move_center(vertex)
        c.register_mask(deepcopy(circle.get_mask()))

    circle.move_center(center)
    c.register_mask(deepcopy(circle.get_mask()))

    #-------------------------------------------------------------------------------4
    center = Point(400, 350)
    scale = 2
    graph = Graph((lambda t: 1*cos(t)+7.3*cos(-11*t)),\
                  (lambda t: 1*sin(t)+7.3*sin(-11*t)), pen, t_range=[0,3*pi])
    graph.scale(scale)
    graph.rotate(2, pi/12)
    graph.move_center(center)
    c.draw_polyline(graph)
    #-------------------------------------------------------------------------------
    graph = Graph((lambda t: 3*cos(t)+2.5*cos(-11*t)**3),\
                  (lambda t: 3*sin(t)+2.5*sin(-11*t)**3), pen, t_range=[0,2*pi])
    graph.scale(scale)
    graph.move_center(center)
    c.draw_polyline(graph)
    #-------------------------------------------------------------------------------
    num_circles = 8
    path = Regular_polygone(45, num_circles, pen)
    path.scale(scale)
    path.move_center(center)

    circle = Regular_polygone(35, 150,pen)
    circle.scale(scale)
    points_on_circles = []

    for vertex in path.path[:-1]:
        circle.move_center(vertex)
        circle.rotate(2, pi/2)
        points_on_circles.append(deepcopy(circle.path))

    path1 = []
    for row in np.array(points_on_circles).T:
        for ele in row:
            path1.append(ele)

    c.draw_polyline(Polyline(path1, pen))
    #-------------------------------------------------------------------------------

    for vertex in path.path[:-1]:
        circle.move_center(vertex)
        c.register_mask(deepcopy(circle.get_mask()))

    circle.move_center(center)
    c.register_mask(deepcopy(circle.get_mask()))
    #------------------------------------------------------------------------------
    graph6 = Graph((lambda t: 200*cos(t)+200*cos(pi*t)),\
                     (lambda t: 200*sin(t)+200*sin(pi*t)), Pen((10,10,10), 0.3), t_range=[0,150*pi])
    graph6.move(115, 200)
    c.draw_polyline(graph6)

    c.show_bitmap(50, noise=True)
    
    ac = AxidrawController(c)
    #ac.draw(False, True)

if __name__ == "__main__":
    main()
