import cv2
import numpy as np

class DigitalImage:

    def __init__(self, paper_color, width, height, magnification = 10):
        self.paper_color = paper_color
        self.width = width
        self.height = height
        self.magnification = magnification
        self.digital_image = np.tile(self.paper_color, (self.height*self.magnification,\
                self.width*self.magnification, 1)).astype('uint8')
        cv2.namedWindow("digital_image", cv2.WINDOW_NORMAL)

    def register_magnification(self, magnification):
        self.digital_image = cv2.resize(self.digital_image, dsize=(self.width*magnification,\
                self.height*magnification), interpolation=cv2.INTER_LINEAR)
        self.magnification = magnification

    def reset_image(self):
        self.digital_image = np.tile(self.paper_color, (self.height*self.magnification,\
                self.width*self.magnification, 1)).astype('uint8')

    def draw_polylines(self, polylines):
        for polyline in polylines:
            polyline_array = np.array([point.coordinate[:2] for point in polyline.path],dtype=np.int32)*self.magnification
            self.digital_image = cv2.polylines(self.digital_image, [polyline_array], False, polyline.pen.color,\
                            int(polyline.pen.thickness*self.magnification))

    def show_polylines(self, polylines):
        digital_image = np.tile(self.paper_color, (self.height*self.magnification,\
                        self.width*self.magnification, 1)).astype('uint8')
        for polyline in polylines:
            polyline_array = np.array([point.coordinate[:2] for point in polyline.path],dtype=np.int32)*self.magnification
            digital_image = cv2.polylines(digital_image, [polyline_array], False, polyline.pen.color,\
                            int(polyline.pen.thickness*self.magnification))
        cv2.imshow('digital_image',digital_image)
        cv2.waitKey(100)

    def show_image(self):
        cv2.imshow('digital_image',self.digital_image)
        cv2.waitKey(100)

    def terminate(self):
        cv2.destroyAllWindows()

