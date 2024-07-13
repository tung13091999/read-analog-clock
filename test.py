import cv2
import displayImages
import numpy as np
import handClockProcessor as hCP

display = displayImages.ImageDisplay(fig_size=(15, 10))
color_type = displayImages.ColorType

color_img = cv2.imread('img_2/09h00m20s.png')
display.add_img(img_type=color_type.BGR, img=color_img, subplot_pos=231, axis_title='Color img')
gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(gray_img, 100, 150, apertureSize=3)
gray_img = cv2.GaussianBlur(gray_img, ksize=(3,3), sigmaX=0)
_, thresh_img = cv2.threshold(gray_img, 240, 255, cv2.THRESH_BINARY)
display.add_img(img_type=color_type.GRAY, img=gray_img, subplot_pos=232, axis_title='Color img')

_, contours = hCP.find_contours(color_img, gray_img)
display.show()