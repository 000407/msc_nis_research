import os

import matplotlib.pyplot as plt
import pandas as pd

from db.mongo import MongoClient, CollectionName


def conf_plots(sub_figs, df, x):
    axs_t = sub_figs[0].subplots(1, 1)
    sub_figs[0].suptitle('MSE Variation', fontsize=15, fontweight='bold')
    axs_t.plot(x, df.loc[:, 'mse'])

    axs_m = sub_figs[1].subplots(1, 1)
    sub_figs[1].suptitle('PSNR Variation', fontsize=15, fontweight='bold')
    axs_m.plot(x, df.loc[:, 'psnr'])

    axs_b = sub_figs[2].subplots(1, 1)
    sub_figs[2].suptitle('SSIM Variation', fontsize=15, fontweight='bold')
    axs_b.plot(x, df.loc[:, 'ssim'])

    axs_t.set_ylabel(' ')
    axs_m.set_ylabel('Value')
    axs_b.set_ylabel(' ')


def plot_const_secret_dip_variation_idx(mongo_client: MongoClient, save_plot: bool = False, out_dir: str = ''):
    df = pd.DataFrame.from_records(list(mongo_client.find_all(CollectionName.DIP_CONST_SECRET_TEST)))

    fig = plt.figure(constrained_layout=True, figsize=(15, 12))
    sub_figs = fig.subfigures(3, 1, wspace=0.07)

    conf_plots(sub_figs, df, df.index)

    fig.suptitle('DIP Measures Variation: Sample Indices', fontsize=18, fontweight='bold')

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

    conf_plots(sub_figs, df, range(len(df.index)))

    fig.suptitle('DIP Measures Variation: Pixel Count', fontsize=18, fontweight='bold')

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
