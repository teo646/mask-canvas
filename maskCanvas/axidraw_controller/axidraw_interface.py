from .plan_polylines import plan_polylines
from maskCanvas import Point, Polyline, Pen
from .axidraw_controller import AxidrawController
from .digital_image import DigitalImage
import asyncio
import aioconsole



command_info ="""
Axidraw Controller Commands--------------------------------------
                                                                |
-help: print this page                                          |
                                                                |
-draw: Draw the lines on canvas.                                |
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

    async def _interact(self):

        async def _choose_pen():
            print("Select the pen from below: ")
            pens = [pen for pen in self.polylines.keys()]
            for index, pen in enumerate(pens):
                print("%d: (%s, %s)" %(index, str(pen.color), str(pen.thickness)))
            pen_index = int(await aioconsole.ainput(':'))
            if(pen_index < 0 or pen_index >= len(self.polylines.keys())):
                print("invalid index")
                return None
            else:
                return pens[pen_index]

        async def _index_polylines(polylines):
            print("The last index of polylines is %d" %(len(polylines)-1))
            from_ = int(await aioconsole.ainput('Starting index: '))
            to_ = int(await aioconsole.ainput('Last index: '))
            try:
                indexed_polylines = polylines[from_:to_+1]
            except:
                print("invalid indexing")
                indexed_polylines = []
            return indexed_polylines

        print(command_info)
        while 1:
            command = await aioconsole.ainput()
            if(command=="magnification"):
                digital_image_magnification = int(input("Enter digital image magnification:"))
                self.digital_image.register_magnification(digital_image_magnification)
                self.digital_image.refresh()

            elif(command=="draw"):
                pen = await _choose_pen()
                if(pen):
                    polylines = self.polylines[pen]
                    polylines = await _index_polylines(polylines)
                    #if no polylines to draw(empty)
                    if(not polylines):
                        continue
                else:
                    continue

                tmp_digital_image = DigitalImage(self.canvas.paper_color, self.canvas.x, self.canvas.y)
                tmp_digital_image.draw_polylines(polylines)
                tmp_digital_image.refresh()

                draw_or_not = await aioconsole.ainput("do you want to draw?(y/n): ")
                tmp_digital_image.terminate()

                if(draw_or_not == "y"):
                    self.axidraw_controller.register_polylines(polylines)

            elif(command=="stop"):
                self.axidraw_controller.paused = True

            elif(command=="start"):
                self.axidraw_controller.paused = False

            elif(command=="align"):
                polylines = [Polyline([Point(0,0)], Pen([0,0,0], 0)),
                            Polyline([Point(self.canvas.x,0)], Pen([0,0,0], 0)),
                            Polyline([Point(self.canvas.x,self.canvas.y)], Pen([0,0,0], 0)),
                            Polyline([Point(0,self.canvas.y)], Pen([0,0,0], 0))]
                self.axidraw_controller.register_polylines(polylines, priority=1)

            elif(command=="pen"):
                polylines = [Polyline([Point(0,0)], Pen([0,0,0], 0))]
                self.axidraw_controller.register_polylines(polylines, priority=1)

            elif(command=="quit"):
                self.axidraw_controller.terminate()
                return 

            elif(command=="reset"):
                self.axidraw_controller.reset()

            elif(command == 'help'):
                print(command_info)

            else:
                print("unkown command '",command,"'")
                print(command_info)

    def __init__(self, canvas):
        #canvas is drawing that you will draw.
        self.canvas = canvas
        digital_image = DigitalImage(self.canvas.paper_color, self.canvas.x, self.canvas.y)
        self.axidraw_controller = AxidrawController(digital_image)

        print("arranging lines ...")
        self.polylines = plan_polylines(self.canvas.polylines)
        print("arranging lines done")
        asyncio.run(self._process())


    async def _process(self):
        async with asyncio.TaskGroup() as tg:
            axidraw = tg.create_task(self.axidraw_controller.process())
            interface = tg.create_task(self._interact())



