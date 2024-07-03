import displayImages
import cv2

color_img = cv2.imread('clock8.png', 1)
gray_img = cv2.imread('clock8.png', cv2.IMREAD_GRAYSCALE)
binary_img = cv2.Canny(gray_img, 100, 150)

color_type = displayImages.ColorType
display = displayImages.ImageDisplay(fig_size=(10, 15))

display.add_img(img_type=color_type.BGR, img=color_img, subplot_pos=321, axis_title='')
display.add_img(img_type=color_type.GRAY, img=gray_img, subplot_pos=322, axis_title='')
display.add_img(img_type=color_type.BINARY, img=binary_img, subplot_pos=323, axis_title='')
display.add_img(img_type=color_type.BGR, img=color_img, subplot_pos=324, axis_title='')
display.add_img(img_type=color_type.GRAY, img=gray_img, subplot_pos=325, axis_title='')
display.add_img(img_type=color_type.BINARY, img=binary_img, subplot_pos=326, axis_title='')


display.show()
