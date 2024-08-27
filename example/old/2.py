from maskCanvas import Canvas, Polyline, Mask, Point, Circle, Graph
from maskCanvas import Pen
from math import cos, sin, pi
def main():
    #size of a3
    c= Canvas(420,297,5,frame=False)

    pen = Pen((60,60,60),0.3)
    circle = Circle(60, pen)
    for point in circle.path[::100]:
        sub_circle = Circle(20, pen)
        sub_circle.move_center(point)
        sub_circle.move(210, 149)
        c.draw_polyline(sub_circle)


    '''
    for i in range(66):
        c.draw_polyline(Polyline([Point(210+40*cos(i*pi/(33)+pi/2),149+40*sin(i*pi/(33)+pi/2)),Point(210+100*cos(i*pi/(33)+pi/2),149+100*sin(i*pi/(33)+pi/2))], pen))
    #c.register_mask(graph1.get_mask())
    graph6 = Graph((lambda t: 200*cos(t)+200*cos(pi*t)),\
                     (lambda t: 200*sin(t)+200*sin(pi*t)), pen, t_range=[0,150*pi])
    graph6.move(210,149)
    c.draw_polyline(graph6)
    '''
    c.show_bitmap(10)

if __name__ == "__main__":
    main()
