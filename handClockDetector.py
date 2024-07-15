import cv2
import numpy as np

color_img = None
gray_img = None


class CannyEdgeParams:
    def __init__(self, threshold1, threshold2, aperture_size=3):
        self.threshold1 = threshold1
        self.threshold2 = threshold2
        self.aperture_size = aperture_size


def preprocess_img(color_img_path, canny_edge_params):
    global color_img, gray_img
    color_img = cv2.imread(color_img_path)
    gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
    edges = None

    if isinstance(canny_edge_params, CannyEdgeParams):
        edges = cv2.Canny(gray_img,
                          threshold1=canny_edge_params.threshold1,
                          threshold2=canny_edge_params.threshold2,
                          apertureSize=canny_edge_params.aperture_size)
    else:
        print('Canny Edges Params: Invalid data type')
    return [color_img, gray_img, edges]

def find_contours(binary_img):
    pass
