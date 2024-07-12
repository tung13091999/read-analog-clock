import cv2
import displayImages
import numpy as np
from handClockProcessor import find_max_circle, find_contours, merge_lines

display = displayImages.ImageDisplay(fig_size=(15, 10))
color_type = displayImages.ColorType


def distance_to_line(point, line_points):
    x, y = point
    x_1, y_1 = line_points[0]
    x_2, y_2 = line_points[1]

    numerator = abs((y_2 - y_1) * x - (x_2 - x_1) * y + x_2 * y_1 - x_1 * y_2)
    denominator = np.sqrt((y_2 - y_1) ** 2 + (x_2 - x_1) ** 2)
    distance = numerator / denominator

    return distance


color_img = cv2.imread('img_2/09h00m20s.png')
display.add_img(img_type=color_type.BGR, img=color_img, subplot_pos=231, axis_title='Color img')
gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray_img, 100, 150, apertureSize=3)

_, contours = find_contours(color_img, gray_img)
clock_centre, radius = find_max_circle(color_img, contours)

number_of_lines = 0
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=20, minLineLength=50, maxLineGap=10)

new_lines = []
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        tmp_line_points = [(x1, y1), (x2, y2)]
        # cv2.line(color_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        if distance_to_line(clock_centre, tmp_line_points) < 10:
            cv2.line(color_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            new_lines.append(line)
            number_of_lines = number_of_lines + 1
print(f'Number of lines = {number_of_lines}')
new_lines = np.squeeze(new_lines)
print(f'Squeezed lines = {new_lines}')

merged_lines = merge_lines(new_lines, np.radians(40))
print(f'Merged lines = {merged_lines}')

for line in merged_lines:
    x1, y1, x2, y2 = line
    cv2.line(color_img, (x1, y1), (x2, y2), (255, 0, 0), 2)


display.add_img(img_type=color_type.GRAY, img=gray_img, subplot_pos=232, axis_title='Gray img')
display.add_img(img_type=color_type.GRAY, img=edges, subplot_pos=233, axis_title='Edges img')
display.add_img(img_type=color_type.BGR, img=color_img, subplot_pos=234, axis_title='Color img with lines')

display.show()

