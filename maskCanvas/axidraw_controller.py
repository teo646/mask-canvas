from pyaxidraw import axidraw
from .components import Point
import numpy as np
import cv2

def find_nearest_polyline(point, polylines):
    nearest_polyline = polylines[0]
    min_distance = get_squared_distance(nearest_polyline.path[0], point)

    for polyline in polylines:
        distance = get_squared_distance(polyline.path[0], point)
        if(distance == 0):
            return polyline
        if(min_distance > distance):
            nearest_polyline = polyline
            min_distance = distance

        distance = get_squared_distance(polyline.path[-1], point)
        if(distance == 0):
            polyline.path.reverse()
            return polyline
        if(min_distance > distance):
            polyline.path.reverse()
            nearest_polyline = polyline
            min_distance = distance

    return nearest_polyline


def get_squared_distance(point1, point2):
    return (point1.coordinate[0] - point2.coordinate[0])**2\
            + (point1.coordinate[1] - point2.coordinate[1])**2

def arrange_polylines(polylines):
    starting_polyline = find_nearest_polyline(Point(0,0), polylines)
    arranged_polylines = [starting_polyline]
    polylines.remove(starting_polyline)

    while len(polylines) != 0:
        current_point = arranged_polylines[-1].path[-1]
        next_polyline = find_nearest_polyline(current_point, polylines)
        arranged_polylines.append(next_polyline)
        polylines.remove(next_polyline)

    return arranged_polylines


def classify_polylines_by_pen(polylines):
    classified_polylines = {}
    for polyline in polylines:
        if(polyline.pen in classified_polylines.keys()):
            classified_polylines[polyline.pen].append(polyline)
        else:
            classified_polylines[polyline.pen] = [polyline]
    return classified_polylines

def plan_polylines(polylines):
    classified_polylines = classify_polylines_by_pen(polylines)

    for pen in classified_polylines:
        classified_polylines[pen] = arrange_polylines(classified_polylines[pen])

    return classified_polylines



class AxidrawController:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self, is_axidraw_drawing, is_digital_drawing, magnification=20):
        print("arranging lines ...")
        polylines = plan_polylines(self.canvas.polylines)
        print("arranging lines done")

        #setup axidraw
        if(is_axidraw_drawing):
            ad = axidraw.AxiDraw() # Initialize class
            ad.interactive()            # Enter interactive mode
            connected = ad.connect()    # Open serial port to AxiDraw
            
            if not connected:
                is_axidraw_drawing = False
            else:
                ad.options.units = 2              # set working units to mm.
                ad.options.pen_pos_up = 62        # select a large range for the pen up/down swing
                ad.options.pen_pos_down = 38
                ad.options.model = 2
                ad.update()


        #setup digital image
        if(is_digital_drawing):
            digital_image = np.tile(self.canvas.paper_color, (self.canvas.y*magnification, self.canvas.x*magnification, 1)).astype('uint8')
            cv2.namedWindow("digital_image", cv2.WINDOW_NORMAL)
            cv2.moveWindow("digital_image", 900, -900)
            cv2.setWindowProperty("digital_image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        #draw image
        for pen in polylines:
            if(is_axidraw_drawing):
                ad.goto(0, 0)
                print("equip ", pen.color, "on the axidraw")
                while 1:
                    input_ = str(input())
                    if(input_ == ""):
                        break

            for polyline in polylines[pen]:
                if(is_axidraw_drawing):
                    ad.draw_path([point.coordinate[:2] for point in polyline.path])     
                if(is_digital_drawing):
                    for p1, p2 in zip(polyline.path, polyline.path[1:]):
                        p1_cv2 = p1.as_numpy(magnification)
                        p2_cv2 = p2.as_numpy(magnification)
                        digital_image = cv2.line(digital_image, p1_cv2, p2_cv2, pen.color, int(pen.thickness*magnification))

                    cv2.imshow('digital_image',digital_image)
                    cv2.waitKey(1)
    

        #terminate process
        if(is_axidraw_drawing):
            ad.goto(0, 0)
            ad.disconnect()
        if(is_digital_drawing):
            cv2.waitKey(0)
            cv2.destroyAllWindows()

