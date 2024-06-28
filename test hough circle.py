import cv2
import numpy as np

img = cv2.imread('clock7.png', cv2.IMREAD_GRAYSCALE)
img = cv2.GaussianBlur(img, (11, 11), 0)
cv2.imshow('xxx', img)
cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 10, param1=50, param2=100, minRadius=0, maxRadius=0)
circles = np.uint16(np.around(circles))
print(circles)
# if circles is not None:
#     circles = np.uint16(np.around(circles))
# for i in circles[0, :]:
#     center = (i[0], i[1])
#     # circle center
#     cv2.circle(cimg, center, 1, (0, 100, 100), 3)
#     # circle outline
#     radius = i[2]
#     cv2.circle(cimg, center, radius, (255, 0, 255), 3)

# minRad = circles[0][0][2]
# centre = ()
# for i in circles[0]:
#     if i[2] <= minRad:
#         minRad = i[2]
#         centre = (i[0], i[1])
# cv2.circle(cimg, centre, minRad,(0, 255, 0), 2)
# print(minRad)
#
maxRad = 0
centre = ()
for i in circles[0]:
    if i[2] > maxRad:
        maxRad = i[2]
        centre = (i[0], i[1])
cv2.circle(cimg, centre, int(maxRad),(255, 0, 0), 2)
cv2.imshow('detected circles', cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()