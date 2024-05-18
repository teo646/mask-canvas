from maskCanvas import Canvas, Polyline, Mask, Point, Arc, Graph, Regular_polygone
from maskCanvas import Pen, draw_linear_background
from math import cos, sin, pi
def main():
    #size of a3
    c= Canvas(420,297,5,frame=False, paper_color= (25,15,14))

    pen = Pen((250,200,200),0.2)
    
    graph = Graph((lambda t: 8*cos(t)+8*cos(3.34256*t)),\
                     (lambda t: 8*sin(t)+8*sin(3.34256*t)), pen, t_range=[0,40*pi])
    graph.move(210,149)
    graph.rotate(2, pi/3)
    c.draw_polyline(graph)

    outer_path = Regular_polygone(35, 150,pen)
    outer_path.move(210, 149)
    for index, point in enumerate(outer_path.path[:-1]):
        sub_square = Regular_polygone(15,7,pen)
        sub_square.move_center(point)
        c.draw_polyline(sub_square)

    outer_path = Regular_polygone(60, 250,pen)
    outer_path.move(210, 149)
    for index, point in enumerate(outer_path.path[:-1]):
        sub_square = Regular_polygone(21,7, pen)
        sub_square.move_center(point)
        c.draw_polyline(sub_square)

    graph = Graph((lambda t: 80*cos(t)+1*cos(8*t)),\
                     (lambda t: 80*sin(t)+1*sin(8*t)), pen, t_range=[0,6*pi])
    graph.move(210,149)
    c.draw_polyline(graph)
    c.register_mask(graph.get_mask())

    c= draw_linear_background(c, Pen((170,150,200), 0.5), 80, 60)
    c= draw_linear_background(c, Pen((170, 120, 210), 0.5), 80, 60)
    c= draw_linear_background(c, Pen((150, 150, 250), 0.3), 80, 60)
    c.show_bitmap(50)

if __name__ == "__main__":
    main()
