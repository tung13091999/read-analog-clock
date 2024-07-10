import cv2
import numpy as np


def preprocessing_img(color_img_path, blur_ksize, thresh_value, thresh_max_value):
    """
    Returns:
        [color_img, gray_img, thresh_img]
    """

    color_img = cv2.imread(color_img_path)

    # gray_img = cv2.imread(color_img_path, cv2.IMREAD_GRAYSCALE)

    gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

    gray_img = cv2.GaussianBlur(gray_img, ksize=blur_ksize, sigmaX=0)
    _, thresh_img = cv2.threshold(gray_img, thresh_value, thresh_max_value, cv2.THRESH_BINARY)

    kernel = np.ones((5, 5), np.uint8)
    dilation_img = cv2.dilate(thresh_img, kernel, iterations=1)
    # canny_edges = cv2.Canny(gray_img, canny_threshold1, canny_threshold2)
    return [color_img, gray_img, thresh_img, dilation_img]


def find_max_clock_circle(color_img, gray_img, dp, min_dist, param1, param2):
    """
    Returns:
        [clock_centre, max_rad]
    """
    circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, dp=dp, minDist=min_dist, param1=param1, param2=param2,
                               minRadius=0, maxRadius=0)
    if circles is None:
        print('Cannot found any circles. Please check!')
    circles = np.uint16(circles)
    print(f'List of found circles : {circles}')
    max_rad = 0
    clock_centre = ()
    for circle in circles[0]:
        rad = circle[2]
        if rad > max_rad:
            max_rad = rad
            clock_centre = (circle[0], circle[1])
    print(f'Max radius of clock = {max_rad}')
    print(f'Clock centre = {clock_centre}')
    cv2.circle(color_img, clock_centre, max_rad, (255, 0, 255), 3)
    # cv2.imshow('Circle', color_img)
    return [clock_centre, max_rad]


def find_contours(color_img, binary_img):
    """
    Returns:
        [color_img, contours]
    """
    contours, _ = cv2.findContours(binary_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image=color_img, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=3)
    return [color_img, contours]


def find_max_circle(color_img, contours):
    """
    Returns:
        [clock_centre, max_rad]
    """
    max_x = 0
    max_y = 0
    max_width = 0
    max_height = 0
    max_bounding_rect_area = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w*h > max_bounding_rect_area:
            max_bounding_rect_area = w*h
            max_width = w
            max_height = h
            max_x = x
            max_y = y
    print(f'Max bounding width = {max_width}')
    print(f'Max bounding height = {max_height}')

    cv2.rectangle(color_img, pt1=(max_x, max_y), pt2=(max_x + max_width, max_y + max_height), color=(0, 0, 0), thickness=3)

    clock_centre = (int(max_x + max_width/2), int(max_y + max_height/2))
    cv2.circle(color_img, center=clock_centre, radius=10, color=(0, 0, 255), thickness=-1)
    max_rad = int((max_height + max_width)/4)
    print(f'Clock centre = {clock_centre}')
    print(f'Max radius = {max_rad}')
    return [clock_centre, max_rad]


def find_hand_contour(color_img, contours, clock_centre):
    """
    Returns:
        hand_contour
    """
    # Getting Contours which contain centre point inside it --> pass in shortlist[]
    contour_shortlist = []
    print("**Bounding rect**")
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if ((x + w) > clock_centre[0] > x) and (y < clock_centre[1] < y + h):
            contour_shortlist.append(contour)
            cv2.rectangle(color_img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 255), thickness=3)
            print(f'width = {w} and height = {h}')
    # Min Contour Area = Hand Clock Contour
    contour_min_area = 0
    hand_contour = []
    for contour in contour_shortlist:
        if contour_min_area == 0:
            contour_min_area = cv2.contourArea(contour)
        elif contour_min_area > cv2.contourArea(contour):
            contour_min_area = cv2.contourArea(contour)
            hand_contour = contour
    print(f'Hand contour = {hand_contour}')
    cv2.drawContours(color_img, contours=hand_contour, contourIdx=-1, color=(255, 0, 0), thickness=2)
    return hand_contour


def find_possible_hand_vertices(color_img, hand_contour, approx_epsilon, clock_centre, min_hand_length):
    """
    Returns:
        [hour_hand_vertex, minute_hand_vertex, second_hand_vertex]
    """
    hand_hull = cv2.convexHull(hand_contour)
    # print(f'Hand Convex = {hand_hull}')
    cv2.drawContours(color_img, contours=[hand_hull], contourIdx=-1, color=(0, 0, 255), thickness=2)

    # Find the Vertices of Convex Hull ~ Vertices of Hand Clock
    # Because Convex Hull has many bad vertices, so we need to clear them to get desired vertices
    # Do it by approxPolyDP method
    desired_hull_vertices = cv2.approxPolyDP(hand_hull, epsilon=approx_epsilon, closed=True)
    # print(f'Simplified points = {desired_hull_vertices}')
    # for i in desired_hull_vertices:
    #     cv2.circle(color_img, center=i[0], radius=10, color=(255, 100, 100), thickness=-1)

    # Now, handHull = quadrilateral = polygon has 4 vertices
    # Only 3 furthest vertices from centre = sec/min/hour vertices --> Need to sort
    sorted_vertices = sorted(desired_hull_vertices, key=lambda vertex: np.sqrt(
        (clock_centre[0] - vertex[0][0]) ** 2 + (clock_centre[1] - vertex[0][1]) ** 2), reverse=True)
    # print(f'Sorted vertice = {sorted_vertices}')

    possible_vertices = []
    # Eliminate some stuff vertices
    for i in sorted_vertices:
        tmp_length = np.sqrt((clock_centre[0] - i[0][0]) ** 2 + (clock_centre[1] - i[0][1]) ** 2)
        if tmp_length > min_hand_length:
            cv2.circle(color_img, center=i[0], radius=10, color=(255, 100, 100), thickness=-1)
            possible_vertices.append(i)
    print(f'Possible vertices = {possible_vertices}')
    return possible_vertices

    # second_hand_vertex = ...
    # minute_hand_vertex = ...
    # hour_hand_vertex = ...
    #
    # try:
    #     second_hand_vertex = sorted_vertices[1][0]
    #     minute_hand_vertex = sorted_vertices[0][0]
    #     hour_hand_vertex = sorted_vertices[2][0]
    # except NameError:
    #     print('xxx')
    #
    # return [hour_hand_vertex, minute_hand_vertex, second_hand_vertex]


def get_angle(color_img, hand, center):
    x_h = hand[0]
    y_h = hand[1]
    x_c = center[0]
    y_c = center[1]
    cv2.arrowedLine(color_img, (x_c, y_c), (x_h, y_h), (0, 255, 0), 2)
    dx = x_h - x_c
    dy = y_h - y_c
    angle = 0
    if dx >= 0 >= dy:
        angle = np.pi / 2 - np.arctan(abs(dy / dx))
    elif dx >= 0 and dy >= 0:
        angle = np.pi / 2 + np.arctan(abs(dy / dx))
    elif dx <= 0 <= dy:
        angle = 3 * np.pi / 2 - np.arctan(abs(dy / dx))
    elif dx <= 0 and dy <= 0:
        angle = 3 * np.pi / 2 + np.arctan(abs(dy / dx))
    return angle * 180 / np.pi


def get_time(color_img, time_hand_vertices, clock_centre):
    """
    Returns:
        [hour_value, minute_value, second_value]
    """
    second_hand_vertex = time_hand_vertices[2]
    minute_hand_vertex = time_hand_vertices[1]
    hour_hand_vertex = time_hand_vertices[0]

    second_angle = get_angle(color_img, second_hand_vertex, clock_centre)
    minute_angle = get_angle(color_img, minute_hand_vertex, clock_centre)
    hour_angle = get_angle(color_img, hour_hand_vertex, clock_centre)

    print(f'second angle = {second_angle}')
    print(f'minute angle = {minute_angle}')
    print(f'hour angle = {hour_angle}')

    second_value = int(np.round(second_angle * 60 / 360))
    minute_value = int(np.round(minute_angle * 60 / 360))
    hour_value = int(np.round(hour_angle * 12 / 360))

    if hour_value == 12:
        hour_value = 0
    if minute_value == 60:
        minute_value = 0
    if second_value == 60:
        second_value = 0

    if 50 <= minute_value <= 59 and hour_angle < (hour_value + 1)*30 - 10 and hour_value != 0:
        hour_value = hour_value - 1
    elif 50 <= minute_value <= 59 and hour_angle < (hour_value + 1)*30 - 10 and hour_value == 0:
        hour_value = 11
    return [hour_value, minute_value, second_value]


def main():
    pass


if __name__ == main():
    main()
