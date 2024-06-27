import cv2
import numpy as np

color_img = cv2.imread('clock2.png')
# gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
gray_img = cv2.imread('clock2.png', cv2.IMREAD_GRAYSCALE)
# blurred_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

# Finding centre of clock by HoughCircle
circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=200, minRadius=0, maxRadius=0)
circles = np.uint16(np.around(circles))
print(f'List of found circles : {circles}')
maxRad = 0
clock_centre = ()
if circles is not None:
    for circle in circles[0]:
        rad = circle[2]
        if rad > maxRad:
            maxRad = rad
            clock_centre = (circle[0], circle[1])
print(f'Max radius of clock = {maxRad}')
print(f'Clock centre = {clock_centre}')
cv2.circle(color_img, clock_centre, maxRad, (255, 0, 255), 3)

# Find Contours
edges = cv2.Canny(gray_img, 50, 150)
cv2.imshow('EDGES', edges)
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(image=color_img, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1)

# Getting Contours which contain centre point inside it --> pass in shortlist[]
contour_shortList = []
print("**Bounding rect**")
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if ((x + w) > clock_centre[0] > x) and (y < clock_centre[1] < y + h):
        contour_shortList.append(contour)
        cv2.rectangle(color_img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 255), thickness=3)
        print(f'width = {w} and height = {h}')

# Min Contour Area = Hand Clock Contour
contour_minArea = 0
handContour = []
for contour in contour_shortList:
    if contour_minArea == 0:
        contour_minArea = cv2.contourArea(contour)
    elif contour_minArea > cv2.contourArea(contour):
        contour_minArea = cv2.contourArea(contour)
        handContour = contour
cv2.drawContours(color_img, contours=handContour, contourIdx=-1, color=(255, 0, 0), thickness=2)

cv2.imshow('IMG', color_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
