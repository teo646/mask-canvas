from maskCanvas import canvas, showImage, line_segment, reverse_mask
colors = [ (0, 0, 255),  (0, 255, 0),  (255, 0, 0),  (0, 255, 255),  (255, 0, 255)]
def main():
    c= canvas()
    mask1_path = [[4,4],[7,10],[10,2],[15,7],[20,8],[20,26],[6,17]]
    mask2_path = [[22,22],[25,22],[25,28],[22,28]]
    for i in range(len(mask1_path)):
        c.drawLineSegment([mask1_path[i-1],mask1_path[i]])
    c.registerMask(mask1_path)



    c.drawLineSegment([[4,4],[24,26]])
    c.drawLineSegment(line_segment([[30,15],[32,26]],color = colors[3]))
    c.drawLineSegment(line_segment([[3,15],[24,26]],color = colors[2]))
    c.drawLineSegment(line_segment([[7,1],[7,13]],color = colors[4]))
    c.drawLineSegment(line_segment([[12,1],[12,4]],color = colors[4]))
    c.show(10)

if __name__ == "__main__":
    main()

