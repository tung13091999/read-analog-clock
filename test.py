import cv2
import numpy as np

# Đường dẫn đến hình ảnh gốc
image_path = 'clock2.png'

# Đọc hình ảnh gốc
image = cv2.imread(image_path)

# Chuyển đổi hình ảnh sang ảnh xám
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Áp dụng Gaussian blur để giảm nhiễu
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Áp dụng Canny edge detection
edges = cv2.Canny(blurred_image, 50, 150)

# Phát hiện các vòng tròn trong ảnh
circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 50,
                           param1=100, param2=30, minRadius=0, maxRadius=0)

# Kiểm tra xem có vòng tròn được tìm thấy hay không
if circles is not None:
    # Chuyển đổi tọa độ và bán kính vòng tròn thành số nguyên
    circles = np.round(circles[0, :]).astype(int)

    # Vẽ các vòng tròn được tìm thấy lên hình ảnh gốc
    for (x, y, r) in circles:
        cv2.circle(image, (x, y), r, (0, 255, 0), 2)

    # Hiển thị hình ảnh với các vòng tròn được tìm thấy
    cv2.imshow('Detected Circles', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No circles found.")