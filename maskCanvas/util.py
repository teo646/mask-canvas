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

class KeyWrapper:
    def __init__(self, iterable, key):
        self.it = iterable
        self.key = key

    def __getitem__(self, i):
        return self.key(self.it[i])

    def __len__(self):
        return len(self.it)

    def insert(self, index, item):
        print('asked to insert %s at index%d' % (item, index))
        self.it.insert(index, {"time":item})


def alpha_shape(points, alpha, only_outer=True):
    """
    Compute the alpha shape (concave hull) of a set of points.
    :param points: np.array of shape (n,2) points.
    :param alpha: alpha value.
    :param only_outer: boolean value to specify if we keep only the outer border
    or also inner edges.
    :return: set of (i,j) pairs representing edges of the alpha-shape. (i,j) are
    the indices in the points array.
    """
    assert len(points) > 3, "Need at least four points"
    tri = Delaunay([point.coordinate[:2] for point in points])
    def add_edge(edges, i, j):
        """
        Add an edge between the i-th and j-th points,
        if not in the list already
        """
        if (i, j) in edges or (j, i) in edges:
            # already added
            assert (j, i) in edges, "Can't go twice over same directed edge right?"
            if only_outer:
                # if both neighboring triangles are in shape, it's not a boundary edge
                edges.remove((j, i))
            return
        edges.add((i, j))
    edges = set()
    # Loop over triangles:
    # ia, ib, ic = indices of corner points of the triangle
    for ia, ib, ic in tri.simplices:
        pa = points[ia]
        pb = points[ib]
        pc = points[ic]
        # Computing radius of triangle circumcircle
        # www.mathalino.com/reviewer/derivation-of-formulas/derivation-of-formula-for-radius-of-circumcircle
        a = np.linalg.norm(pa.coordinate[:2] - pb.coordinate[:2])
        b = np.linalg.norm(pb.coordinate[:2] - pc.coordinate[:2])
        c = np.linalg.norm(pc.coordinate[:2] - pa.coordinate[:2])
        s = (a + b + c) / 2.0
        area = np.sqrt(s * (s - a) * (s - b) * (s - c))
        circum_r = a * b * c / (4.0 * area)
        if circum_r < alpha:
            add_edge(edges, pa, pb)
            add_edge(edges, pb, pc)
            add_edge(edges, pc, pa)

    edges_dict = {}
    for edge in edges:
        edges_dict[edge[0]] = edge[1]
    edges_path = [list(edges)[0][0]]
    while len(edges_path) < len(edges_dict):
        edges_path.append(edges_dict[edges_path[-1]])
        # if empty
        if(not edges_dict):
            break

    return edges_path


