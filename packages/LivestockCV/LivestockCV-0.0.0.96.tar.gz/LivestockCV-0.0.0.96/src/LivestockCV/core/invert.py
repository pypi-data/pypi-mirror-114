# Invert gray image

import cv2
import os
from LivestockCV.core import print_image
from LivestockCV.core import plot_image
from LivestockCV.core import params


def invert(gray_img):
    params.device += 1
    img_inv = cv2.bitwise_not(gray_img)
    if params.debug == 'print':
        print_image(img_inv, os.path.join(params.debug_outdir, str(params.device) + '_invert.png'))
    elif params.debug == 'plot':
        plot_image(img_inv, cmap='gray')
    return img_inv
