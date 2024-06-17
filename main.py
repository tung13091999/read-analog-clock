import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread(filename='clock2.png', flags=1)
# cv2.imshow('Org img', img)

img_gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('Gray scale', img_gray_scale)

img_inverse = cv2.bitwise_not(img_gray_scale)
cv2.imshow('Inverse img', img_inverse)

ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
cv2.imshow('thresh img', thresh)

kernel = np.ones(shape=(5, 5), dtype=np.uint8)

# Erode away pure white, increase black
thresh = cv2.erode(src=thresh, kernel=kernel, iterations=1)
cv2.imshow('thresh img', thresh)

edges = cv2.Canny(thresh, 100, 300)
cv2.imshow('edges', edges)

#Circle Dectection Part
circles = cv2.HoughCircles(image=img_inverse, method=cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=200, minRadius=0, maxRadius=0)
print(circles)
cv2.waitKey(0)
