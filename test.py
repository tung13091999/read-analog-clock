import cv2
import numpy as np

# Đọc ảnh đầu vào và chuyển đổi sang ảnh grayscale
image = cv2.imread('clock13.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Áp dụng phép nhị phân để tách đối tượng nổi bật
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Tìm các đường viền trong ảnh nhị phân
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Vẽ đường viền lên ảnh gốc
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# Hiển thị ảnh kết quả
cv2.imshow('Binary', thresh)
cv2.imshow('Contours', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
