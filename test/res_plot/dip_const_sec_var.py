import os

import matplotlib.pyplot as plt
import pandas as pd

from db.mongo import MongoClient, CollectionName
from plotutils import conf_plots_dip_all


def plot_const_secret_dip_variation_idx(mongo_client: MongoClient, save_plot: bool = False, out_dir: str = ''):
    df = pd.DataFrame.from_records(list(mongo_client.find_all(CollectionName.DIP_CONST_SECRET_TEST)))

    fig = plt.figure(constrained_layout=True, figsize=(15, 12))
    sub_figs = fig.subfigures(3, 1, wspace=0.07)

    conf_plots_dip_all(sub_figs, df, df.index)

    fig.suptitle('DIP Measures Variation: Same Secret in Different Carriers (by Sample Index)', fontsize=18, fontweight='bold')

    if save_plot:
        out_dir = out_dir.strip('/')
        out_dir = f'/{out_dir}' if out_dir else ''
        plot_dir = f'../output/variations/{out_dir}'

        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)

        plot_path = f'{plot_dir}/dipm_vs_idx.png'
        plt.savefig(plot_path)

    plt.show()
    plt.close(fig)


def plot_const_secret_dip_variation_px_count(mongo_client: MongoClient, save_plot: bool = False, out_dir: str = ''):
    pipeline = [
        {
            '$lookup': {
                'from': CollectionName.CARRIER.name,
                'localField': 'carrierId',
                'foreignField': '_id',
                'as': 'carrier'
            }
        },
        {
            '$set': {
                'carrier': {
                    '$first': '$carrier'
                }
            }
        },
        {
            '$set': {
                'carrierSize': {
                    '$multiply': ['$carrier.width', '$carrier.height']
                }
            }
        },
        {
            '$unset': ['carrierId', 'carrier']
        }
    ]

    df = pd.DataFrame \
        .from_records(list(mongo_client.aggregate(CollectionName.DIP_CONST_SECRET_TEST, pipeline))) \
        .sort_values(by=['carrierSize'])

    fig = plt.figure(constrained_layout=True, figsize=(15, 12))
    sub_figs = fig.subfigures(3, 1, wspace=0.07)

    conf_plots_dip_all(sub_figs, df, range(len(df.index)))

    fig.suptitle('DIP Measures Variation: Same Secret in Different Carriers (by Pixel Count)', fontsize=18, fontweight='bold')

    if save_plot:
        out_dir = out_dir.strip('/')
        out_dir = f'/{out_dir}' if out_dir else ''
        plot_dir = f'../output/variations/{out_dir}'

        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)

        plot_path = f'{plot_dir}/dipm_vs_px_count.png'
        plt.savefig(plot_path)

    plt.show()
    plt.close(fig)


if __name__ == '__main__':
    client = MongoClient()
    plot_const_secret_dip_variation_idx(client, save_plot=True, out_dir='dip_csv')
    plot_const_secret_dip_variation_px_count(client, save_plot=True, out_dir='dip_csv')
    exit()
