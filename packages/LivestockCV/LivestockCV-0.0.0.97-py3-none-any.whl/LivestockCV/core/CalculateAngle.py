# Calculate Angle


# my basic libraries 
import cv2
import os
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageOps

# For CalculateAngle function
from math import atan2, degrees
from operator import itemgetter
from pprint import pprint



def calculate_Angle(point1,point2,point3):
    x1,y1 = point1
    x2,y2 = point2
    x3,y3 = point3
    deg = degrees(atan2(point3[1] - point2[1], point3[0] - point2[0]) - atan2(point1[1] - point2[1], point1[0] - point2[0]))
    return deg * -1 if deg < 0 else -1 * (deg - 360) # here is some transformation so we don't get get negative angles