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
        cv2.moveWindow("digital_image", 900, -900)

    def register_magnification(self, magnification):
        self.magnification = magnification

    def reset_image(self):
        self.digital_image = np.tile(self.paper_color, (self.height*self.magnification,\
                self.width*self.magnification, 1)).astype('uint8')

    def draw_polylines(self, polylines, image = None):
        if(image==None):
            image = self.digital_image
        for polyline in polylines:
            polyline_array = np.array([point.coordinate[:2] for point in polyline.path],dtype=np.int32)*self.magnification
            image = cv2.polylines(image, [polyline_array], False, polyline.pen.color,\
                            int(polyline.pen.thickness*self.magnification))

        return image

    def show_polylines(self, polylines):
        digital_image = np.tile(self.paper_color, (self.height*self.magnification,\
                        self.width*self.magnification, 1)).astype('uint8')
        digital_image=self.draw_polylines(polylines, image=digitial_image)
        self.show_image(image=digital_image)
        

    def show_image(self, image=None):
        if(image==None):
            image=self.digital_image
        cv2.imshow('digital_image',self.digital_image)
        cv2.waitKey(0)

    def terminate(self):
        cv2.destroyAllWindows()





