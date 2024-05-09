from maskCanvas import Canvas, Polyline, Mask, Point, Circle, Graph, Regular_polygone
from maskCanvas import Pen, draw_linear_background
from math import cos, sin, pi
def main():
    #size of a3
    c= Canvas(420,297,5,frame=False, paper_color= (25,15,14))

    pen = Pen((200,200,200),0.3)

    c = draw_linear_background(c, pen, 100, 50)

    c.show_bitmap(50)




if __name__ == "__main__":
    main()
