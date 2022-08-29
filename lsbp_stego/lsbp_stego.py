import cv2
import numpy as np
import random

from ec.sec import StegoEllipticCurve
from lsbp.lsbp import LSBPlus
from sage.schemes.elliptic_curves.ell_point import EllipticCurvePoint
from sklearn.cluster import KMeans


class LSBPlusStego:
    def __init__(self, stego_curve: StegoEllipticCurve) -> None:
        self._stego_curve = stego_curve

    def embed(self, in_file: str, out_file: str, recip_key_u: EllipticCurvePoint, secret: int) \
            -> tuple[list[int], np.ndarray]:
        centroid_coords = np.array(self._stego_curve.generate_points(recip_key_u))

        img = cv2.imread(in_file)
        img_f = np.float32(img & 252)

        centroids = img_f[centroid_coords[:, 0], centroid_coords[:, 1]]
        n_clusters = len(centroids)
        original_shape = img.shape

        img = img.reshape((-1, 3))
        img_f = img_f.reshape((-1, 3))

        kmeans = KMeans(n_clusters=n_clusters, init=centroids, max_iter=1, n_init=1)
        labels = kmeans.fit_predict(img_f)
        np_labels = np.array(labels)

        d_lbl_cent = {
            n: {
                'c': centroids[n].tolist(),
                'i': np.where(np_labels == n)[0].tolist()
            } for n in list(set(labels))}

        keys = random.choices(range(16, 255), k=n_clusters)

        lsb_plus = LSBPlus()
        embed_payload = []
        out_img = [None] * img.shape[0]
        out_block_order = []

        for c_index in d_lbl_cent:
            out_block_order.extend(d_lbl_cent[c_index]['i'])
            for b_index in d_lbl_cent[c_index]['i']:
                c_blocks = img[b_index].tolist()
                embed_payload.extend(list(zip([keys[c_index]] * len(c_blocks), c_blocks)))

        embed_res, secret = lsb_plus.embed(secret, embed_payload)

        for i in range(img.shape[0]):
            out_img[out_block_order[i]] = [embed_res[(i * 3) + 0], embed_res[(i * 3) + 1], embed_res[(i * 3) + 2]]

        embed_res = np.reshape(np.array(out_img), original_shape)
        cv2.imwrite(out_file, embed_res)

        return keys, embed_res

    def extract(self, in_file: str, recip_key_u: EllipticCurvePoint, expected_secret: int, keys: list[int]) -> int:
        centroid_coords = np.array(self._stego_curve.generate_points(recip_key_u))

        img = cv2.imread(in_file)
        img_f = np.float32(img & 252)

        centroids = img_f[centroid_coords[:, 0], centroid_coords[:, 1]]
        n_clusters = len(centroids)

        img = img.reshape((-1, 3))
        img_f = img_f.reshape((-1, 3))

        kmeans = KMeans(n_clusters=n_clusters, init=centroids, max_iter=1, n_init=1)
        labels = kmeans.fit_predict(img_f)
        np_labels = np.array(labels)

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

        return lsb_plus.extract(carrier_payload) & expected_secret
