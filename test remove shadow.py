import cv2
import numpy as np

img = cv2.imread("clock8.png")
cv2.imshow('org img', img)


def shadow_remove(shadow_img):
    rgb_planes = cv2.split(shadow_img)
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_norm_planes.append(norm_img)
    img_without_shadow = cv2.merge(result_norm_planes)
    return img_without_shadow


shad = shadow_remove(img)
cv2.imshow('img without shadow', shad)

gray_img = cv2.cvtColor(shad, cv2.COLOR_BGR2GRAY)
gray_img = cv2.GaussianBlur(gray_img, ksize=(7, 7), sigmaX=0)
canny_edges = cv2.Canny(gray_img, 100, 150)
cv2.imshow('gray img', gray_img)
cv2.imshow('canny edges', canny_edges)

cv2.waitKey(0)
cv2.destroyAllWindows()
