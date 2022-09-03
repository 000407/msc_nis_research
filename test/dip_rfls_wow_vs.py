import time

from db.mongo import *
from dip_tests.dip import *
from ec.sec import StegoEllipticCurve
from ext_alg.WOW import demo_wow_embed
from lsbp_stego.lsbp_stego import LSBPlusStego
from util import get_random_secret


def rfls_vs_wow_test():
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

        for i in range(100):
            secret = get_random_secret(1600 * 3)
            print(f'Embedding sample: {(i + 1):03d}...', end='')

            start_l = time.time()
            path_i = os.path.abspath(f'./test_data/carrier/{c_name}.png')
            path_o_l = os.path.abspath(f'./output/rfls_bm/{c_name}_lsbp_{i:07d}.png')
            path_o_w = os.path.abspath(f'./output/rfls_bm/{c_name}_wow_{i:07d}.png')

            kys, embed = stego.embed(path_i, path_o_l, sec_b.key_u, secret)
            end_l = time.time()
            print(f' completed; time elapsed: {end_l - start_l}; Performing WOW embedding..', end='')

            start_w = time.time()
            demo_wow_embed(path_i, secret, path_o_w, True)
            end_w = time.time()
            print(f' completed; time elapsed: {end_w - start_w}; Performing DIP tests..', end='')

            mse_v_l = mse(path_i, path_o_l)
            psnr_v_l = psnr(path_i, path_o_l)
            ssim_v_l = ssim(path_i, path_o_l)

            mse_v_w = mse(path_i, path_o_w)
            psnr_v_w = psnr(path_i, path_o_w)
            ssim_v_w = ssim(path_i, path_o_w)
            print(f' completed; Writing results to db... ', end='')

            data = {
                'carrierId': obj['_id'],
                'index': i + 1,
                'secret': str(secret),
                'secretLength': secret.bit_length(),
                'timeElapsedLsbp': end_l - start_l,
                'timeElapsedWow': end_w - start_w,
                'psnr_lsbp': psnr_v_l,
                'ssim_lsbp': ssim_v_l,
                'mse_lsbp': mse_v_l,
                'psnr_wow': psnr_v_w,
                'ssim_wow': ssim_v_w,
                'mse_wow': mse_v_w
            }
            client.insert_one({
                'collection': CollectionName.DIP_RFLS_VS_WOW_TEST,
                'data': data
            })
            print(' DONE!')


if __name__ == '__main__':
    rfls_vs_wow_test()
    exit()
