from maskCanvas import canvas, showImage, line_seg, circle, point
from math import pi
def main():
    c= canvas()

    center = point(100,100)
    radius = 30
    c.registerCircle(circle(center, radius))

    center = point(20,20)
    radius = 10
    c.registerCircle(circle(center, radius, 0, pi))

    center = point(150,100)
    radius = 25
    c.registerCircle(circle(center, radius, pi/6, pi*1.5))

    showImage(c.draw(30))

if __name__ == "__main__":
    main()

