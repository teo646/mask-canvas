import random
from maskCanvas import Point, Polyline
#this function will attempt to draw 'num_dot' dots at random points
#it will draw only when random value is bigger than z value of object at the point.
def dot_object(canvas, obj, num_dot, pen):
    for i in range(num_dot):
        print("working on point number ", i)
        random_x = random.uniform(0, canvas.x)
        random_y = random.uniform(0, canvas.y)
        random_threshold = random.uniform(-0.4, 0.4)
        if(random_threshold < obj.get_z(Point(random_x, random_y))):
            canvas.draw_polyline(Polyline([Point(random_x, random_y), Point(random_x, random_y+0.1)], pen))

    
    
