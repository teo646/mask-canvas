import numpy as np
from bisect import bisect_left
from .util import *
from .elements import line_segment, point
#you can either put point instance or coordinates as path


class mask:


    def isValid(self):
        if(len(self.path) > 2):
            return True
        else:
            return False

    def removeDuplicatedIndex(self, path):
        duplicated_index = []
        for i in range(len(path)):
            if(path[i-1].x == path[i].x and path[i-1].y == path[i].y):
                duplicated_index.append(i)
        for i in reversed(duplicated_index):
            del path[i]
        
        return path

    def convertToPoints(self, points):
        if(not isinstance(points[0], point)):
            tmp = []
            for p in points:
                tmp.append(point(p[0], p[1]))
            points = tmp

        return points

    def __init__(self, path):
        path = self.convertToPoints(path)
        self.path = self.removeDuplicatedIndex(path)

            

    def getIntersectionsAndIndex(self, line):
        intercept = line.getIntercept(line.points[0])
        intersections = []

        #get intersections between mask and line(not line segment)
        vertex1_sign = line.getIntercept(self.path[-1]) - intercept
        for index in range(len(self.path)):
            vertex2_sign = line.getIntercept(self.path[index]) - intercept
            #basic intersecting case
            if(vertex1_sign*vertex2_sign < 0):
                intersection = line.getLineIntersection(line_segment([self.path[index-1], self.path[index]]))
                if(intersection):
                    intersections.append(intersection)
            #case where a vertex lies on the line
            elif(vertex1_sign == 0 and (line.getIntercept(self.path[index-2])-intercept)*vertex2_sign < 0):
                intersections.append(self.path[index-1])
            vertex1_sign = vertex2_sign


        #get line segments from intersections
        if(line.useDX):
            intersections = sorted(intersections, key= lambda point: point.x)
            point1_index = bisect_left(KeyWrapper(intersections, key=lambda c: c.x), line.points[0].x)
            point2_index = bisect_left(KeyWrapper(intersections, key=lambda c: c.x), line.points[1].x)
        else:
            intersections = sorted(intersections, key= lambda point: point.y)
            point1_index = bisect_left(KeyWrapper(intersections, key=lambda c: c.y), line.points[0].y)
            point2_index = bisect_left(KeyWrapper(intersections, key=lambda c: c.y), line.points[1].y)

        return intersections, point1_index, point2_index

    #mask line segment
    def maskLineSegment(self, line):
        intersections, point1_index, point2_index = self.getIntersectionsAndIndex(line)

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
            masked_lines.append(line_segment([line.points[0], intersections[point1_index]], color = line.color, thickness = line.thickness))
            point1_index += 1
        if(point2_index%2 == 0):
            masked_lines.append(line_segment([intersections[point2_index-1], line.points[1]], color = line.color, thickness = line.thickness))
            point2_index -= 1
        for index in range(point1_index, point2_index, 2):
            masked_lines.append(line_segment([intersections[index], intersections[index+1]], color = line.color, thickness = line.thickness))

        return masked_lines

#mask that let you only draw inside of the mask
class reverse_mask(mask):
    def __init__(self, path):
        super().__init__(path)

    def maskLineSegment(self, line):
        intersections, point1_index, point2_index = self.getIntersectionsAndIndex(line)

        #if there is no intersections
        if(point1_index == point2_index):
            #no masking
            if(point1_index%2 == 0):
                return []
            else:
                return [line]

        #if there is any intersection
        masked_lines = []
        if(point1_index%2 == 1):
            masked_lines.append(line_segment([line.points[0], intersections[point1_index]], color = line.color, thickness = line.thickness))
            point1_index += 1
        if(point2_index%2 == 1):
            masked_lines.append(line_segment([intersections[point2_index-1], line.points[1]], color = line.color, thickness = line.thickness))
            point2_index -= 1
        for index in range(point1_index, point2_index, 2):
            masked_lines.append(line_segment([intersections[index], intersections[index+1]], color = line.color, thickness = line.thickness))

        return masked_lines

