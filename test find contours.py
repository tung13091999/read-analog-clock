import cv2
import numpy as np

img = cv2.imread('08h55m00.png', 1)
temp = img.copy()
temp2 = img.copy()
img_grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
# kernel = np.ones((5, 5), np.uint8)
# thresh = cv2.erode(thresh, kernel, iterations=1)
edges = cv2.Canny(thresh, 100, 200)
cv2.imshow('EDGES', edges)
cv2.imshow('THRESHOLD IMAGE', thresh)

# Getting and display Contours
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(image=img, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1)
cv2.imshow('Contours', img)

# Getting Contours which contain centre point within it --> pass in shortlist[]
centre = (494, 486, 470)
cv2.circle(temp, center=(centre[0], centre[1]), radius=5, color=(0, 255, 0), thickness=-1)
shortlist = []
for i in contours:
    x, y, w, h = cv2.boundingRect(i)
    if ((x + w) > centre[0] > x) and (y < centre[1] < y + h):
        shortlist.append(i)
# cv2.drawContours(temp, shortlist, -1, (255, 0, 0), 2)

# Getting Contour of Hands ~ get the min area of contour in shortlist
minArea = 0
handContour = []
for i in shortlist:
    if minArea == 0:
        minArea = cv2.contourArea(i)
    elif minArea > cv2.contourArea(i):
        minArea = cv2.contourArea(i)
        handContour = i
cv2.drawContours(temp, handContour, -1, (255, 0, 0), 2)
cv2.imshow('hand contour', temp)

# # Getting and Clustering Hull Points
hull = cv2.convexHull(handContour)
# for i in range(0, len(hull)):
#     cv2.circle(temp, center=(hull[i][0][0], hull[i][0][1]), radius=5, color=(100, 100, 100), thickness=-1)

cv2.drawContours(temp, [hull], -1, (0, 0, 255), 2)
cv2.imshow('Convex Hull', temp)


def simplify_convex_hull(hull, epsilon):
    # Chuyển đổi danh sách các điểm convex hull sang định dạng numpy array
    points = np.array(hull, dtype=np.float32)
    # Đơn giản hóa convex hull bằng thuật toán Douglas-Peucker
    simplified_points = cv2.approxPolyDP(points, epsilon, True)
    # Chuyển đổi danh sách các điểm đơn giản hóa trở lại định dạng danh sách các điểm
    simplified_hull = simplified_points.squeeze().tolist()
    return simplified_hull


def get_angle(image, hand, center):
    x_h = hand[0]
    y_h = hand[1]
    x_c = center[0]
    y_c = center[1]
    cv2.arrowedLine(image, (x_c, y_c), (x_h, y_h), (0, 0, 255), 2)
    dx = x_h - x_c
    dy = y_h - y_c
    angle = 0
    if dx > 0 > dy:
        angle = np.pi/2 - np.arctan(abs(dy / dx))
    elif dx > 0 and dy > 0:
        angle = np.pi/2 + np.arctan(abs(dy / dx))
    elif dx < 0 < dy:
        angle = 3*np.pi/2 - np.arctan(abs(dy / dx))
    elif dx < 0 and dy < 0:
        angle = 3 * np.pi / 2 + np.arctan(abs(dy / dx))
    return angle*180/np.pi


print(simplify_convex_hull(hull, 8))
unique_vertices = simplify_convex_hull(hull, 8)
unique_vertices = np.array(unique_vertices, dtype=np.int32)
sorted_vertices = sorted(unique_vertices, key=lambda vertex: np.sqrt((centre[0] - vertex[0])**2 + (centre[1] - vertex[1])**2), reverse=True)
print(sorted_vertices)
second_hand = sorted_vertices[0]
minute_hand = sorted_vertices[1]
hour_hand = sorted_vertices[2]

second_value = int(get_angle(temp, second_hand, centre)*60 / 360)
minute_value = int(get_angle(temp, minute_hand, centre)*60 / 360)
hour_value = int(get_angle(temp, hour_hand, centre)*12 / 360)

print(f"time = {hour_value} : {minute_value} : {second_value}")
cv2.imshow('Unique vertex', temp)
cv2.waitKey(0)
cv2.destroyAllWindows()
