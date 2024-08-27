from maskCanvas import Canvas, Polyline, Mask, Point, Circle, Graph
from maskCanvas import Pen
from math import cos, sin, pi
colors = [ (0, 0, 255),  (0, 255, 0),  (255, 0, 0),  (0, 255, 255),  (255, 0, 255)]
def main():
    c= Canvas(420,297,5,frame=False)

    pen = Pen((60,60,60),0.3)
    graph1 = Graph((lambda t: 100*cos(t)+30*cos(-pi*t)),\
                     (lambda t: 100*sin(t)+30*sin(-pi*t)), Pen((255, 0, 255), 0.3), t_range=[0,200*pi])
    graph1.move(210,149)
    c.draw_polyline(graph1)

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
