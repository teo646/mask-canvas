from maskCanvas import Canvas, Polyline, Mask, Point, Circle, Graph, Regular_polygone
from maskCanvas import Pen
from math import cos, sin, pi
def main():
    #size of a3
    c= Canvas(420,297,5,frame=False, paper_color= (255, 255, 255))

    pen = Pen((0,0,0),0.3)
    '''
    outer_path = Regular_polygone(20,80,pen)
    outer_path.move(210, 149)
    for index, point in enumerate(outer_path.path[:-1]):
        sub_square = Regular_polygone(21,7,Pen((0, 50, 100), 0.2))
        sub_square.move_center(point)
        c.draw_polyline(sub_square)
    '''
    '''
    for radius in range(2, 10):
        circle = Circle(radius, Pen((0,0,0),0.3))
        circle.move(210, 149)
        c.draw_polyline(circle)
    graph1 = Graph((lambda t: 20*cos(t)+10*cos(2.73245*t)),\
                     (lambda t: 20*sin(t)+10*sin(2.73245*t)), Pen((0, 0, 100), 0.3), t_range=[0,50*pi])
    graph1.move(210,149)
    c.draw_polyline(graph1)

    outer_path = Regular_polygone(46,180,pen)
    outer_path.move(210, 149)
    for index, point in enumerate(outer_path.path[:-1]):
        sub_square = Regular_polygone(16,7,Pen((0, 0, 128), 0.3))
        sub_square.rotate(2, index/90*pi)
        sub_square.move_center(point)
        c.draw_polyline(sub_square)


    graph1 = Graph((lambda t: 90*cos(t)+27*cos(-pi*t)),\
                     (lambda t: 90*sin(t)+27*sin(-pi*t)), Pen((0, 0, 191), 0.3), t_range=[0,99*pi])
    graph1.move(210,149)
    c.draw_polyline(graph1)
    c.register_mask(graph1.get_mask())
    '''
    graph6 = Graph((lambda t: 200*cos(t)+200*cos(pi*t)),\
                     (lambda t: 200*sin(t)+200*sin(pi*t)), pen, t_range=[0,150*pi])
    graph6.move(210,149)
    c.draw_polyline(graph6)
    c.show_bitmap(10)

if __name__ == "__main__":
    main()
