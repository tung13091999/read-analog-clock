import cv2
import numpy as np
from angleProcessor import get_angle

color_img = cv2.imread('img_1.png')
# gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
gray_img = cv2.imread('img_1.png', cv2.IMREAD_GRAYSCALE)
gray_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

# Finding centre of clock by HoughCircle
circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, 1, 10, param1=50, param2=100, minRadius=0, maxRadius=0)
if circles is None:
    exit('Cannot found any circles. Please check!')

circles = np.uint16(circles)
print(f'List of found circles : {circles}')
maxRad = 0
clock_centre = ()
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
print(f'Hand contour = {handContour}')
cv2.drawContours(color_img, contours=handContour, contourIdx=-1, color=(255, 0, 0), thickness=2)

# Find Convex Hull of Hand Contour
handHull = cv2.convexHull(handContour)
print(f'Hand Convex = {handHull}')
cv2.drawContours(color_img, contours=[handHull], contourIdx=-1, color=(0, 0, 255), thickness=2)

# Find the Vertices of Convex Hull ~ Vertices of Hand Clock
# Because Convex Hull has many bad vertices, so we need to clear them to get desired vertices
# Do it by approxPolyDP method
desired_hull_vertices = cv2.approxPolyDP(handHull, epsilon=8, closed=True)
desired_hull_vertices = desired_hull_vertices.squeeze().tolist()
print(f'Simplified points = {desired_hull_vertices}')

# Now, handHull = quadrilateral = polygon has 4 vertices
# Only 3 furthest vertices from centre = sec/min/hour vertices --> Need to sort
sorted_vertices = sorted(desired_hull_vertices, key=lambda vertex: np.sqrt((clock_centre[0] - vertex[0])**2 + (clock_centre[1] - vertex[1])**2), reverse=True)
print(f'Sorted vertice = {sorted_vertices}')
second_hand_vertex = sorted_vertices[0]
minute_hand_vertex = sorted_vertices[1]
hour_hand_vertex = sorted_vertices[2]
# Draw time_vertices on img
for i in range(0, 3):
    cv2.circle(color_img, center=sorted_vertices[i], radius=5, color=(255, 0, 255), thickness=-1)
second_value = int(get_angle(color_img, second_hand_vertex, clock_centre)*60 / 360)
minute_value = int(get_angle(color_img, minute_hand_vertex, clock_centre)*60 / 360)
hour_value = int(get_angle(color_img, hour_hand_vertex, clock_centre)*12 / 360)

print(f"Time result = {hour_value} : {minute_value} : {second_value}")
cv2.imshow('IMG', color_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
