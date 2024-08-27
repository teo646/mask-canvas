from maskCanvas import Point
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin
from math import ceil, floor
from tqdm import tqdm
import random
matplotlib.use('TkAgg')

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
        self.vertices, self.faces = self._read_obj_from_path(file_path)
        self.range = [None, None, None]
        self._update_range()
        self.last_searched_face = self.faces[0]

        super().__init__()

    def _update_range(self):
        x_values = [point.coordinate[0] for point in self.vertices]
        y_values = [point.coordinate[1] for point in self.vertices]
        z_values = [point.coordinate[2] for point in self.vertices]
        self.range[0] = [min(x_values), max(x_values)]
        self.range[1] = [min(y_values), max(y_values)]
        self.range[2] = [min(z_values), max(z_values)]

    def _read_obj_from_path(self, file_path):
        try:
            vertices = []
            faces = []
            with open(file_path) as f:
                for line in tqdm(f, desc="reading "+file_path):
                    if line[:2] == "v ":
                        xyz = list(map(float, line[2:].strip().split()))
                        vertices.append(Point(xyz[0], xyz[1], xyz[2]))
                    elif line[0] == "f":
                        vertices_strings = line[2:].strip().split()
                        face = [vertices[int(chunk.split('/')[0])-1] for chunk in vertices_strings[:3]]
                        faces.append(face)
                        if(len(vertices_strings) == 4):
                            face = [vertices[int(chunk.split('/')[0])-1] for chunk in vertices_strings[2:]+[vertices_strings[0]]]
                            faces.append(face)

        except FileNotFoundError:
            print(f"{file_path} not found.")
        except Exception as e:
            print(e)
            print("An error occurred while loading the shape.")
        self.file_path = file_path
        return vertices, faces

    '''
    def add_object_file(self, obj):
        self.vertices += obj.vertices
        self.faces += obj.faces
        self._update_range()
    '''


    def get_front_faces(self):
        faces = []
        for face in tqdm(self.faces, desc = "getting front faces"):
            v1 = face[1].coordinate[:2] - face[0].coordinate[:2]
            v2 = face[2].coordinate[:2] - face[0].coordinate[:2]
            det = np.linalg.det(np.array([v1,v2]))
            if(det > 0):
                faces.append(face)
        return faces

    def scale(self, axis, amplitude):
        scale_mat = np.identity(4)
        scale_mat[axis] *= amplitude
        for point in tqdm(self.vertices, desc="scaling"):
            point.coordinate = np.matmul(scale_mat,point.coordinate)
        self._update_range()

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
        for point in tqdm(self.vertices, desc="rotating"):
            point.coordinate = np.matmul(rotate_mat,point.coordinate)
        self._update_range()

    def move(self, axis, delta):
        for point in tqdm(self.vertices, desc="moving"):
            point.coordinate[axis] += delta
        self._update_range()

    def center(self, axis, value):
        self.move(axis, value-(self.range[axis][1]+self.range[axis][0])/2)

    def squeeze(self, axis, val_min, val_max):
        self.scale(axis, (val_max-val_min)/(self.range[axis][1]-self.range[axis][0]))
        self.center(axis, (val_min+val_max)/2)

    def slice(self, axis, min_):
        faces = []
        for face in tqdm(self.faces, desc="slicing faces"):
            if(all([True if point.coordinate[axis] > min_ else False for point in face])):
                faces.append(face)
        self.faces = faces

        vertices = []
        for point in tqdm(self.vertices, desc="slicing vertices"):
            if point.coordinate[axis] > min_:
                vertices.append(point)
        self.vertices = vertices
        self.range[axis][0] = min_

    def show(self):
        plt.close('all')
        MAX_VERTICES = 300
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        if(len(self.vertices) > MAX_VERTICES):
            vertices_to_show = random.sample(self.vertices, MAX_VERTICES)
        else:
            vertices_to_show = self.vertices

        x_values = [vertice.coordinate[0] for vertice in vertices_to_show]
        y_values = [vertice.coordinate[1] for vertice in vertices_to_show]
        z_values = [vertice.coordinate[2] for vertice in vertices_to_show]

        ax.scatter(x_values, y_values, z_values, marker='o')

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        plt.gca().invert_yaxis()
        plt.show()

    def edit(self):
        self.show()
        while 1:
            command = input("command: ")
            if(command == "q"):
                break
            elif(command == "m"):
                axis = int(input("axis: "))
                delta = float(input("delta: "))
                self.move(axis, delta)
                self.show()
            elif(command == "r"):
                axis = int(input("axis: "))
                angle = float(input("angle(degree): "))
                #degree to radian
                angle *= 0.0174533
                self.rotate(axis, angle)
                self.show()
            elif(command == "s"):
                axis = int(input("axis: "))
                ratio = float(input("ratio: "))
                self.scale(axis, ratio)
                self.show()
            #save
            elif(command == "save"):
                file_path = input("file path: ")
                if(file_path == ""):
                    file_path = self.file_path
                f = open(file_path, 'w')
                index_recorder = {}
                for index, vertice in enumerate(self.vertices):
                    f.write("v %f %f %f\n" %tuple(vertice.coordinate[:3]))
                    index_recorder[vertice] = index+1
                f.write("\n")
                for face in self.faces:
                    f.write("f %d %d %d\n" %tuple([index_recorder[vertice] for vertice in face]))
                f.close
                print(len(self.faces))

            else:
                print("invalid command!")

                

class GridifiedObj:
    def __init__(self, obj, interval):
        self.range = obj.range
        self.interval = interval
        num_x = ceil((self.range[0][1]-self.range[0][0])/interval)+1
        num_y = ceil((self.range[1][1]-self.range[1][0])/interval)+1
        self.grid = np.full((num_x, num_y), -1, dtype="float")

        for face in tqdm(obj.get_front_faces(), desc="gridifying"):
            x_values = [point.coordinate[0] for point in face]
            y_values = [point.coordinate[1] for point in face]
            x_min_index = floor((min(x_values)-self.range[0][0])/interval)
            x_max_index = ceil((max(x_values)-self.range[0][0])/interval)
            y_min_index = floor((min(y_values)-self.range[1][0])/interval)
            y_max_index = ceil((max(y_values)-self.range[1][0])/interval)
            for x_index in range(x_min_index, x_max_index):
                x = x_index*self.interval+self.range[0][0]
                for y_index in range(y_min_index, y_max_index):
                    y = y_index*self.interval+self.range[1][0]
                    if(self._is_point_in_face(face, x, y)):
                        z = self._get_z_on_face(face, x, y)
                    else:
                        continue
                    if(z > self.grid[x_index][y_index]):
                        self.grid[x_index][y_index] = z
    def show(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        x_values = [self.range[0][0] + index*self.interval for index in range(len(self.grid)) for col in self.grid[0]]
        y_values = [self.range[1][0] + index*self.interval for z in self.grid for index in range(len(self.grid[0]))]
        z_values = self.grid.flatten()

        ax.scatter(x_values, y_values, z_values, marker='o')

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        plt.show()

    def get_z(self, x, y):
        #Out of area
        if(x < self.range[0][0] or x > self.range[0][1] or
                y < self.range[1][0] or y > self.range[1][1]):
            return 0

        x_index = (x-self.range[0][0])/self.interval
        y_index = (y-self.range[1][0])/self.interval
        x_ratio = x_index-floor(x_index)
        y_ratio = y_index-floor(y_index)

        #if one of the grid value is 0, return None
        for low in self.grid[floor(x_index):floor(x_index)+2]:
            if(low[floor(y_index)] == -1 or low[floor(y_index)+1] == -1):
                return None
        return (self.grid[ceil(x_index)][ceil(y_index)]*x_ratio+\
                self.grid[floor(x_index)][ceil(y_index)]*(1-x_ratio))*y_ratio\
                + (self.grid[ceil(x_index)][floor(y_index)]*x_ratio+\
                self.grid[floor(x_index)][floor(y_index)]*(1-x_ratio))*(1-y_ratio)

    def _is_point_in_face(self, face, x, y):
        A = face[0].coordinate
        B = face[1].coordinate
        C = face[2].coordinate
        P = np.array([x,y])

        denominator = ((B[1] - C[1]) * (A[0] - C[0]) +
                   (C[0] - B[0]) * (A[1] - C[1]))

        if(denominator < 0.001):
            return False

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
