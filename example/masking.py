from maskCanvas import canvas, showImage

def main():
    c= canvas()
    mask_path = [[4,4],[7,10],[10,2],[15,17],[20,8],[20,26],[6,17]]
    for i in range(len(mask_path)):
        c.registerLineSeg([mask_path[i-1],mask_path[i]])
    c.registerMask(mask_path)

    c.registerLineSeg([[2,9],[38,7]])
    c.registerLineSeg([[4,4],[24,26]])
    c.registerLineSeg([[3,15],[24,26]])
    c.registerLineSeg([[4,16],[14,21]])
    showImage(c.draw(10))

if __name__ == "__main__":
    main()

