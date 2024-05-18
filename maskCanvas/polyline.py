import numpy as np
from copy import deepcopy
from math import pi, cos, sin, atan2
from .mask import Mask
from .components import Point
from .util import get_outline
import cv2

class Polyline():

    def _get_center(self):
        x_mean = np.array([p.coordinate[0] for p in self.path]).mean()
        y_mean = np.array([p.coordinate[1] for p in self.path]).mean()
        z_mean = np.array([p.coordinate[2] for p in self.path]).mean()
        return Point(x_mean, y_mean, z_mean)

    def __init__(self, path, pen):
        self.path = path
        self.pen = pen
        self.center = self._get_center()

    def draw_bitmap(self, image, magnification):
        for p1, p2 in zip(self.path, self.path[1:]):
            image = cv2.line(image, p1.as_numpy(magnification), p2.as_numpy(magnification)\
                    , self.pen.color, int(self.pen.thickness*magnification))
        return image

    def get_mask(self):
        return None

    #axis 0 = x, 1 = y, 2 = z.
    def rotate(self, axis, angle):
        if(axis == 0):
            rotate_mat = np.array([[1, 0, 0, 0],
                                   [0, cos(angle), -sin(angle), 0],
                                   [0, sin(angle), cos(angle), 0],
                                   [0, 0, 0, 1]])
        elif(axis == 1):
            rotate_mat = np.array([[cos(angle), 0, sin(angle), 0],
                                   [0, 1, 0, 0],
                                   [-sin(angle), 0, cos(angle), 0],
                                   [0, 0, 0, 1]])
        else:
            rotate_mat = np.array([[cos(angle), -sin(angle), 0, 0],
                                   [sin(angle), cos(angle), 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1]])
        center = deepcopy(self.center)
        self.move(-center.coordinate[0], -center.coordinate[1])
        for point in self.path:
            point.coordinate = np.matmul(rotate_mat,point.coordinate)
        self.move(center.coordinate[0], center.coordinate[1])

    def scale(self, ratio):
        scale_mat = np.identity(4)
        scale_mat[:3] *= ratio
        center = deepcopy(self.center)
        self.move(-center.coordinate[0], -center.coordinate[1])
        for point in self.path:
            point.coordinate = np.matmul(scale_mat,point.coordinate)
        self.move(center.coordinate[0], center.coordinate[1])

    def move(self, dx, dy):
        for point in self.path:
            point.coordinate[0] += dx
            point.coordinate[1] += dy

        self.center.coordinate[0] += dx
        self.center.coordinate[1] += dy

    def move_center(self, point):
        dx = point.coordinate[0]-self.center.coordinate[0]
        dy = point.coordinate[1]-self.center.coordinate[1]
        self.move(dx, dy)

class Rectangle(Polyline):
    def _get_center(self):
        return Point(0,0,0)

    def __init__(self, x, y, pen):
        path = [Point(-x/2, -y/2), Point(x/2, -y/2), Point(x/2, y/2),\
                Point(-x/2, y/2), Point(-x/2,-y/2)]
        super().__init__(path, pen)

    def get_mask(self):
        return Mask(self.path)

class Regular_polygone(Polyline):
    def _get_center(self):
        return Point(0,0,0)

    def __init__(self, radius, num_angles, pen):
        inner_angle = 0
        path = []
        for index in range(num_angles+1):
            path.append(Point(cos(inner_angle)*radius, sin(inner_angle)*radius))
            inner_angle += 2*pi/num_angles

        super().__init__(path, pen)

    def get_mask(self):
        return Mask(self.path)

class Graph(Polyline):

    def _get_center(self):
        return Point(0,0,0)

    def __init__(self, x_func, y_func, pen, t_range=(0,2*pi), z_func=lambda t: 0, precision=0.01):
        self.x_func = x_func
        self.y_func = y_func
        self.z_func = z_func
        self.t_range = t_range
        self.precision=precision
        if(t_range[0]<t_range[1]):
            path = self._get_path()
        else:
            print("t_range begin should be smaller than the end")
            path = []
        super().__init__(path, pen)

    def _get_path(self):
        path=[]
        t_current = self.t_range[0]
        while t_current < self.t_range[1]:
            current_point = Point(self.x_func(t_current), self.y_func(t_current), self.z_func(t_current))
            path.append(current_point)
            t_current += self.precision
        return path

    def get_mask(self):
        alpha = 10
        outline_on_angle = np.zeros((360*alpha))
        t_current = self.t_range[0]
        while t_current < self.t_range[1]:
            x = self.x_func(t_current)
            y = self.y_func(t_current)
            angle = int(atan2(y,x)/pi*180*alpha)
            radius = np.linalg.norm(np.array([x,y]))
            if(outline_on_angle[angle] < radius):
                outline_on_angle[angle] = radius
            t_current += 0.0001
    
        outline_path = []
        for angle, radius in enumerate(outline_on_angle):
            if((not radius == 0) and abs(radius-outline_on_angle[angle-1])<0.5):
                outline_path.append(Point(self.center.coordinate[0]+radius*cos(angle*pi/180/alpha),\
                        self.center.coordinate[1]+radius*sin(angle*pi/180/alpha)))

        return Mask(outline_path)


class Arc(Graph):
    def __init__(self, radius, pen, t_range=(0,2*pi), precision=0.1):
        path = []
        x_func=lambda t: radius*cos(t)
        y_func=lambda t: radius*sin(t)
        super().__init__(x_func, y_func, pen, t_range=t_range, precision=precision)

