from skimage.metrics import mean_squared_error
import argparse
import cv2
import numpy as np


def mse(path_a, path_b):
    im_a = cv2.imread(path_a)
    im_b = cv2.imread(path_b)

    gray_a = cv2.cvtColor(im_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(im_b, cv2.COLOR_BGR2GRAY)

    return np.mean((gray_a - gray_b) ** 2)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--first", required=True, help="Directory of the image that will be compared")
    ap.add_argument("-s", "--second", required=True, help="Directory of the image that will be used to compare")
    args = vars(ap.parse_args())

    print(f'MSE Score: {mse(args["first"], args["second"])}')
    exit()
