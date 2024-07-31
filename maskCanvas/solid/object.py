from maskCanvas import Point
import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin
from math import ceil, floor

class Object:
    def __init__(self):
        pass

    def get_z(self, point):
        return 0

    def scale(self, amplitude):
        pass

    #axis
    #0:x
    #1:y
    #2:z
    def rotate(self, axis, radian):
        pass

class ObjFile(Object):
    def __init__(self, file_path):
        self.set = False
        self.vertices, self.faces = self._read_obj_from_path(file_path)
        self.range = [None, None, None]
        self._update_min_max()
        self.last_searched_face = self.faces[0]

        super().__init__()

    #This function should be called after every rotations and movements.
    #interval can be used to define the distance between grids
    def setup(self, interval=0.5):
        self.back_space_cull()
        self.interval = interval
        self.grid = np.zeros((ceil((self.range[0][1]-self.range[0][0])/interval)+1,\
                ceil((self.range[1][1]-self.range[1][0])/interval)+1), dtype="float")\

        for face in self.faces:
            x_values = [point.coordinate[0] for point in face]
            y_values = [point.coordinate[1] for point in face]
            x_min_index = floor((min(x_values)-self.range[0][0])/interval)
            x_max_index = ceil((max(x_values)-self.range[0][0])/interval)
            y_min_index = floor((min(y_values)-self.range[1][0])/interval)
            y_max_index = ceil((max(y_values)-self.range[1][0])/interval)
            for x_index in range(x_min_index, x_max_index):
                x = x_index*interval+self.range[0][0]
                for y_index in range(y_min_index, y_max_index):
                    y = y_index*interval+self.range[1][0]
                    if(self._is_point_in_face(face, x, y)):
                        z = self._get_z_on_face(face, x, y)
                    else:
                        continue
                    if(z > self.grid[x_index][y_index]):
                        self.grid[x_index][y_index] = z
            self.set = True
        
    def _update_min_max(self):
        x_values = [point.coordinate[0] for point in self.vertices]
        y_values = [point.coordinate[1] for point in self.vertices]
        z_values = [point.coordinate[2] for point in self.vertices]
        self.range[0] = [min(x_values), max(x_values)]
        self.range[1] = [min(y_values), max(y_values)]
        self.range[2] = [min(z_values), max(z_values)]


    def get_z(self, x, y):
        if(not self.set):
            print("the object is not made into grid.")
            return 0
        #Out of area
        if(x < self.range[0][0] or x > self.range[0][1] or
                y < self.range[1][0] or y > self.range[1][1]):
            return 0

        x_index = (x-self.range[0][0])/self.interval
        y_index = (y-self.range[1][0])/self.interval
        x_ratio = x_index-floor(x_index)
        y_ratio = y_index-floor(y_index)
        return (self.grid[ceil(x_index)][ceil(y_index)]*x_ratio+\
                self.grid[floor(x_index)][ceil(y_index)]*(1-x_ratio))*y_ratio\
                + (self.grid[ceil(x_index)][floor(y_index)]*x_ratio+\
                self.grid[floor(x_index)][floor(y_index)]*(1-x_ratio))*(1-y_ratio)

    def get_xy_distance(self, point1, point2):
        return np.linalg.norm(point1.coordinate[:2]-point2.coordinate[:2])

    def _is_point_in_face(self, face, x, y):
        A = face[0].coordinate
        B = face[1].coordinate
        C = face[2].coordinate
        P = np.array([x,y])

        denominator = ((B[1] - C[1]) * (A[0] - C[0]) +
                   (C[0] - B[0]) * (A[1] - C[1]))
        a = ((B[1] - C[1]) * (P[0] - C[0]) +
             (C[0] - B[0]) * (P[1] - C[1])) / denominator
    
        if a >= 0:
            b = ((C[1] - A[1]) * (P[0] - C[0]) +
                (A[0] - C[0]) * (P[1] - C[1])) / denominator
            if b >= 0:
                c = 1 - a - b
                if c >= 0:
                    return True

        return False

    def _get_z_on_face(self, face, x, y):
        point_on_plane= face[0].coordinate[:3]
        v1 = face[1].coordinate[:3] - face[0].coordinate[:3]
        v2 = face[2].coordinate[:3] - face[0].coordinate[:3]
        normal_vect = np.cross(v1, v2)
        return (np.dot(normal_vect, point_on_plane)-np.dot(normal_vect[:2], np.array([x,y])))/normal_vect[2]

    def _read_obj_from_path(self, file_path):
        try:
            vertices = []
            faces = []
            with open(file_path) as f:
                for line in f:
                    if line[:2] == "v ":
                        xyz = list(map(float, line[2:].strip().split()))
                        vertices.append(Point(xyz[0], xyz[1], xyz[2]))
                    elif line[0] == "f":
                        face = [vertices[int(chunk.split('/')[0])-1] for chunk in line[2:].strip().split()]
                        faces.append(face)

        except FileNotFoundError:
            print(f"{file_path} not found.")
        except Exception as e:
            print(e)
            print("An error occurred while loading the shape.")
        
        return vertices, faces


    def back_space_cull(self):
        faces = []
        for face in self.faces:
            v1 = face[1].coordinate[:2] - face[0].coordinate[:2]
            v2 = face[2].coordinate[:2] - face[0].coordinate[:2]
            det = np.linalg.det(np.array([v1,v2]))
            if(det > 0):
                faces.append(face)
        self.faces = faces

    def scale(self, axis, amplitude):
        scale_mat = np.identity(4)
        scale_mat[axis] *= amplitude
        for point in self.vertices:
            point.coordinate = np.matmul(scale_mat,point.coordinate)
        self._update_min_max()

    def rotate(self, axis, radian):
        if(axis == 0):
            rotate_mat = np.array([[1, 0, 0, 0],
                                   [0, cos(radian), -sin(radian), 0],
                                   [0, sin(radian), cos(radian), 0],
                                   [0, 0, 0, 1]])
        elif(axis == 1):
            rotate_mat = np.array([[cos(radian), 0, sin(radian), 0],
                                   [0, 1, 0, 0],
                                   [-sin(radian), 0, cos(radian), 0],
                                   [0, 0, 0, 1]])
        else:
            rotate_mat = np.array([[cos(radian), -sin(radian), 0, 0],
                                   [sin(radian), cos(radian), 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1]])
        for point in self.vertices:
            point.coordinate = np.matmul(rotate_mat,point.coordinate)
        self._update_min_max()

    def move(self, axis, delta):
        for point in self.vertices:
            point.coordinate[axis] += delta
        self._update_min_max()

    def center(self, axis, value):
        self.move(axis, value-(self.range[axis][1]+self.range[axis][0])/2)

    def squeeze(self, axis, val_min, val_max):
        self.scale(axis, (val_max-val_min)/(self.range[axis][1]-self.range[axis][0]))
        self.center(axis, (val_min+val_max)/2)

    def slice(self, axis, min_):
        faces = []
        for face in self.faces:
            if(all([True if point.coordinate[axis] > min_ else False for point in face])):
                faces.append(face)
        self.faces = faces

        vertices = []
        for point in self.vertices:
            if point.coordinate[axis] > min_:
                vertices.append(point)
        self.vertices = vertices

    def show(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        if(not self.set):
            x_values = [vertice.coordinate[0] for vertice in self.vertices]
            y_values = [vertice.coordinate[1] for vertice in self.vertices]
            z_values = [vertice.coordinate[2] for vertice in self.vertices]
        else:
            x_values = [self.range[0][0] + index*self.interval for index in range(len(self.grid)) for col in self.grid[0]]
            y_values = [self.range[1][0] + index*self.interval for z in self.grid for index in range(len(self.grid[0]))]
            z_values = self.grid.flatten()
        ax.scatter(x_values, y_values, z_values, marker='o')

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        plt.show()
