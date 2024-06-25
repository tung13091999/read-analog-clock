import cv2
import numpy as np

img = cv2.imread('clock2.png')
img_copy = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(gray, (3, 3), 10)
cv2.imshow('blurred', blurred)

dst = cv2.Canny(blurred, 100, 200, None, 3)
cv2.imshow('Canny', dst)

linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 25, None, 10, 10)
if linesP is not None:
    for points in linesP:
        x1, y1, x2, y2 = points[0]
        cv2.line(img_copy,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imshow('HoughLineP', img_copy)

slopes = []
for line in linesP:
    x1, y1, x2, y2 = line[0]
    theta = np.arctan2(y2 - y1, x2 - x1)*180/np.pi
    slopes.append(theta)
print(slopes)
angleThreshold = 1
clockHand = []
for i in range(0, len(linesP)):
    for j in range(i+1, len(linesP)):
        if abs(slopes[i] - slopes[j]) < angleThreshold:
            slopes[j] = 0

for i in range(0, len(linesP)):
    if slopes[i] != 0:
        clockHand.append(linesP[i][0])
print(linesP)
print(slopes)
print(clockHand)

if clockHand is not None:
    for line in clockHand:
        x_point = (line[0], line[1])
        y_point = (line[2], line[3])
        cv2.line(img, pt1=x_point, pt2=y_point, color=(0, 255, 0), thickness=3)

cv2.imshow('ClockHand', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
