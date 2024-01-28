from maskCanvas import canvas, showImage


c= canvas
c.registerMask([[4,4],[7,10],[10,2],[15,17],[20,8],[20,26],[6,17]])
c.registerLineSeg([[2,9],[38,7]])
showImage(c.draw(10))


