class Region:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def is_overlaying(self, region):
        if(self.x_min<region.x_max and self.x_max>region.x_min and\
                self.y_min<region.y_max and self.y_max>region.y_min):
            return True
        else:
            return False
