from maskCanvas import canvas, showImage, line_seg, arc, point
from math import pi
def main():
    c= canvas()

    center = point(100,100)
    radius = 30
    c.registerArc(arc(center, radius, pi/4, pi/4, 0, pi))
    showImage(c.draw(30))

if __name__ == "__main__":
    main()

