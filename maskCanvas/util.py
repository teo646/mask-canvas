import cv2
import numpy as np
from scipy.spatial import Delaunay
from .components import Point


def show_image(image):
# Naming a window
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def identical_points(point1, point2):
    if(point1.coordinate[0] == point2.coordinate[0]\
       and point1.coordinate[1] == point2.coordinate[1]):
        return True
    return False

def is_valid_mask(mask_):
    if(len(mask_.path)>2):
        return True
    return False

def get_y_intercept_function(point1, point2):
    def tmp(point):
        slope = (point2.coordinate[1] - point1.coordinate[1])/(point2.coordinate[0] - point1.coordinate[0])
        return point.coordinate[1] - point.coordinate[0]*slope
    return tmp

def get_line_intersection(A,B,C,D):
        a1 = B.coordinate[1] - A.coordinate[1]
        b1 = A.coordinate[0] - B.coordinate[0]
        c1 = a1*(A.coordinate[0]) + b1*(A.coordinate[1])

        # Line CD represented as a2x + b2y = c2
        a2 = D.coordinate[1] - C.coordinate[1]
        b2 = C.coordinate[0] - D.coordinate[0]
        c2 = a2*(C.coordinate[0]) + b2*(C.coordinate[1])

        determinant = a1*b2 - a2*b1

        if(determinant == 0):
            print("you tried to get intersection of parallel lines")
            return None
        else:
            x = (b2*c1 - b1*c2)/determinant
            y = (a1*c2 - a2*c1)/determinant
            return Point(x,y,0)

def get_lines_intersection(A,B,C,D):
        a1 = B.coordinate[1] - A.coordinate[1]
        b1 = A.coordinate[0] - B.coordinate[0]
        c1 = a1*(A.coordinate[0]) + b1*(A.coordinate[1])

        # Line CD represented as a2x + b2y = c2
        a2 = D.coordinate[1] - C.coordinate[1]
        b2 = C.coordinate[0] - D.coordinate[0]
        c2 = a2*(C.coordinate[0]) + b2*(C.coordinate[1])

        determinant = a1*b2 - a2*b1

        if(determinant == 0):
            print("you tried to get intersection of parallel lines")
            return None
        else:
            x = (b2*c1 - b1*c2)/determinant
            y = (a1*c2 - a2*c1)/determinant
            return Point(x,y,0)
        
def get_outline(points):
    points = np.array([p.coordinate[:2] for p in points])
    def add_edge(edges, i, j):
        if (i, j) in edges or (j, i) in edges:
            assert (j, i) in edges, "Can't go twice over same directed edge right?"
            edges.remove((j, i))
            return
        edges.add((i, j))
    tri = Delaunay(points)
    edges = set()
    # Loop over triangles:
    # ia, ib, ic = indices of corner points of the triangle
    for ia, ib, ic in tri.simplices:
        pa = points[ia]
        pb = points[ib]
        pc = points[ic]

        a = np.sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
        b = np.sqrt((pb[0] - pc[0]) ** 2 + (pb[1] - pc[1]) ** 2)
        c = np.sqrt((pc[0] - pa[0]) ** 2 + (pc[1] - pa[1]) ** 2)
        s = (a + b + c) / 2.0
        area = np.sqrt(s * (s - a) * (s - b) * (s - c))
        circum_r = a * b * c / (4.0 * area)
        if circum_r < 8:
            add_edge(edges, ia, ib)
            add_edge(edges, ib, ic)
            add_edge(edges, ic, ia)
    
    start = next(iter(edges))
    outline_path = [start[0], start[1]]
    edges.remove(start)
    while 1:
        for edge in edges:
            if(edge[0] == outline_path[-1]):
                if(edge[1] == outline_path[0]):
                    return [Point(points[p][0], points[p][1]) for p in outline_path]
                outline_path.append(edge[1])


def get_distance(p1, p2):
    return np.linalg.norm(p1.coordinate[:2]-p2.coordinate[:2])
