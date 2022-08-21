import cv2
import numpy as np
import random

from ec.sec import StegoEllipticCurve
from lsbp.lsbp import LSBPlus
from sage.schemes.elliptic_curves.ell_point import EllipticCurvePoint
from tqdm import tqdm

from sklearn.cluster import KMeans


class ProgressBar:
    def __init__(self):
        self.tqdm = tqdm(range(100))
        self._completed = 0

    def update_by(self, progress: float, message: str = None):
        self._completed += progress
        self.tqdm.update(self._completed)

        if message is not None:
            self.tqdm.set_description(message)

        self.tqdm.refresh()

    def complete(self):
        self.tqdm.close()


def demonstrate_embedding(dir_name: str, f_name: str, stego_curve: StegoEllipticCurve, recip_key_u: EllipticCurvePoint, secret: int) -> tuple[list[int], np.ndarray]:
    centroid_coords = np.array(stego_curve.generate_points(recip_key_u))

    p_bar = ProgressBar()

    img = cv2.imread(f'{dir_name}/{f_name}')
    # img = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    img_f = np.float32(img * 252)

    centroids = img_f[centroid_coords[:, 0], centroid_coords[:, 1]]
    n_clusters = len(centroids)
    original_shape = img.shape

    img = img.reshape((-1, 3))
    img_f = img_f.reshape((-1, 3))

    p_bar.update_by(10, f'Loading image {dir_name}/{f_name}... DONE!, commencing clustering...')

    # Fitting K-Means to the dataset
    kmeans = KMeans(n_clusters=n_clusters, init=centroids, max_iter=1, n_init=1)
    labels = kmeans.fit_predict(img_f)  # TODO: Check if this method is correct
    np_labels = np.array(labels)

    p_bar.update_by(15, f'Clustering is complete. Commencing key generation...')

    d_lbl_cent = {
        n: {
            'c': centroids[n].tolist(),
            'i': np.where(np_labels == n)[0].tolist()
        } for n in list(set(labels))}

    keys = random.sample(range(16, 255), n_clusters)  # TODO: Think of the range & key exchange

    p_bar.update_by(5, f'Key generation is complete. Commencing embedding...')

    lsb_plus = LSBPlus()
    embed_payload = []
    out_img = [None] * img.shape[0]
    out_block_order = []

    for c_index in d_lbl_cent:
        out_block_order.extend(d_lbl_cent[c_index]['i'])
        for b_index in d_lbl_cent[c_index]['i']:
            c_blocks = img[b_index].tolist()
            embed_payload.extend(list(zip([keys[c_index]] * len(c_blocks), c_blocks)))

    p_bar.update_by(60 / img.shape[0], f'Embedding {secret:0b}...')

    embed_res, secret = lsb_plus.embed(secret, embed_payload)

    for i in range(img.shape[0]):
        out_img[out_block_order[i]] = [embed_res[(i * 3) + 0], embed_res[(i * 3) + 1], embed_res[(i * 3) + 2]]

    p_bar.update_by(0, f'Embedding secret is completed. Writing image file to output/{f_name}...')

    # print(img.tolist())
    # print(embed_res)
    embed_res = np.reshape(np.array(out_img), original_shape)
    cv2.imwrite(f'output/{f_name}', embed_res)

    p_bar.update_by(10, f'Embedding completed!')
    p_bar.complete()
    return keys, embed_res


def demonstrate_extraction(dir_name: str, f_name: str, stego_curve: StegoEllipticCurve, recip_key_u: EllipticCurvePoint, expected_secret: int, keys: list[int]) -> int:
    centroid_coords = np.array(stego_curve.generate_points(recip_key_u))

    p_bar = ProgressBar()

    img = cv2.imread(f'{dir_name}/{f_name}')
    # img = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    img_f = np.float32(img * 252)

    centroids = img_f[centroid_coords[:, 0], centroid_coords[:, 1]]
    n_clusters = len(centroids)

    img = img.reshape((-1, 3))
    img_f = img_f.reshape((-1, 3))

    p_bar.update_by(10, f'Loading stego image {dir_name}/{f_name}... DONE!, commencing clustering...')

    # Fitting K-Means to the dataset
    kmeans = KMeans(n_clusters=n_clusters, init=centroids, max_iter=1, n_init=1)
    labels = kmeans.fit_predict(img_f)  # TODO: Check if this method is correct
    np_labels = np.array(labels)

    p_bar.update_by(20, f'Clustering is complete. Commencing retrieval...')

    d_lbl_cent = {
        n: {
            'c': centroids[n].tolist(),
            'i': np.where(np_labels == n)[0].tolist()
        } for n in list(set(labels))}

    lsb_plus = LSBPlus()
    carrier_payload = []

    for c_index in d_lbl_cent:
        for b_index in d_lbl_cent[c_index]['i']:
            c_blocks = img[b_index].tolist()
            carrier_payload.extend(list(zip([keys[c_index]] * len(c_blocks), c_blocks)))
    # print(carrier_payload)
    p_bar.update_by(60 / img.shape[0], f'Extracting secret...')

    extracted_secret = lsb_plus.extract(carrier_payload) & expected_secret

    p_bar.update_by(5, f'Extracting secret is completed. Comparing with the expected...')
    message = f'{extracted_secret:0b} == {expected_secret:0b} ? {True if extracted_secret == expected_secret else False}'

    p_bar.update_by(5, f'Extraction completed!')
    p_bar.complete()

    print(message)
    return extracted_secret


if __name__ == '__main__':
    sec_a = StegoEllipticCurve(5, 2, 1, 3)
    sec_b = StegoEllipticCurve(5, 2, 1, 2)

    p_a = sec_a.key_u
    p_b = sec_b.key_u

    kys, res = demonstrate_embedding('test_data', 'test1_sm.png', sec_a, p_b, 5127)
    ex_secret = demonstrate_extraction('output', 'test1_sm.png', sec_b, p_a, 5127, kys)
    exit()
