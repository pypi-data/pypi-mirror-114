# Contour


# my basic libraries 
import cv2
from LivestockCV.core import show_image

def contour_max(img):
    contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = max(contours, key= cv2.contourArea)
    cv2.drawContours(img, contours, -1, (255, 100, 200), 2)
    show_image(img)
    
def contour(img):
    contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img, contours, -1, (255, 100, 200), 2)
    show_image(img)