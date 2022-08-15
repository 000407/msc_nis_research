import numpy as np
import skimage.color
import skimage.io
import matplotlib.pyplot as plt
# %matplotlib widget
import argparse


def hist(path):
    image = skimage.io.imread(fname=path, as_gray=True)

    fig, ax = plt.subplots()
    plt.imshow(image, cmap='gray')
    plt.show()

    histogram, bin_edges = np.histogram(image, bins=256, range=(0, 1))

    plt.figure()
    plt.title('Grayscale Histogram')
    plt.xlabel('grayscale value')
    plt.ylabel('pixel count')
    plt.xlim([0.0, 1.0])

    plt.plot(bin_edges[0:-1], histogram)
    plt.show()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--path', required=True, help='Path of the image file')
    args = vars(ap.parse_args())

    hist(args['path'])
    exit()
