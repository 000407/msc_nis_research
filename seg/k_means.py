import numpy as np
import cv2
import matplotlib.pyplot as plt

if __name__ == '__main__':
    original_image = cv2.imread("input/test1_sm.png")
    img = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    vectorized = np.float32(img.reshape((-1, 3)))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    K = 7
    attempts = 10
    ret, label, center = cv2.kmeans(vectorized, K, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)

    center = np.uint8(center)

    res = center[label.flatten()]
    result_image = res.reshape(img.shape)

    figure_size = 15
    plt.figure(figsize=(figure_size, figure_size))
    plt.subplot(1, 2, 1), plt.imshow(img)
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(1, 2, 2), plt.imshow(result_image)
    plt.title('Segmented Image when K = %i' % K), plt.xticks([]), plt.yticks([])
    plt.show()

    print('YES' if cv2.imwrite('output/test1_clusters.jpg', result_image) else 'NO')

    exit()
