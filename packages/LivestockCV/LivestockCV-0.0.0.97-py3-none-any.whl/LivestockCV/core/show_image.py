# Plot image to screen
import cv2
import numpy
import matplotlib
from LivestockCV.core import params
from matplotlib import pyplot as plt
from LivestockCV.core import fatal_error
from google.colab.patches import cv2_imshow

def show_image(img, cmap=None):
	cv2_imshow(img)
