from pyaxidraw import axidraw

#draw canvas image using axidraw machine
class AxidrawController:
    def __init__(self):
        ad = axidraw.AxiDraw() # Initialize class
        ad.interactive()            # Enter interactive mode
        connected = ad.connect()    # Open serial port to AxiDraw
        ad.load_config(os.path.join(os.path.dirname(__file__),"axidraw_conf_copy.py"))
        self.paused = False

        #this is for scheduling polylines. 
        #you can register polylines based on priority.
        #1,2, or 3. 
        self.polylines_priority = [[],[],[]]

        if connected:
            self.ad = ad
            drawing_thread = Thread(target = self.process, args = []])
            drawing_thread.start()
        else:
            exit(0)
       
    def register_polylines(self, polylines, priority=2):
        self.registered_polylines[priority]+=polylines

    def process(self):
        while 1:
            while(self.paused):
                time.sleep(0.3)
            for polylines in self.polylines_priority:
                for polyline in polylines:
                    self._draw_polyline(polyline)
                    break
                break
            try:
                del polyline

    def _draw_polyline(self, polyline)
        polyline_array = np.array([point.coordinate[:2] for point in polyline.path],dtype=np.int32)
        self.ad.draw_path(polyline_array)

    def terminate(self):
        self.polylines_priority = [[],[],[]]
        self.ad.moveto(0,0)
        self.ad.disconnect()


