import numpy as np
from copy import deepcopy

class Pen:
    def __init__(self, color, thickness):
        self.color = color
        self.thickness = thickness

class Point():
    def __init__(self, x,y,z=0):
        self.coordinate = np.array(deepcopy([x,y,z,1]), dtype='float')

    def yx_convert(self):
        tmp = self.coordinate[0]
        self.coordinate[0] = self.coordinate[1]
        self.coordinate[1] = tmp

    def as_numpy(self, magnification):
        return np.array([self.coordinate[0]*magnification,\
                self.coordinate[1]*magnification]).astype('uint')

