import cv2
from tkinter import Tk, Button, Scale, Label, HORIZONTAL
from tkinter.filedialog import askopenfilename

dp_scale = Scale(None)
def detect_circles():
    # Đọc hình ảnh và chuyển đổi thành ảnh xám
    image = cv2.imread(file_path, 0)

    # Lấy giá trị từ các thanh trượt
    # dp = dp_scale.get()
    # minDist = min_dist_scale.get()
    # param1 = param1_scale.get()
    # param2 = param2_scale.get()
    # minRadius = min_radius_scale.get()
    # maxRadius = max_radius_scale.get()
    print(f'dp = {dp_scale.get()}')

    # # Áp dụng phương pháp HoughCircles để tìm vòng tròn
    # circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp, minDist, param1=param1, param2=param2,
    #                            minRadius=minRadius, maxRadius=maxRadius)
    #
    # # Kiểm tra nếu không tìm thấy vòng tròn
    # if circles is None:
    #     print("Không tìm thấy vòng tròn.")
    # else:
    #     print("Đã tìm thấy", len(circles[0]), "vòng tròn.")

# Hàm xử lý sự kiện khi nhấn nút "Chọn tệp tin"
def select_file():
    global file_path
    file_path = askopenfilename()


def create_scale(root, label_text, from_val, to_val, default_val):
    label = Label(root, text=label_text)
    label.pack()
    scale = Scale(root, from_=from_val, to=to_val, orient=HORIZONTAL)
    scale.set(default_val)
    scale.pack()
    return scale


def main():
    root = Tk()
    root.title("Hough Circles Detection")

    select_button = Button(root, text="Chọn tệp tin", command=select_file)
    select_button.pack()

    global dp_scale
    dp_scale = create_scale(root, "dp", 1, 10, 1)
    min_dist_scale = create_scale(root, "minDist", 1, 100, 50)
    param1_scale = create_scale(root, "param1", 1, 100, 50)
    param2_scale = create_scale(root, "param2", 1, 100, 30)
    min_radius_scale = create_scale(root, "minRadius", 0, 100, 0)
    max_radius_scale = create_scale(root, "maxRadius", 0, 100, 0)

    detect_button = Button(root, text="Tìm vòng tròn", command=detect_circles)
    detect_button.pack()

    root.mainloop()

if __name__ == main():
    main()