# Crop

import os
import cv2
import numpy as np
from LivestockCV.core import plot_image
from LivestockCV.core import print_image
from LivestockCV.core import params


def crop(img, x, y, h, w):

    params.device += 1

    if len(np.shape(img)) > 2 and np.shape(img)[-1] > 3:
        ref_img = img[:, :, [0]]
        ref_img = np.transpose(np.transpose(ref_img)[0])
        cropped = img[y:y + h, x:x + w, :]
    else:
        ref_img = np.copy(img)
        cropped = img[y:y + h, x:x + w]


    pt1 = (x, y)
    pt2 = (x + w - 1, y + h - 1)

    ref_img = cv2.rectangle(img=ref_img, pt1=pt1, pt2=pt2, color=(0, 255, 0), thickness=params.line_thickness)

    if params.debug == "print":
        print_image(ref_img, os.path.join(params.debug_outdir, str(params.device) + "_crop.png"))
    elif params.debug == "plot":
        plot_image(ref_img)

    return cropped
