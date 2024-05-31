from .plan_polylines import plan_polyline
from maskCanvas import Point, Polyline, Pen
from threading import Thread



command_info =
"""
Axidraw Controller Commands

-help: print this page

-draw: start drawing process.

-stop: pause drawing process. 
       do nothing if you haven't start drawing process.

-restart: restart drawing process.

-align: move plotter to every edges and dot to check if the
        pen is aligned collectly. 

-pen: move pen down and up once to check pen movement range

-quit: stop precess and exit program. use with care
"""




class UserInterface:

    def _find_match(str_object, objects):
        for _object in objects:
            if(str_object == str(_object)):
                return _object
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
                self.digital_image.draw_polylines(polylines)
                self.axidraw.register_polylines(polylines)


            elif(command=="draw some"):
                print(self.polylines.keys())
                drawing_detail = input("choose color and range from above(ex: [1,2,3] 1 20)").split()
                str_color = drawing_detail[0]
                color = _find_match(str_color, self.polylines.keys())

                if(color == None):
                    print("invalid color")
                    continue

                if(len(drawing_detail) == 3) and drawing_detail[2]<len(self.polylines[color])):
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
                    self.digital_image.draw_polylines(self.polylines[color][start:end])
                    self.axidraw.register_polylines(self.polylines[color][start:end])

            elif(command=="stop"):
                self.axidraw.paused = True

            elif(command=="start"):
                self.axidraw.paused = False

            elif(command="align"):
                polylines = [Polyline([Point(0,0)], Pen([0,0,0], 0)),
                            Polyline([Point(self.canvas.x,0)], Pen([0,0,0], 0)),
                            Polyline([Point(self.canvas.x,self.canvas.y)], Pen([0,0,0], 0)),
                            Polyline([Point(0,self.canvas.y)], Pen([0,0,0], 0))]
                self.axidraw.register_polylines(polylines, priority=1)

            elif(command="pen"):
                polylines = [Polyline([Point(0,0)], Pen([0,0,0], 0))]
                self.axidraw.register_polylines(polylines, priority=1)

            elif(command="quit"):
                self.digital_image.terminate()
                self.axidraw.terminate()
                exit()

            elif(command == 'help'):
                print(command_info)

            else:
                print("unkown command '",cammand,"'")
                print(command_info)

    def __init__(self, canvas):
        #canvas is drawing that you will draw.
        self.canvas = canvas

        print("arranging lines ...")
        self.polylines = plan_polylines(self.canvas.polylines)
        print("arranging lines done")

        axidraw = AxidrawController()
        digital_image = DigitalImage(self.canvas.paper_color, self.canvas.x, self.canvas.y)
        self._process()

