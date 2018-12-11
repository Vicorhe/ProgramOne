import cv2 as cv

cap_1 = cv.VideoCapture('/Users/victorhe/Pictures/factorySampleCollection/videoClips/clip_1.mp4')
cap_2 = cv.VideoCapture('/Users/victorhe/Pictures/factorySampleCollection/videoClips/clip_2.mp4')
cap_3 = cv.VideoCapture('/Users/victorhe/Pictures/factorySampleCollection/videoClips/clip_3.mp4')
cap_4 = cv.VideoCapture('/Users/victorhe/Pictures/factorySampleCollection/videoClips/clip_4.mp4')
cap_5 = cv.VideoCapture('/Users/victorhe/Pictures/factorySampleCollection/videoClips/clip_5.mp4')

# contender for best overall
# fgbg = cv.createBackgroundSubtractorKNN(history=10, dist2Threshold=1000, detectShadows=False)

# ok
# fgbg = cv.bgsegm.createBackgroundSubtractorMOG(backgroundRatio=0.1, noiseSigma=40, nmixtures=3, history=30)

# best results over all
fgbg = cv.createBackgroundSubtractorMOG2(history=10, varThreshold=1000,  detectShadows=False)

# slow, wacky to play around with
# kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
# fgbg = cv.bgsegm.createBackgroundSubtractorGMG(initializationFrames=10, decisionThreshold=0.95)

# doesn't handle shaking well, speed ok
# fgbg = cv.bgsegm.createBackgroundSubtractorCNT(minPixelStability=1, useHistory=True)

# too slow
# fgbg = cv.bgsegm.createBackgroundSubtractorGSOC()

# too slow
# fgbg = cv.bgsegm.createBackgroundSubtractorLSBP()


cv.namedWindow('frame', cv.WINDOW_NORMAL)
cv.namedWindow('mask', cv.WINDOW_NORMAL)

cap = cap_1

while 1:
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    # fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)

    cv.imshow('frame', frame)
    cv.imshow('mask', fgmask)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

cap_1.release()
cap_2.release()
cap_3.release()
cap_4.release()
cap_5.release()
cv.destroyAllWindows()
