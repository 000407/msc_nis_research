import random
import time

from db.mongo import *
from dip_tests.dip import *
from ec.sec import StegoEllipticCurve
from lsbp_stego.lsbp_stego import LSBPlusStego


def get_random_secret(length: int):
    secret = 0
    for i in range(length):
        secret = (secret << 1) | random.randrange(2)

    return secret


def random_fixed_length_secret_test():
    client = MongoClient()
    c_name = 'img_0001'
    obj = client.find_one_by(
        {
            'collection': CollectionName.CARRIER,
            'query': {
                'name': f'{c_name}.png'
            }
        }
    )

    if obj:
        sec_a = StegoEllipticCurve(1049, 1672, 4562, 403)
        sec_b = StegoEllipticCurve(1049, 1672, 4562, 343)

        stego = LSBPlusStego(sec_a)

        for i in range(57, 500):
            secret = get_random_secret(1600 * 3)
            print(f'Embedding sample: {(i + 1):03d}...', end='')

            start = time.time()
            path_i = os.path.abspath(f'./test_data/carrier/{c_name}.png')
            path_o = os.path.abspath(f'./output/rfls/{c_name}_{i:07d}.png')

            kys, embed = stego.embed(path_i, path_o, sec_b.key_u, secret)
            end = time.time()
            print(f' completed; time elapsed: {end - start}; Performing DIP tests..', end='')

            mse_v = mse(path_i, path_o)
            psnr_v = psnr(path_i, path_o)
            ssim_v = ssim(path_i, path_o)
            print(f' completed; Writing results to db... ', end='')

            data = {
                'carrierId': obj['_id'],
                'index': i + 1,
                'secret': str(secret),
                'secretLength': secret.bit_length(),
                'timeElapsed': end - start,
                'psnr': psnr_v,
                'ssim': ssim_v,
                'mse': mse_v
            }
            client.insert_one({
                'collection': CollectionName.DIP_RANDOM_FIXED_LENGTH_SECRET_TEST,
                'data': data
            })
            print(' DONE!')


if __name__ == '__main__':
    random_fixed_length_secret_test()
    exit()
