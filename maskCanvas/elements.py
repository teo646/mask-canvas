import numpy as np
import sys
from math import pi, cos, sin
import cv2
DEFAULT_LINE_COLOR = (0,0,0)
DEFAULT_LINE_THICKNESS = 0.3


class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def asNumpy(self, magnification):
        return np.array([self.x, self.y])*magnification

    def print(self):
        print(self.x, self.y)
class line_seg:
    def __init__(self, points, color = DEFAULT_LINE_COLOR, thickness = DEFAULT_LINE_THICKNESS):
        if(len(points) != 2 or points[0] == points[1]):
            raise Exception("line has to have two different points")

        if(not isinstance(points[0], point)):
            tmp = []
            for p in points:
                tmp.append(point(p[0], p[1]))
            points = tmp

        self.vertical = True if abs(points[1].x - points[0].x) < 0.001 else False
        if(self.vertical and points[0].y > points[1].y):
            points.reverse()
        elif(points[0].x > points[1].x):
            points.reverse()

        self.points = points
        self.color= color
        self.thickness = thickness

    def getXMax(self):
        return self.points[1].x

    def getXMin(self):
        return self.points[0].x

    def getYMax(self):
        return self.points[0].y if self.points[0].y > self.points[1].y else self.points[1].y

    def getYMin(self):
        return self.points[0].y if self.points[0].y < self.points[1].y else self.points[1].y


    def slope(self):
        if(not self.vertical):
            return (float)(self.points[1].y-self.points[0].y)/(self.points[1].x-self.points[0].x)
        return None

    def draw(self, image, magnification):
        return cv2.line(image, self.points[0].asNumpy(magnification).astype('uint'), self.points[1].asNumpy(magnification).astype('uint'), self.color, int(self.thickness*magnification))

    def getLineIntersection(self, line):
        # Line AB represented as a1x + b1y = c1
        A = self.points[0]
        B = self.points[1]
        C = line.points[0]
        D = line.points[1]

        a1 = B.y - A.y
        b1 = A.x - B.x
        c1 = a1*(A.x) + b1*(A.y)

        # Line CD represented as a2x + b2y = c2
        a2 = D.y - C.y
        b2 = C.x - D.x
        c2 = a2*(C.x) + b2*(C.y)

        determinant = a1*b2 - a2*b1

        try:
            x = (b2*c1 - b1*c2)/determinant
            y = (a1*c2 - a2*c1)/determinant
        except ZeroDivisionError as e:
            print("you tried to get intersection of parallel lines")
            x = 0
            y = 0

        return point(x, y)
    
    def print(self):
        self.points[0].print()
        self.points[1].print()


class arc:
    unit_line_length = 0.5
    def __init__(self, center, radius, start_angle=0, end_angle=2*pi):
        self.lines = []

        if(start_angle > end_angle):
            end_angle += 2*pi
        unit_angle = self.unit_line_length/radius

        p1 = point(center.x+radius*cos(start_angle), center.y-radius*sin(start_angle))
        for angle in np.arange(start_angle+unit_angle, end_angle, unit_angle):
            p2 = point(center.x+radius*cos(angle), center.y-radius*sin(angle))
            self.lines.append(line_seg([p1,p2]))
            p1=p2
        


