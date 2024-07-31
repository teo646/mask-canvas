import numpy as np
from perlin_noise import PerlinNoise
from .object import Object
'''
def noise_polylines(polylines, scale=0.1, amplitude=2):
    polylines_after_noise = []
    perlin_noise = PerlinNoise()

    for polyline in polylines:
        path = []
        for p1, p2 in zip(polyline.path, polyline.path[1:]):
            length=get_distance(p1, p2)
            num_interval=int(length*30)
            dx=(p2.coordinate[0]-p1.coordinate[0])
            dy=(p2.coordinate[1]-p1.coordinate[1])
            sin_theta=dy/length
            cos_theta=dx/length
            for index in range(num_interval):
                x = p1.coordinate[0]+index*dx/num_interval
                y = p1.coordinate[1]+index*dy/num_interval
                noise = amplitude*perlin_noise([x*scale,y*scale])
                path.append(Point(x+noise*sin_theta,y-noise*cos_theta))
        polylines_after_noise.append(Polyline(path, polyline.pen, fill=polyline.fill))


    return Polylines_after_noise



def noise_polyline(polyline, scale=0.1, amplitude=2):
    return noise_polylines([polyline], scale, amplitude)[0]
'''
class Perlin(Object):
    def __init__(self, amplitude=1):
        self.perlin_noise = PerlinNoise(seed=1)
        self.amplitude = amplitude

    def get_z(self, point):
        x = point.coordinate[0]
        y = point.coordinate[1]
        return self.perlin_noise([x*self.amplitude, y*self.amplitude])

    def scale(self, amplitude):
        self.amplitude = self.amplitude*amplitude

    def rotate(self, axis, radian):
        print("perlin does not support rotation")





