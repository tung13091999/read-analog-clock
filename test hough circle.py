import cv2
import numpy as np

img = cv2.imread('clock2.png', cv2.IMREAD_GRAYSCALE)
img = cv2.medianBlur(img, 5)
cv2.imshow('xxx', img)
cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT, 0.5, 20, param1=50, param2=300, minRadius=0, maxRadius=0)
circles = np.uint16(np.around(circles))

maxRad = 0
centre = ()
for i in circles[0]:
    if i[2] > maxRad:
        maxRad = i[2]
        centre = (i[0], i[1])
print(circles)

cv2.circle(cimg, centre, maxRad,(0, 255, 0), 2)
cv2.imshow('detected circles', cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()