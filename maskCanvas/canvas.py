import numpy as np
import cv2
from .elements import line_segment, path
from .mask import mask
from .util import showImage
import math

class canvas:
    def __init__(self, color=(0,0,0), thickness=0.3):
        self.line_segs = []
        self.masks = []
        self.color = color
        self.thickness = thickness

    def changePen(self, color, thickness):
        self.color = color
        self.thickness = thickness

    def drawLineSegment(self, line):
        if(not isinstance(line, line_segment)):
            line = line_segment(line, self.color, self.thickness)

        if(line.isValid()):
            line_segs_to_mask  = [line] 
            for mask in self.masks:
                masked_lines = []
                for line in line_segs_to_mask:
                    if(line.isValid()):
                        masked_lines += mask.maskLineSegment(line)
                line_segs_to_mask = masked_lines
            self.line_segs += line_segs_to_mask
        
    def drawPath(self, path_):
        if(not isinstance(path_, path)):
            path_ = path(path_, self.color, self.thickness)

        for line in path_.lines:
            self.drawLineSegment(line)


    #you can either put mask or path as a parameter
    def registerMask(self, mask_instance):
        if(not isinstance(mask_instance, mask)):
            mask_instance = mask(mask_instance)

        if(mask_instance.isValid()):
            self.masks.append(mask_instance)



    def show(self, magnification):
        x_max = math.ceil(max(self.line_segs, key = lambda c: c.getXMax()).getXMax()*1.2)
        y_max = math.ceil(max(self.line_segs, key = lambda c: c.getYMax()).getYMax()*1.2)

        image = np.full((y_max*magnification,x_max*magnification,3), 255, dtype='uint8')

        for line in self.line_segs:
            image = line.draw(image, magnification)

        showImage(image)
