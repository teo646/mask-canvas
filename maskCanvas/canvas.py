import numpy as np
import cv2
from .elements import line_seg
from .mask import mask
import math

class canvas:
    def __init__(self):
        self.line_segs = []
        self.masks = []

    #you an either put line or two points as a parameter
    #this needs to be edited to masked by only nearby masks
    def registerLineSeg(self, line):
        if(not isinstance(line, line_seg)):
            line = line_seg(line)
        line_segs_to_mask  = [line] 
        for mask in self.masks:
            masked_lines = []
            for line in line_segs_to_mask:
                masked_lines += mask.maskLineSeg(line)
            line_segs_to_mask = masked_lines

        self.line_segs += line_segs_to_mask

        
    #you can either put mask or path as a parameter
    def registerMask(self, mask_instance):
        if(not isinstance(mask_instance, mask)):
            mask_instance = mask(mask_instance)
        self.masks.append(mask_instance)

    def draw(self, magnification):
        x_max = math.ceil(max(self.line_segs, key = lambda c: c.getXMax()).getXMax()*1.2)
        y_max = math.ceil(max(self.line_segs, key = lambda c: c.getYMax()).getYMax()*1.2)

        canvas = np.full((y_max*magnification,x_max*magnification), 255, dtype='uint8')

        for line in self.line_segs:
            canvas = line.draw(canvas, magnification)

        return np.flip(canvas, axis=0)
