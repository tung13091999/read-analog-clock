import cv2
from tkinter import Tk, Button, Scale, Label, HORIZONTAL
from tkinter.filedialog import askopenfilename

def detect_circles():
    # Đọc hình ảnh và chuyển đổi thành ảnh xám
    image = cv2.imread(file_path, 0)

    # Lấy giá trị từ các thanh trượt
    dp = dp_scale.get()
    minDist = min_dist_scale.get()
    param1 = param1_scale.get()
    param2 = param2_scale.get()
    minRadius = min_radius_scale.get()
    maxRadius = max_radius_scale.get()

    # Áp dụng phương pháp HoughCircles để tìm vòng tròn
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp, minDist, param1=param1, param2=param2,
                               minRadius=minRadius, maxRadius=maxRadius)

    # Kiểm tra nếu không tìm thấy vòng tròn
    if circles is None:
        print("Không tìm thấy vòng tròn.")
    else:
        print("Đã tìm thấy", len(circles[0]), "vòng tròn.")

# Hàm xử lý sự kiện khi nhấn nút "Chọn tệp tin"
def select_file():
    global file_path
    file_path = askopenfilename()

# Tạo cửa sổ gốc tkinter
root = Tk()
root.title("Hough Circles Detection")

# Tạo nút "Chọn tệp tin"
select_button = Button(root, text="Chọn tệp tin", command=select_file)
select_button.pack()

# Tạo các thanh trượt để điều chỉnh các giá trị đầu vào
dp_label = Label(root, text="dp")
dp_label.pack()
dp_scale = Scale(root, from_=1, to=10, orient=HORIZONTAL)
dp_scale.set(1)
dp_scale.pack()

min_dist_label = Label(root, text="minDist")
min_dist_label.pack()
min_dist_scale = Scale(root, from_=1, to=100, orient=HORIZONTAL)
min_dist_scale.set(50)
min_dist_scale.pack()

param1_label = Label(root, text="param1")
param1_label.pack()
param1_scale = Scale(root, from_=1, to=100, orient=HORIZONTAL)
param1_scale.set(50)
param1_scale.pack()

param2_label = Label(root, text="param2")
param2_label.pack()
param2_scale = Scale(root, from_=1, to=100, orient=HORIZONTAL)
param2_scale.set(30)
param2_scale.pack()

min_radius_label = Label(root, text="minRadius")
min_radius_label.pack()
min_radius_scale = Scale(root, from_=0, to=100, orient=HORIZONTAL)
min_radius_scale.set(0)
min_radius_scale.pack()

max_radius_label = Label(root, text="maxRadius")
max_radius_label.pack()
max_radius_scale = Scale(root, from_=0, to=100, orient=HORIZONTAL)
max_radius_scale.set(0)
max_radius_scale.pack()

# Tạo nút "Tìm vòng tròn"
detect_button = Button(root, text="Tìm vòng tròn", command=detect_circles)
detect_button.pack()

# Chạy ứng dụng tkinter
root.mainloop()