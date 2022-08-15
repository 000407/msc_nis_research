from skimage.metrics import structural_similarity
import argparse
import cv2


def ssim(path_a, path_b):
    im_a = cv2.imread(path_a)
    im_b = cv2.imread(path_b)

    gray_a = cv2.cvtColor(im_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(im_b, cv2.COLOR_BGR2GRAY)

    (score, diff) = structural_similarity(gray_a, gray_b, full=True)
    # diff = (diff * 255).astype("uint8")

    return score


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--first", required=True, help="Directory of the image that will be compared")
    ap.add_argument("-s", "--second", required=True, help="Directory of the image that will be used to compare")
    args = vars(ap.parse_args())

    print(f'SSIM Score: {ssim(args["first"], args["second"])}')
    exit()
