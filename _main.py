# import tkinter
#
# import cv2
# import numpy as np
import handClockProcessor as hCP
from tkinter import Tk, Button, Scale, Label, HORIZONTAL
from tkinter.filedialog import askopenfilename

img_file_path = ''
canny_threshold1 = 1
canny_threshold2 = 1
hcc_dp = 1
hcc_min_dist = 1
hcc_param1 = 1
hcc_param2 = 1


def select_file():
    global img_file_path
    img_file_path = askopenfilename()


def detect_circles():
    gray_img, color_img = hCP.preprocessing_img(color_img_path=img_file_path,
                                                blur_ksize=(5, 5),
                                                canny_threshold1=canny_threshold1,
                                                canny_threshold2=canny_threshold2)
    clock_centre, max_rad = hCP.find_max_clock_circle(color_img=color_img,
                                                      gray_img=gray_img,
                                                      dp=hcc_dp,
                                                      min_dist=hcc_min_dist,
                                                      param1=hcc_param1,
                                                      param2=hcc_param2)


def create_tkinter_slider(tkinter_root, label_name, start_val, end_val, default_val, orient_val):
    label = Label(tkinter_root, text=label_name)
    label.pack()
    scale = Scale(tkinter_root, from_=start_val, to=end_val, orient=orient_val)
    scale.set(default_val)
    scale.pack()
    return scale.get()


def main():
    # Create tkinter root window
    root = Tk()
    root.title('Tuning parameters')

    # Create "Select file" button
    select_button = Button(root, text="Select file", command=select_file)
    select_button.pack()

    # Create slider for Canny threshold1
    global canny_threshold1
    canny_threshold1 = create_tkinter_slider(root, 'Canny Threshold1', 0, 255, 100, HORIZONTAL)

    # Create slider for Canny threshold2
    global canny_threshold2
    canny_threshold2 = create_tkinter_slider(root, 'Canny Threshold2', 0, 255, 150, HORIZONTAL)

    # Create slider for Hough Circle dp
    global hcc_dp
    hcc_dp = create_tkinter_slider(root, 'Hough CC dp', 1, 10, 1, HORIZONTAL)

    # Create slider for Hough Circle minDist
    global hcc_min_dist
    hcc_min_dist = create_tkinter_slider(root, 'Hough CC min dist', 10, 100, 10, HORIZONTAL)

    # Create slider for Hough Circle param1
    global hcc_param1
    hcc_param1 = create_tkinter_slider(root, 'Hough CC param1', 0, 255, 50, HORIZONTAL)

    # Create slider for Hough Circle param2
    global hcc_param2
    hcc_param2 = create_tkinter_slider(root, 'Hough CC param2', 0, 300, 100, HORIZONTAL)

    detect_button = Button(root, text="Tìm vòng tròn", command=detect_circles)
    detect_button.pack()
    # Run tkinter
    root.mainloop()


if __name__ == main():
    main()


