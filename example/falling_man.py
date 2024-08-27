from maskCanvas import Canvas, Polyline, Mask, Point, Arc, Graph, Regular_polygone
from maskCanvas import Pen, draw_linear_background, AxidrawInterface, ObjFile
from maskCanvas import dot_object, put_polylines_on_object, GridifiedObj
from math import cos, sin, pi, atan
from scipy.spatial import Delaunay
import math
import numpy as np
import random
from tqdm import tqdm
test = 0
if(test):
    grid_interval = 1
else:
    grid_interval = 0.2



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

def main():
    c= Canvas(200,200,0,frame=False, paper_color= (255,255,255))

    pen1 = Pen((0,0,0),0.2)
    pen2 = Pen((0,0,255),0.2)

    man = ObjFile("./obj/test.obj")
    man.edit()
    grid_man = GridifiedObj(man, grid_interval)
    grid_man.show()
    polylines = []
    for x in np.arange(man.range[0][0], man.range[0][1], 0.28):
        polylines.append(Polyline([Point(x, man.range[1][0]), Point(x, man.range[1][1])], pen1))

    polylines = put_polylines_on_object(polylines, grid_man)
    
    for polyline in polylines:
        #polyline.rotate(1, -pi/10)
        c.draw_polyline(polyline)

    outline_points = [polyline.path[index] for polyline in polylines for index in [0, -1]]
    arranged_points = alpha_shape(outline_points, 2)
    c.draw_polyline(Polyline(arranged_points, pen2))
    #c.register_mask(Mask(arranged_points))

    c.draw_polyline(Polyline([Point(0,0), Point(200,200)], pen1))

    c.show_bitmap(50)
    #ai = AxidrawInterface(c)

if __name__ == "__main__":
    main()
