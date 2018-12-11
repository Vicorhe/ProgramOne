from lucasKanadeTracker import lktrack
import cv2 as cv

imnames = ['/Users/victorhe/Desktop/corridor/bt.000.pgm', '/Users/victorhe/Desktop/corridor/bt.002.pgm',
           '/Users/victorhe/Desktop/corridor/bt.003.pgm', '/Users/victorhe/Desktop/corridor/bt.004.pgm']

lkt = lktrack.LKTracker(imnames)

lkt.detect_points()
lkt.draw()
for i in range(len(imnames)-1):
    lkt.track_points()
    lkt.draw()
    cv.waitKey(0)


cv.waitKey(0)
cv.destroyAllWindows()