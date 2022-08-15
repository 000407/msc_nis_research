import argparse

from math import log10, sqrt
from mse import mse as f_mse


def psnr(path_a, path_b):
    mse = f_mse(path_a, path_b)
    if mse == 0:
        return 100

    max_pixel = 255.0
    return 20 * log10(max_pixel / sqrt(mse))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--first", required=True, help="Directory of the image that will be compared")
    ap.add_argument("-s", "--second", required=True, help="Directory of the image that will be used to compare")
    args = vars(ap.parse_args())

    print(f'PSNR Score: {psnr(args["first"], args["second"])}')
    exit()
