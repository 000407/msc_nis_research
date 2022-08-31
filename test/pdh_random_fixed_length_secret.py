import random
import time

from db.mongo import *
from dip_tests.dip import *
from ec.sec import StegoEllipticCurve
from lsbp_stego.lsbp_stego import LSBPlusStego
from steganalysis.pd_hist import hist_rgb


def get_random_secret(length: int):
    secret = 0
    for i in range(length):
        secret = (secret << 1) | random.randrange(2)

    return secret


def random_fixed_length_secret_histogram():
    client = MongoClient()
    c_name = 'img_0001'
    carrier = client.find_one_by(
        {
            'collection': CollectionName.CARRIER,
            'query': {
                'name': f'{c_name}.png'
            }
        }
    )

    if carrier:
        for s_obj in os.listdir('./output/rfls'):
            c_path = f"{carrier['path']}/{carrier['name']}"
            s_path = f"./output/rfls/{s_obj}"

            print(f'Generating histogram data for {c_path} & {s_path}...', end='')
            data = {
                'carrierId': carrier['_id'],
                'stegoPath': s_path,
                'histogramData': hist_rgb(c_path, s_path, make_plot=True, save_plot=True, out_dir='pdh_cs')
            }
            print(f' completed; Saving data to db...', end='')

            client.insert_one(
                {
                    'collection': CollectionName.PDH_CONST_CARRIER_TEST,
                    'data': data
                }
            )
            print(' DONE!')


if __name__ == '__main__':
    random_fixed_length_secret_histogram()
    exit()
