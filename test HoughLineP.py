import cv2
import displayImages
import numpy as np
import handClockProcessor as hCP

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


color_img = cv2.imread('clock5.jpg  ')
display.add_img(img_type=color_type.BGR, img=color_img, subplot_pos=231, axis_title='Color img')
gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray_img, 100, 150, apertureSize=3)

_, contours = hCP.find_contours(color_img, gray_img)
clock_centre, radius = hCP.find_max_circle(color_img, contours)

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
# print(f'Squeezed lines = {new_lines}')
#
line_groups = hCP.cluster_lines(new_lines, np.radians(40))
# merged_lines = np.squeeze(merged_lines)
print(f'Number of line groups = {len(line_groups)}')
print(f'Merged lines = {line_groups[1][1]}')

max_points = []

for group in line_groups:
    max_length = 0
    point = [0, 0]
    for line in group:
        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]

        length_1 = np.sqrt((x1 - clock_centre[0])**2 + (y1 - clock_centre[1])**2)
        length_2 = np.sqrt((x2 - clock_centre[0])**2 + (y2 - clock_centre[1])**2)

        if length_1 >= length_2 and length_1 >= max_length:
            max_length = length_1
            point[0] = x1
            point[1] = y1
        if length_2 >= length_1 and length_2 >= max_length:
            max_length = length_2
            point[0] = x2
            point[1] = y2
    max_points.append(point)
for point in max_points:
    cv2.circle(color_img, center=point, radius=10, color=(255, 100, 100), thickness=-1)

print(f'Max points = {max_points}')
hand_points = sorted(max_points, key=lambda point: np.sqrt((point[0] - clock_centre[0])**2 + (point[1] - clock_centre[1])**2))
print(f'hour_point = {hand_points[0]} \n')

time_value = hCP.get_time(color_img, hand_points, clock_centre)
print(f'Time value = {time_value}')

display.add_img(img_type=color_type.GRAY, img=gray_img, subplot_pos=232, axis_title='Gray img')
display.add_img(img_type=color_type.GRAY, img=edges, subplot_pos=233, axis_title='Edges img')
display.add_img(img_type=color_type.BGR, img=color_img, subplot_pos=234, axis_title='Color img with lines')

display.show()

