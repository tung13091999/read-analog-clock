import tkinter

import cv2
import numpy as np
import handClockProcessor as hcp
from tkinter import Tk, Button, Scale, Label, HORIZONTAL
from tkinter.filedialog import askopenfilename

img_file_path = ''


def select_file():
    global img_file_path
    img_file_path = askopenfilename()


def detect_circles():
    hcp.preprocessing_img(color_img_path=img_file_path, blur_ksize=(5, 5,))
    pass



def main():
    # Create tkinter root window
    root = Tk()
    root.title('Tuning parameters')

    # Create "Select file" button
    select_button = Button(root, text="Select file", command=select_file)
    select_button.pack()

    # Create slider for Canny threshold1
    canny_threshold1_label = Label(root, text="Canny Threshold1")
    canny_threshold1_label.pack()
    canny_threshold1_scale = Scale(root, from_=0, to=255, orient=HORIZONTAL)
    canny_threshold1_scale.set(100)
    canny_threshold1_scale.pack()
    print(canny_threshold1_scale)

    # Run tkinter
    root.mainloop()


if __name__ == main():
    main()

