import cv2



def showImage(image):
# Naming a window
    cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Resized_Window", 700, 700)
    cv2.imshow("Resized_Window", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


class KeyWrapper:
    def __init__(self, iterable, key):
        self.it = iterable
        self.key = key

    def __getitem__(self, i):
        return self.key(self.it[i])

    def __len__(self):
        return len(self.it)

def getYIntercept(slope, point):
    return point.y - slope*point.x


