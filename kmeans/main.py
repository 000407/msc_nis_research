import cv2
import matplotlib.pyplot as plt
import numpy as np
import random

from tqdm import tqdm

from sklearn.cluster import KMeans


def clusterize(path: str, n_clusters: int, random_state: int):
    p_bar = tqdm(range(100))

    original_image = cv2.imread(path)
    img = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    img = np.float32(img.reshape((-1, 3)))

    p_bar.update(10)
    p_bar.refresh()

    # Fitting K-Means to the dataset
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=random_state)
    y_kmeans = kmeans.fit_predict(img)
    p_bar.update(65)
    p_bar.refresh()

    plt.rcParams["figure.figsize"] = [3 * i for i in plt.rcParams["figure.figsize"]]
    ax = plt.figure().add_subplot(projection='3d')

    # for x in range(y_kmeans.shape[0]):
    #     plt.annotate(f'[{X[x][0]}, {X[x][1]}, {X[x][2]}]', (X[x][0], X[x][1]))

    # Visualising the clusters
    for i in range(3):
        # print(X[y_kmeans == i, 0], X[y_kmeans == i, 1], X[y_kmeans == i, 2])
        ax.scatter(img[y_kmeans == i, 0], img[y_kmeans == i, 1], img[y_kmeans == i, 2],
                   s=100, c=f'#{"".join(random.choice("0123456789abcdef") for c in range(6))}',
                   label=f'Cluster {i + 1}')
    p_bar.update(80)
    p_bar.refresh()

    ax.scatter(kmeans.cluster_centers_[:, 0],
               kmeans.cluster_centers_[:, 1],
               kmeans.cluster_centers_[:, 2], s=300, c='yellow', label='Centroids')

    plt.title(f'Pixel Clusters: {path}')
    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')
    # plt.legend()
    plt.show()

    p_bar.update(100)
    p_bar.refresh()


if __name__ == '__main__':
    # for i in range(6):
    clusterize('test_data/test1.jpg', 3, 42)

    exit()
