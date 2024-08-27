from maskCanvas import Canvas, Polyline, Mask, Point, Circle, Graph
from maskCanvas import Pen
from math import cos, sin, pi
colors = [ (0, 0, 255),  (0, 255, 0),  (255, 0, 0),  (0, 255, 255),  (255, 0, 255)]
def main():
    c= Canvas(420,297,5,frame=False)

    pen = Pen((60,60,60),0.3)
    for i in range(1,5):
        graph = Graph((lambda t: i*10*cos(t)+i*10*cos(pi*t)),\
                     (lambda t: i*10*sin(t)+i*10*sin(pi*t)), Pen((30*i,30*i,30*i), 0.3), t_range=[0,150*pi])
        graph.move(210,149)
        c.draw_polyline(graph)
        c.register_mask(graph.get_mask())

    graph6 = Graph((lambda t: 200*cos(t)+200*cos(pi*t)),\
                     (lambda t: 200*sin(t)+200*sin(pi*t)), pen, t_range=[0,150*pi])
    graph6.move(210,149)
    c.draw_polyline(graph6)

    c.show_bitmap(10)

if __name__ == "__main__":
    main()

