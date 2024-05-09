import numpy as np
import cv2
from .components import Point, Pen
from .polyline import Polyline
from .mask import Mask
from .region import Region
from .util import is_valid_mask, identical_points, show_image
import math
import random

class Canvas:
    def __init__(self, x, y, offset, frame=True, frame_pen = Pen((0,0,0), 1), paper_color=(0,0,0)):
        self.polylines = []
        self.masks = []
        self.x = x
        self.y = y
        self.offset = offset
        self.paper_color = np.array(list(paper_color))
        paper_region_path = [Point(offset,offset), Point(x-offset,offset),\
                Point(x-offset,y-offset),Point(offset,y-offset)]
        if(frame):
            self.draw_polyline(Polyline(paper_region_path+[paper_region_path[0]], frame_pen))
        self.register_mask(Mask(paper_region_path, reverse=True))
        
    def draw_polyline(self, polyline):
        current_point = polyline.path[0]
        current_path = [current_point]
        for p1, p2 in zip(polyline.path, polyline.path[1:]):
            for line in self._mask_segment(p1,p2):
                if(identical_points(current_point, line[0])):
                    current_point = line[1]
                    current_path.append(current_point)
                else:
                    if(not len(current_path) == 1):
                        self.polylines.append(Polyline(current_path, polyline.pen))
                    current_path = [line[0], line[1]]
                    current_point = line[1]
        if(not len(current_path) == 1):
            self.polylines.append(Polyline(current_path, polyline.pen))   

    def _mask_segment(self, point1, point2):
        if(not identical_points(point1, point2)):
            segments_to_mask  = [[point1, point2]]
            for mask in self._get_mask_in_region(point1, point2):
                masked_lines = []
                for line in segments_to_mask:
                    if(not identical_points(line[0], line[1])):
                        masked_lines += mask.mask_line_segment(line[0], line[1])
                segments_to_mask = masked_lines

            return segments_to_mask
        return []

    def _get_mask_in_region(self, point1, point2):
        region = Region(point1.coordinate[0] if point1.coordinate[0]\
                < point2.coordinate[0] else point2.coordinate[0],
                        point1.coordinate[0] if point1.coordinate[0]\
                                > point2.coordinate[0] else point2.coordinate[0],
                        point1.coordinate[1] if point1.coordinate[1]\
                                < point2.coordinate[1] else point2.coordinate[1],
                        point1.coordinate[1] if point1.coordinate[1]\
                                > point2.coordinate[1] else point2.coordinate[1])
        mask_in_region = []
        for mask in self.masks:
            if(mask.region.is_overlaying(region)):
                mask_in_region.append(mask)

        return mask_in_region

    def register_mask(self, mask):
        if(is_valid_mask(mask)):
            self.masks.append(mask)

    def _get_range_of_points(self):
        x_values = np.array([point.coordinate[0] for point in polyline\
                for polyline in self.polylines])
        y_values = np.array([point.coordinate[1] for point in polyline\
                for polyline in self.polylines])
        return Region(floor(x_values.min()), ceil(x_values.max()), floor(y_values.min()), ceil(y_values.max()))

    def show_bitmap(self, magnification):
        image = np.tile(self.paper_color, (self.y*magnification, self.x*magnification, 1)).astype('uint8')
        for polyline in self.polylines:
            image = polyline.draw_bitmap(image, magnification)
        show_image(image)

        save_image = input("do you want to save the image?")
        if(save_image == 'y'):
            cv2.imwrite('images/'+str(random.random())+'image.jpg', image)
