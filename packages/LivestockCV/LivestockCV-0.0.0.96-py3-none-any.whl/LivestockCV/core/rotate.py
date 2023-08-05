# Rotate an image

import os
import cv2
import numpy as np
from LivestockCV.core import print_image
from LivestockCV.core import plot_image
from LivestockCV.core import params


def rotate(img, rotation_deg):

    # Here we're going to input our parameters 
    iy, ix = np.shape(img)[:2]
    m = cv2.getRotationMatrix2D((ix / 2, iy / 2), rotation_deg, 1)
    cos = np.abs(m[0, 0])
    sin = np.abs(m[0, 1])
    nw = int((iy * sin) + (ix * cos))
    nh = int((iy * cos) + (ix * sin))
    m[0, 2] += (nw / 2) - (ix / 2)
    m[1, 2] += (nh / 2) - (iy / 2)

    rotated_img = cv2.warpAffine(img, m, (nw, nh))


    params.device += 1

    if params.debug == 'print':
        print_image(rotated_img, os.path.join(params.debug_outdir,
                                              str(params.device) + '_' + str(rotation_deg) + '_rotated_img.png'))

    elif params.debug == 'plot':
        if len(np.shape(img)) == 3:
            plot_image(rotated_img)
        else:
            plot_image(rotated_img, cmap='gray')

    return rotated_img
