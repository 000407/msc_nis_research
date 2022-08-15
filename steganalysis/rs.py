from rs_util import *
import cv2
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib import cm
from tqdm import trange, tqdm
# from PIL import Image, ImageOps

if __name__ == '__main__':
    mask_size_w, mask_size_h = 8, 8
    mask = np.random.randint(low=0, high=2, size=(mask_size_w, mask_size_h))
    # print(mask)

    plt.title('Mask Size %dx%d' % mask.shape)
    plt.imshow(mask, cmap='gray')
    plt.axis('off')
    # plt.show()

    img_path = './input/test1.jpg'
    img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB).astype('int16')

    img_size_w, img_size_h = img.shape[0], img.shape[1]

    img_size_w = img_size_w if img_size_w % mask.shape[0] == 0 else img_size_w + (
                mask.shape[0] - img_size_w % mask.shape[0])
    img_size_h = img_size_h if img_size_h % mask.shape[1] == 0 else img_size_h + (
                mask.shape[1] - img_size_h % mask.shape[1])

    img = cv2.resize(img, (img_size_h, img_size_w), interpolation=cv2.INTER_AREA)

    plt.title('Image')
    plt.imshow(img)
    plt.axis('off')
    plt.show()

    print('shape', img.shape)

    print('Rm->%f\tSm->%f' % calculate_count_groups(img[:, :, 0], mask))
    print('R-m->%f\tS-m->%f' % calculate_count_groups(img[:, :, 0], -mask))

    r_m, s_m, r_neg_m, s_neg_m = [], [], [], []

    iter_count = 20
    range_iter = trange(iter_count, leave=True)

    channels = [img[:, :, k] for k in range(img.shape[2])]

    for i in range_iter:
        temp_rm, temp_sm, temp_r_neg_m, temp_s_neg_m = rs_helper(channels, mask, flip=True, percent=i * .05)

        r_m.append(temp_rm)
        r_neg_m.append(temp_r_neg_m)
        s_m.append(temp_sm)
        s_neg_m.append(temp_s_neg_m)

        range_iter.set_postfix_str('Rm->%f, R-m->%f, Sm->%f, S-m->%f' % (r_m[-1], r_neg_m[-1], s_m[-1], s_neg_m[-1]))
        range_iter.refresh()

    plt.title('RS Diagram')

    step = 0.05
    plt.plot(range(0, 100, int(step * 100)), 100 * np.array(r_m), 'r', label="Rm")
    plt.plot(range(0, 100, int(step * 100)), 100 * np.array(s_m), 'g', label='Sm')
    plt.plot(range(0, 100, int(step * 100)), 100 * np.array(r_neg_m), 'b', label='R-m')
    plt.plot(range(0, 100, int(step * 100)), 100 * np.array(s_neg_m), 'y', label='S-m')
    plt.legend()

    plt.savefig('./output/output-rs-diagram-%s.jpg' % img_path.strip().split('/')[-1].split('.bmp')[0].strip(),
                facecolor='w', edgecolor='none')
    plt.show()
    exit(0)
