import numpy as np
from bisect import bisect_left
from .util import *
from .elements import line_seg, point

#you can either put point instance or coordinates as path
class mask:
    def __init__(self, path):
        if(len(path) < 3):
            raise Exception("mask should have at least three points as path")
        if(not isinstance(path[0], point)):
            tmp = []
            for p in path:
                tmp.append(point(p[0], p[1]))
            path = tmp
        self.path = path

    #mask line segment
    def maskLineSeg(self, line):
        y_intercept = getYIntercept(line.slope(), line.points[0])
        intersections = []

        #get intersections between mask and line(not line segment)
        for index in range(len(self.path)):
            vertex1_sign = getYIntercept(line.slope(), self.path[index-1]) - y_intercept
            vertex2_sign = getYIntercept(line.slope(), self.path[index]) - y_intercept
            #basic intersecting case
            if(vertex1_sign*vertex2_sign < 0):
                intersections.append(line.getLineIntersection(line_seg([self.path[index-1], self.path[index]])))
            #case where a vertex lies on the line
            elif(vertex1_sign == 0 and (getYIntercept(line.slope(), self.path[index-2])-y_intercept)*vertex2_sign < 0):
                intersections.append(self.path[index-1])
            vertex1_sign = vertex2_sign

        intersections = sorted(intersections, key= lambda point: point.x)

        #get line segments from intersections
        if(line.slope()):
            point1_index = bisect_left(KeyWrapper(intersections, key=lambda c: c.x), line.points[0].x)
            point2_index = bisect_left(KeyWrapper(intersections, key=lambda c: c.x), line.points[1].x)
        else:
            point1_index = bisect_left(KeyWrapper(intersections, key=lambda c: c.y), line.points[0].y)
            point2_index = bisect_left(KeyWrapper(intersections, key=lambda c: c.y), line.points[1].y)

        #if there is no intersections
        if(point1_index == point2_index):
            #no masking 
            if(point1_index%2 == 0):
                return [line]
            else:
                return []

        #if there is any intersection
        masked_lines = []
        if(point1_index%2 == 0):
            masked_lines.append(line_seg([line.points[0], intersections[point1_index]], color = line.color, thickness = line.thickness))
            point1_index += 1
        if(point2_index%2 == 0):
            masked_lines.append(line_seg([intersections[point2_index-1], line.points[1]], color = line.color, thickness = line.thickness))
            point2_index -= 1
        for index in range(point1_index, point2_index, 2):
            masked_lines.append(line_seg([intersections[index], intersections[index+1]], color = line.color, thickness = line.thickness))

        return masked_lines

