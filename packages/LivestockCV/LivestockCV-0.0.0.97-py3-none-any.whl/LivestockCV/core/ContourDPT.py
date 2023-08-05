# ContourDPT


# my basic libraries 
import cv2
from LivestockCV.core import show_image


def Contour_DPT(img, contouredimg, epsilon):
    thresh_copy = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB) 
    perimeter = cv2.arcLength(contours, True)
    e = epsilon * perimeter 
    transformed_contour = cv2.approxPolyDP(contours, epsilon = e, closed = True)
    cv2.drawContours(thresh_copy, [ transformed_contour ], contourIdx=-1, color=(250, 255, 0), thickness=2) 
    print('', transformed_contour.shape[0])
    show_image(thresh_copy)