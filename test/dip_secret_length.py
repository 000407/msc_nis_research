import random
import time

from db.mongo import *
from dip_tests.dip import *
from ec.sec import StegoEllipticCurve
from lsbp_stego.lsbp_stego import LSBPlusStego
from util import get_random_secret


def secret_len_test():
    client = MongoClient()
    c_name = 'img_0001.png'
    obj = client.find_one_by(
        {
            'collection': CollectionName.CARRIER,
            'query': {
                'name': c_name
            }
        }
    )

    if obj:
        sec_a = StegoEllipticCurve(1597, 1672, 4562, 403)
        sec_b = StegoEllipticCurve(1597, 1672, 4562, 343)

        stego = LSBPlusStego(sec_a)

        secret = get_random_secret(1)

        for i in range(0, 2000):
            secret_bit = random.randrange(2)
            secret = (secret << 1) | secret_bit
            print(f'Embedding secret (sample: {(i + 1):03d})...', end='')

            start = time.time()
            path_i = os.path.abspath('./test_data/carrier/img_0001.png')
            path_o = os.path.abspath(f'./output/sl/img_0001_{i:07d}.png')

            kys, embed = stego.embed(path_i, path_o, sec_b.key_u, secret)
            end = time.time()
            print(f' completed; time elapsed: {end - start}; Performing DIP tests..', end='')

            mse_v = mse(path_i, path_o)
            psnr_v = psnr(path_i, path_o)
            ssim_v = ssim(path_i, path_o)
            print(f' completed; Writing results to db... ', end='')

            data = {
                'index': i + 1,
                'secretLength': secret.bit_length(),
                'secretBit': secret_bit,
                'timeElapsed': end - start,
                'psnr': psnr_v,
                'ssim': ssim_v,
                'mse': mse_v
            }
            client.insert_one({
                'collection': CollectionName.DIP_SECRET_LENGTH_TEST,
                'data': data
            })
            print(' DONE!')


if __name__ == '__main__':
    secret_len_test()
    exit()
