from pyaxidraw import axidraw
#from .fake_axidraw import axidraw
import time
import os
import numpy as np
import asyncio


#draw canvas image using axidraw machine
class AxidrawController:
    def __init__(self, digital_image):
        ad = axidraw.AxiDraw() # Initialize class
        ad.interactive()            # Enter interactive mode
        connected = ad.connect()    # Open serial port to AxiDraw
        ad.options.units = 2
        ad.options.model = 2
        ad.options.speed_pendown = 30
        ad.options.speed_penup = 30
        #ad.options.pen_rate_lower = 90
        #ad.options.pen_rate_raise = 90
        ad.update()

        #ad.options.pen_pos_up = 70
        #ad.options.pen_pos_down = 50
        self.paused = False
        self.terminated = False
        self.digital_image = digital_image

        #this is for scheduling polylines. 
        #you can register polylines based on priority.
        #1,2, or 3. 
        self.polylines_priority = [[],[],[]]

        if connected:
            self.ad = ad
        else:
            exit(0)

    def register_polylines(self, polylines, priority=2):
        self.polylines_priority[priority]+=polylines
        
    def _draw_first_polyline(self):
        for polylines in self.polylines_priority:
            #if polylines is not empty
            if(polylines):
                self._draw_polyline(polylines[0])
                del polylines[0]
                return
        return

    def reset():
        self.digital_image.reset()
        self.ad.penup()
        self.ad.moveto(0,0)

    async def process(self):
        while not self.terminated:
            #give some space for other process
            await asyncio.sleep(0.1)

            if(self.paused):
                await asyncio.sleep(0.3)
            else:
                self._draw_first_polyline()
            
    def _draw_polyline(self, polyline):
        polyline_array = np.round(np.array([point.coordinate[:2] for point in polyline.path]), 3)
        if(len(polyline_array) == 1):
            #where it is a dot
            self.ad.moveto(polyline_array[0][0], polyline_array[0][1])
            self.ad.pendown()
            self.ad.penup()
        else:
            #where it is not a dot
            self.ad.draw_path(polyline_array)
        self.digital_image.draw_polylines([polyline])

    def terminate(self):
        self.digital_image.terminate()
        self.polylines_priority = [[],[],[]]
        self.terminated = True
        self.ad.moveto(0,0)
        self.ad.disconnect()


