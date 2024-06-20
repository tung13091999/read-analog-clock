import cv2
import numpy as np

# Tạo một tập hợp các điểm
points = np.array([[50, 50], [200, 50], [200, 200], [50, 200], [100, 100]])

# Tìm đa giác lồi
hull = cv2.convexHull(points)

# Vẽ đa giác lồi
image = np.zeros((250, 250), dtype=np.uint8)
cv2.drawContours(image, [hull], 0, 255, 2)

# Hiển thị ảnh với đa giác lồi
cv2.imshow('Convex Hull', image)
cv2.waitKey(0)
cv2.destroyAllWindows()