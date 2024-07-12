import cv2
import displayImages
import numpy as np

display = displayImages.ImageDisplay(fig_size=(15, 10))
color_type = displayImages.ColorType

color_img = cv2.imread('img_2/09h00m20s.png')
display.add_img(img_type=color_type.BGR, img=color_img, subplot_pos=231, axis_title='Color img')

display.show()
#
#
# cv2.imshow('ClockHand', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
