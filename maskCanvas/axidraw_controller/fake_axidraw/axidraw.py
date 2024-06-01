import time

class AxiDraw:
    def __init__(self):
        print("axidraw init")

    def interactive(self):
        pass

    def connect(self):
        print("connected to axidraw")
        return True

    def load_config(self, file_path):
        pass

    def draw_path(self, path):
        print("axidraw drawing path:")
        print(path)
        time.sleep(3)


    def moveto(self, x, y):
        print("axidraw moving")
        print(x, y)
        time.sleep(3)

    def disconnect(self):
        print("axidraw disconnected")
