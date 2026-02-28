import cv2
import uuid
import numpy as np
import asyncio

class DigitalImage:

    def __init__(self, paper_color, width, height, magnification = 10):
        self.id = str(uuid.uuid4())
        self.paper_color = paper_color
        self.width = width
        self.height = height
        self.magnification = magnification
        self.digital_image = np.tile(self.paper_color, (self.height*self.magnification,\
                self.width*self.magnification, 1)).astype('uint8')
        cv2.namedWindow(self.id, cv2.WINDOW_NORMAL)
        self.refresh

    def register_magnification(self, magnification):
        self.digital_image = cv2.resize(self.digital_image, dsize=(self.width*magnification,\
                self.height*magnification), interpolation=cv2.INTER_LINEAR)
        self.magnification = magnification

    def reset(self):
        self.digital_image = np.tile(self.paper_color, (self.height*self.magnification,\
                self.width*self.magnification, 1)).astype('uint8')

    def draw_polylines(self, polylines):
        for polyline in polylines:
            polyline_array = np.array([point.coordinate[:2] for point in polyline.path],dtype=np.int32)*self.magnification
            self.digital_image = cv2.polylines(self.digital_image, [polyline_array], False, polyline.pen.color,\
                            int(polyline.pen.thickness*self.magnification))
        self.refresh()

    def refresh(self):
        cv2.imshow(self.id,self.digital_image)
        cv2.waitKey(100)

    def terminate(self):
        cv2.destroyWindow(self.id)


