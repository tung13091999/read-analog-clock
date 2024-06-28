import cv2
import numpy as np


def get_angle(image, hand, center):
    x_h = hand[0]
    y_h = hand[1]
    x_c = center[0]
    y_c = center[1]
    cv2.arrowedLine(image, (x_c, y_c), (x_h, y_h), (0, 255, 0), 2)
    dx = x_h - x_c
    dy = y_h - y_c
    angle = 0
    if dx > 0 > dy:
        angle = np.pi/2 - np.arctan(abs(dy / dx))
    elif dx > 0 and dy > 0:
        angle = np.pi/2 + np.arctan(abs(dy / dx))
    elif dx < 0 < dy:
        angle = 3*np.pi/2 - np.arctan(abs(dy / dx))
    elif dx < 0 and dy < 0:
        angle = 3 * np.pi / 2 + np.arctan(abs(dy / dx))
    return angle*180/np.pi
