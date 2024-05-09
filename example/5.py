from maskCanvas import Canvas, Polyline, Mask, Point, Circle, Graph, Regular_polygone
from maskCanvas import Pen, draw_linear_background
from math import cos, sin, pi
def main():
    #size of a3
    c= Canvas(420,297,5,frame=False, paper_color= (25,15,14))

    pen = Pen((250,200,200),0.2)
    
    graph = Graph((lambda t: 8*cos(5*t)+30*cos(1/30*t)+3*t),\
                     (lambda t: 297-8*sin(5*t)+30*sin(1/30*t)-2*t), pen, t_range=[0,150])
    c.draw_polyline(graph)
    c.show_bitmap(50)

if __name__ == "__main__":
    main()
