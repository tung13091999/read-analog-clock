import cv2
import numpy as np

img = cv2.imread('clock3.jpg', 1)
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
    if (centre[0] < (x+w) and centre[0] > x) and (centre[1]>y and centre[1]<y+h):
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

# Getting and Clustering Hull Points
hull = cv2.convexHull(handContour)
# for i in range(0, len(hull)):
#     cv2.circle(temp, center=(hull[i][0][0], hull[i][0][1]), radius=5, color=(100, 100, 100), thickness=-1)

cv2.drawContours(temp, [hull], -1, (0, 0, 255), 2)
cv2.imshow('Convex Hull', temp)

# hull_sorted = sorted(hull, key=lambda x: x[0][0]) # sắp xếp đỉnh convex tăng dần theo tọa độ x
# print(hull)
# threshold = 19  # Ngưỡng khoảng cách giữa các đỉnh
# unique_vertices = []
# for i in range(len(hull_sorted)):
#     if i == 0 or abs(hull_sorted[i][0][0] - unique_vertices[-1][0]) > threshold:
#         unique_vertices.append(hull_sorted[i][0])
#
# # In tọa độ các đỉnh duy nhất
# for vertex in unique_vertices:
#     print(vertex)
#     cv2.circle(temp, center=(vertex[0], vertex[1]), radius=5, color=(100, 100, 100), thickness=-1)
# cv2.imshow('Unique vertex', temp)

def simplify_convex_hull(hull, epsilon):
    # Chuyển đổi danh sách các điểm convex hull sang định dạng numpy array
    points = np.array(hull, dtype=np.float32)
    # Đơn giản hóa convex hull bằng thuật toán Douglas-Peucker
    simplified_points = cv2.approxPolyDP(points, epsilon, True)
    # Chuyển đổi danh sách các điểm đơn giản hóa trở lại định dạng danh sách các điểm
    simplified_hull = simplified_points.squeeze().tolist()
    return simplified_hull
print(simplify_convex_hull(hull, 8))
unique_vertices = simplify_convex_hull(hull, 8)
unique_vertices = np.array(unique_vertices, dtype=np.int32)
for vertex in unique_vertices:
    print(vertex)
    cv2.circle(temp, center=(vertex[0], vertex[1]), radius=5, color=(100, 100, 100), thickness=-1)
cv2.imshow('Unique vertex', temp)
cv2.imshow('Unique vertex', temp)
cv2.waitKey(0)
cv2.destroyAllWindows()
