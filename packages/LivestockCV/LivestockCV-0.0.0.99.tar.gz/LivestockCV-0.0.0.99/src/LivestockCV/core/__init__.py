# Versioning
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions



import os
import matplotlib

from LivestockCV.core.classes import Params
from LivestockCV.core.classes import Outputs
from LivestockCV.core.fatal_error import fatal_error


params = Params()
outputs = Outputs()


from LivestockCV.core.deprecation_warning import deprecation_warning
from LivestockCV.core.print_image import print_image
from LivestockCV.core.plot_image import plot_image
from LivestockCV.core.color_palette import color_palette
from LivestockCV.core.rgb2gray import rgb2gray
from LivestockCV.core.rgb2gray_hsv import rgb2gray_hsv
from LivestockCV.core.rgb2gray_lab import rgb2gray_lab
from LivestockCV.core import transform
from LivestockCV.core.apply_mask import apply_mask
from LivestockCV.core.crop import crop
from LivestockCV.core.invert import invert
from LivestockCV.core.rotate import rotate
from LivestockCV.core import roi
from LivestockCV.core import threshold
from LivestockCV.core.gaussian_blur import gaussian_blur
from LivestockCV.core.analyze_color import analyze_color
from LivestockCV.core.frame_count import frame_count
from LivestockCV.core import js_to_image
from LivestockCV.core import bbox_to_bytes
from LivestockCV.core import take_photo
from LivestockCV.core.show_image import show_image
from LivestockCV.core.CalculateAngle import calculate_Angle
from LivestockCV.core.dimensions import dimensions
from LivestockCV.core.cannyedge_detect import cannyedge_detector
from LivestockCV.core.dilate import dilate
from LivestockCV.core.erode import erode
from LivestockCV.core.contours import contour, contour_max


