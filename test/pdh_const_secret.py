from db.mongo import *
from steganalysis.pd_hist import hist_rgb


def same_secret_different_carriers_histogram():
    client = MongoClient()

    carriers = list(client.find_all(CollectionName.CARRIER))

    for c in carriers:
        c_path = f"{c['path']}/{c['name']}"
        s_path = f"./output/cl/{c['name']}"

        print(f'Generating histogram data for {c_path} & {s_path}...', end='')
        data = {
            'carrierId': c['_id'],
            'stegoPath': s_path,
            'histogramData': hist_rgb(c_path, s_path, make_plot=True, save_plot=True, out_dir='pdh_cs')
        }
        print(f' completed; Saving data to db...', end='')

        client.insert_one(
            {
                'collection': CollectionName.PDH_CONST_SECRET_TEST,
                'data': data
            }
        )
        print(' DONE!')


if __name__ == '__main__':
    same_secret_different_carriers_histogram()
