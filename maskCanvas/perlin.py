import numpy as np
from perlin_noise import PerlinNoise
import random
from .components import Point
from .polyline import Polyline
from .util import get_distance

def noise_polyline(polyline, scale=0.1, amplitude=2):
    
    path = []
    perlin_noise = PerlinNoise()
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


    return Polyline(path, polyline.pen, fill=polyline.fill)

