import cv2
import numpy as np

img = cv2.imread('clock7.png', cv2.IMREAD_GRAYSCALE)
img = cv2.GaussianBlur(img, (5, 5), 0)
circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 10, param1=50, param2=100, minRadius=0, maxRadius=0)
print(circles)


edges = cv2.Canny(img, 50, 150)

cv2.imshow('EDGES', edges)
cv2.imshow('IMG', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

