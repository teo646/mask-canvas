import numpy as np
from copy import deepcopy
from bisect import bisect_left, insort
from .util import identical_points, get_y_intercept_function,\
        get_lines_intersection
from .region import Region
from .components import Point

class Mask:
    def _remove_duplicated_index(self, path):
        duplicated_index = []
        for i in range(len(path)):
            if(identical_points(path[i-1], path[i])):
                duplicated_index.append(i)
        for i in reversed(duplicated_index):
            del path[i]
        
        return path

    def _get_region(self):
        x_values = np.array([p.coordinate[0] for p in self.path])
        y_values = np.array([p.coordinate[1] for p in self.path])
        return Region(np.min(x_values), np.max(x_values), np.min(y_values),\
                np.max(y_values))

    def __init__(self, path, reverse=False):
        self.path = self._remove_duplicated_index(path)
        self.region = self._get_region()
        self.reverse = reverse
        if(self.reverse):
            self.region.is_overlaying = lambda region: True

            

    def _get_intersections(self, point1, point2):
        get_y_intercept = get_y_intercept_function(point1, point2)
        intercept = get_y_intercept(point1)
        intersections = []

        #get intersections between mask and line(not line segment)
        vertex1_sign = get_y_intercept(self.path[-1]) - intercept
        for index in range(len(self.path)):
            vertex2_sign = get_y_intercept(self.path[index]) - intercept
            #basic intersecting case
            if(vertex1_sign*vertex2_sign < 0):
                intersection = get_lines_intersection(self.path[index-1], self.path[index], point1, point2)
                intersections.append(intersection)
            #case where a vertex lies on the line
            elif(vertex1_sign == 0 and (get_y_intercept(self.path[index-2])-intercept)*vertex2_sign < 0):
                intersections.append(self.path[index-1])
            vertex1_sign = vertex2_sign

        return intersections

    #mask line segment
    def mask_line_segment(self, point1, point2):

        #if abs(slope) is bigger than 1 y interception can be too big(or small)
        #then symmetrically transpose mask and points on y=x. and then get the masked lines 
        #and symmetrically transpose them again.
        if(abs(point2.coordinate[1]-point1.coordinate[1])>\
                abs(point2.coordinate[0]-point1.coordinate[0])):

            for p in self.path:
                p.yx_convert()
            point1.yx_convert()
            point2.yx_convert()

            masked_lines = deepcopy(self.mask_line_segment(point1, point2))

            for line in masked_lines:
                for point in line:
                    point.yx_convert()
            for p in self.path:
                p.yx_convert()
            point1.yx_convert()
            point2.yx_convert()
            return masked_lines

        intersections = self._get_intersections(point1, point2)
        intersections += [point1, point2]
        intersections = sorted(intersections, key= lambda point: point.coordinate[0])
        point1_index = bisect_left(intersections, point1.coordinate[0], key=lambda c: c.coordinate[0])
        point2_index = bisect_left(intersections, point2.coordinate[0], key=lambda c: c.coordinate[0])
        if(point1_index>point2_index):
            intersections.reverse()
            point1_index = len(intersections)-point1_index-1
            point2_index = len(intersections)-point2_index-1

        masked_lines = []
        for index in range(point1_index, point2_index):
            if(index%2 == self.reverse):
                masked_lines.append([intersections[index], intersections[index+1]])
        return masked_lines

