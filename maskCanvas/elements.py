import numpy as np
import sys
from math import pi, cos, sin, tan
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

        self.points = points
        self.color= color
        self.thickness = thickness
        if(not isinstance(self.points[0], point)):
            tmp = []
            for p in self.points:
                tmp.append(point(p[0], p[1]))
            self.points = tmp
        

        if(self.isValid()):
            self.useDX = True if abs(self.points[1].x - self.points[0].x) > abs(self.points[1].y - self.points[0].y) else False
            if(self.useDX and self.points[0].x > self.points[1].x):
                self.points.reverse()
            elif(not self.useDX and self.points[0].y > self.points[1].y):
                self.points.reverse()

            if(self.useDX):
                self.slope = (float)(self.points[1].y-self.points[0].y)/(self.points[1].x-self.points[0].x)
            else:
                self.slope =  (float)(self.points[1].x-self.points[0].x)/(self.points[1].y-self.points[0].y)

    def isValid(self):
        if(len(self.points) != 2 or (self.points[0].x == self.points[1].x and self.points[0].y == self.points[1].y)):
            return False
        return True

    def getXMax(self):
        return self.points[0].x if self.points[0].x > self.points[1].x else self.points[1].x

    def getXMin(self):
        return self.points[0].x if self.points[0].x < self.points[1].x else self.points[1].x

    def getYMax(self):
        return self.points[0].y if self.points[0].y > self.points[1].y else self.points[1].y

    def getYMin(self):
        return self.points[0].y if self.points[0].y < self.points[1].y else self.points[1].y

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
            return None
        else:
            return point(x,y)
   
    def getIntercept(self, point):
        if(self.useDX):
            return point.y - self.slope*point.x
        else:
            return point.x - self.slope*point.y

    def print(self):
        self.points[0].print()
        self.points[1].print()


class arc:
    unit_line_length = 0.5
    def __init__(self, center, radius, pitch=0, yaw=0, start_angle=0, end_angle=2*pi):
        self.lines = []
        self.center = center
        self.radius = radius
        self.pitch = pitch
        self.yaw = yaw

        if(start_angle > end_angle):
            end_angle += 2*pi

        unit_angle = self.unit_line_length/radius

        p1 = self.getPoint(start_angle)
        for angle in np.arange(start_angle+unit_angle, end_angle, unit_angle):
            p2 = self.getPoint(angle)
            self.lines.append([p1,p2])
            p1=p2
        
    def getPoint(self,angle):
        return point(self.center.x+self.radius*cos(angle)*cos(self.yaw), self.center.y-(sin(self.yaw)*cos(angle)*sin(self.pitch)+sin(angle)*cos(self.pitch))*self.radius)



#               point(point_.x + cos(roll)*cos(yaw)*length*self.scale, point_.y - (sin(yaw)*cos(roll)*sin(pitch)+sin(roll)*cos(pitch))*length*selfssdd.scale)
