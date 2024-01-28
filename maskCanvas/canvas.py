import numpy as np
import cv2
from bisect import bisect_left
from .elements import line_seg

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

        self.line_segs += masked_lines

        
    #you can either put mask or path as a parameter
    def registerMask(self, mask_instance):
        if(not isinstance(mask_instance, mask)):
            mask_instance = mask(mask_instnace)
        self.masks.append(mask_instance)

    def draw(self, magnification):
        x_min = min(self.line_segs, key = lambda c: c.getXMin())
        y_min = min(self.line_segs, key = lambda c: c.getYMin())
        x_max = max(self.line_segs, key = lambda c: c.getXMax())
        y_max = max(self.line_segs, key = lambda c: c.getYMax())

        canvas = np.full(((y_max-y_min)*magnification,(x_max-x_min)*magnification), 255)

        for line in self.line_segs:
            canvas = line.draw(canvas, magnification)

        return canvas
