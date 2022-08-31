import random
import time

from db.mongo import *
from dip_tests.dip import *
from ec.sec import StegoEllipticCurve
from lsbp_stego.lsbp_stego import LSBPlusStego


def same_secret_different_carriers():
    client = MongoClient()

    secret = 1
    for i in range(1050 * 3):  # To compensate the carrier with the smallest dimension
        secret = (secret << 1) | random.randrange(2)
    print(f'Secret: {secret}')

    sec_a = StegoEllipticCurve(1049, 1672, 4562, 403)
    sec_b = StegoEllipticCurve(1049, 1672, 4562, 343)
    stego = LSBPlusStego(sec_a)
    carriers = list(client.find_all(CollectionName.CARRIER))

    for c in carriers:
        print(f'Embedding secret in carrier: {c["name"]})...', end='')

        start = time.time()
        path_i = os.path.abspath(f'./test_data/carrier/{c["name"]}')
        path_o = os.path.abspath(f'./output/cl/{c["name"]}')

        kys, embed = stego.embed(path_i, path_o, sec_b.key_u, secret)
        end = time.time()
        print(f' completed; time elapsed: {end - start}; Performing DIP tests..', end='')

        mse_v = mse(path_i, path_o)
        psnr_v = psnr(path_i, path_o)
        ssim_v = ssim(path_i, path_o)
        print(f' completed; Writing results to db... ', end='')

        data = {
            'carrierId': c['_id'],
            'secretLength': secret.bit_length(),
            'timeElapsed': end - start,
            'psnr': psnr_v,
            'ssim': ssim_v,
            'mse': mse_v
        }
        client.insert_one({
            'collection': CollectionName.DIP_CONST_SECRET_TEST,
            'data': data
        })
        print(' DONE!')


if __name__ == '__main__':
    same_secret_different_carriers()
