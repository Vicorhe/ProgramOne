import cv2
from glob import glob


def detect_shapes(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 127, 255, 1)

    print(cv2.findContours(thresh, 1, 2))

    _, contours, h = cv2.findContours(thresh, 1, 2)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        print(len(approx))
        if len(approx) == 5:
            print("pentagon")
            cv2.drawContours(img, [cnt], 0, 255, -1)
        elif len(approx) == 3:
            print("triangle")
            cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)
        elif len(approx) == 4:
            print("square")
            cv2.drawContours(img, [cnt], 0, (0, 0, 255), -1)
        elif len(approx) == 9:
            print("half-circle")
            cv2.drawContours(img, [cnt], 0, (255, 255, 0), -1)
        elif len(approx) > 15:
            print("circle")
            cv2.drawContours(img, [cnt], 0, (0, 255, 255), -1)

    cv2.imshow('img', img)
    cv2.waitKey(0)


for fn in glob('../../../Pictures/square/google/*.jpg'):
    image = cv2.imread(fn)
    detect_shapes(image)
    ch = cv2.waitKey()
    if ch == 27:
        break

cv2.destroyAllWindows()