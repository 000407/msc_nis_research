import cv2
import numpy as np

from math import log10, sqrt
from skimage.metrics import structural_similarity


def mse(path_a, path_b):
    im_a = cv2.imread(path_a)
    im_b = cv2.imread(path_b)

    gray_a = cv2.cvtColor(im_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(im_b, cv2.COLOR_BGR2GRAY)

    return np.mean((gray_a - gray_b) ** 2)


def psnr(path_a, path_b):
    mse_v = mse(path_a, path_b)
    if mse_v == 0:
        return 100

    max_pixel = 255.0
    return 20 * log10(max_pixel / sqrt(mse_v))


def ssim(path_a, path_b):
    im_a = cv2.imread(path_a)
    im_b = cv2.imread(path_b)

    gray_a = cv2.cvtColor(im_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(im_b, cv2.COLOR_BGR2GRAY)

    (score, diff) = structural_similarity(gray_a, gray_b, full=True)

    return score
