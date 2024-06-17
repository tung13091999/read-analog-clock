import cv2
import numpy as np

img = cv2.imread('sudoku.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray)

ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
cv2.imshow('thresh', thresh)

edges = cv2.Canny(thresh, 50, 150)
cv2.imshow("edges", edges)

copy1 = np.copy(img)
copy2 = np.copy(img)
# sobel = cv2.Sobel(thresh, -1, 1, 0)
# cv2.imshow("sobel", sobel)

# This returns an array of rho and theta values
# 3D matrix with shape = [[[r, theta]]]
lines = cv2.HoughLines(edges, 1, np.pi/180, 300)
if lines is not None:
    for i in range(0, len(lines)):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = np.cos(theta)
        b = np.sin(theta)

        # Tọa độ của điểm vuông góc
        x0 = rho*a
        y0 = rho*b

        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*a))
        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*b))

        cv2.line(copy1, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)

cv2.imshow("Standard Hough Line Transform", copy1)

linesP = cv2.HoughLinesP(edges, 0.3, np.pi/180, 150, minLineLength=100, maxLineGap=10)
print(linesP)

if linesP is not None:
    for i in range(0, len(linesP)):
        l = linesP[i][0]
        cv2.line(copy2, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)

cv2.imshow("Probabilistic Hough Line Transform", copy2)
cv2.waitKey(0)