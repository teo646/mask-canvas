from .plan_polylines import plan_polylines
from maskCanvas import Point, Polyline, Pen
from .axidraw_controller import AxidrawController
from .digital_image import DigitalImage



command_info ="""
Axidraw Controller Commands--------------------------------------
                                                                |
-help: print this page                                          |
                                                                |
-draw all: Draw all of the lines on canvas.                     |
                                                                |
-draw some: Draw some of the lines on canvas.                   |
                                                                |
-stop: pause drawing process.                                   |
       do nothing if you haven't start drawing process.         |     
                                                                |
-start: restart drawing process.                                |
                                                                |
-align: move plotter to every edges and dot to check if the     |
        pen is aligned collectly.                               |
                                                                |
-pen: move pen down and up once to check pen movement range     |
                                                                |
-quit: stop precess and exit program. use with care             |
-----------------------------------------------------------------
"""




class AxidrawInterface:

    @staticmethod
    def _find_matching_pen(target_pen, pens):
        for pen in pens:
            if(target_pen == (str(pen.color)).replace(" ", "")):
                return pen
        return None

    def _process(self):
        print(command_info)
        while 1:
            command = input()
            if(command=="magnification"):
                digital_image_magnification = int(input("Enter digital image magnification:"))
                self.digital_image.register_magnification(digital_image_magnification)

            elif(command=="draw all"):
                polylines = [j for sub in self.polylines.values() for j in sub]
                self.axidraw.register_polylines(polylines)

            elif(command=="draw some"):
                print([pen.color for pen in self.polylines.keys()])
                drawing_detail = input("choose color and range from above(ex: (1,2,3) 1 20)").split()
                str_color = drawing_detail[0]
                color = self._find_matching_pen(str_color, self.polylines.keys())

                if(color == None):
                    print("invalid color")
                    continue

                if(len(drawing_detail) == 3 and drawing_detail[2]<len(self.polylines[color])):
                    start = drawing_detail[1]
                    end = drawing_detail[2]
                elif(len(drawing_detail) == 3):
                    start = drawing_detail[1]
                    end = len(self.polylines[color])
                else:
                    start = 0
                    end = len(self.polylines[color])

                self.digital_image.show_polylines(self.polylines[color][start:end])

                draw_or_not = input("do you want to draw?(y/n)")
                if(draw_or_not == "y"):
                    self.axidraw.register_polylines(self.polylines[color][start:end])

            elif(command=="stop"):
                self.axidraw.paused = True

            elif(command=="start"):
                self.axidraw.paused = False

            elif(command=="align"):
                polylines = [Polyline([Point(0,0)], Pen([0,0,0], 0)),
                            Polyline([Point(self.canvas.x,0)], Pen([0,0,0], 0)),
                            Polyline([Point(self.canvas.x,self.canvas.y)], Pen([0,0,0], 0)),
                            Polyline([Point(0,self.canvas.y)], Pen([0,0,0], 0))]
                self.axidraw.register_polylines(polylines, priority=1)

            elif(command=="pen"):
                polylines = [Polyline([Point(0,0)], Pen([0,0,0], 0))]
                self.axidraw.register_polylines(polylines, priority=1)

            elif(command=="quit"):
                self.axidraw.terminate()
                self.digital_image.terminate()
                exit()

            elif(command == 'help'):
                print(command_info)

            else:
                print("unkown command '",command,"'")
                print(command_info)

    def __init__(self, canvas):
        #canvas is drawing that you will draw.
        self.canvas = canvas
        self.axidraw = AxidrawController()
        self.digital_image = DigitalImage(self.canvas.paper_color, self.canvas.x, self.canvas.y)
        self.axidraw.set_digital_image(self.digital_image)

        print("arranging lines ...")
        self.polylines = plan_polylines(self.canvas.polylines)
        print("arranging lines done")

        self._process()

