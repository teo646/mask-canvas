#from pyaxidraw import axidraw
from .fake_axidraw import axidraw
import time
import os
import numpy as np
from threading import Thread


#draw canvas image using axidraw machine
class AxidrawController:
    def __init__(self):
        ad = axidraw.AxiDraw() # Initialize class
        ad.interactive()            # Enter interactive mode
        connected = ad.connect()    # Open serial port to AxiDraw
        ad.load_config(os.path.join(os.path.dirname(__file__),"axidraw_conf_copy.py"))
        self.paused = False
        self.terminated = False
        self.digital_image = None

        #this is for scheduling polylines. 
        #you can register polylines based on priority.
        #1,2, or 3. 
        self.polylines_priority = [[],[],[]]

        if connected:
            self.ad = ad
            drawing_thread = Thread(target = self.process, args = [])
            drawing_thread.start()
        else:
            exit(0)
    
    def set_digital_image(self, digital_image):
        self.digital_image = digital_image

    def register_polylines(self, polylines, priority=2):
        self.polylines_priority[priority]+=polylines
        
    def _draw_first(self, polylines):
        if(len(polylines)==0):
            return False
        else:
            self._draw_polyline(polylines[0])
            if(self.digital_image):
                self.digital_image.draw_polylines(polylines[0])
            del polylines[0]
            if(len(self.polylines_priority[0])==0 and \
                    len(self.polylines_priority[1])==0 and\
                    len(self.polylines_priority[2])==0):
                print("nothing more to draw")
            return True

    def process(self):
        while (not self.terminated):
            while(self.paused):
                time.sleep(0.3)
            for polylines in self.polylines_priority:
                drawn = self._draw_first(polylines)
                if(drawn):
                    break
        print("terminated")

    def _draw_polyline(self, polyline):
        polyline_array = np.array([point.coordinate[:2] for point in polyline.path],dtype=np.int32)
        self.ad.draw_path(polyline_array)

    def terminate(self):
        self.polylines_priority = [[],[],[]]
        self.terminated = True
        self.ad.moveto(0,0)
        self.ad.disconnect()
        exit(0)


