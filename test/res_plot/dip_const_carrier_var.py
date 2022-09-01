import os

import matplotlib.pyplot as plt
import pandas as pd

from util import conf_plots
from db.mongo import MongoClient, CollectionName


def plot_const_carrier_dip_variation_idx(mongo_client: MongoClient, save_plot: bool = False, out_dir: str = ''):
    df = pd.DataFrame.from_records(list(mongo_client.find_all(CollectionName.DIP_RANDOM_FIXED_LENGTH_SECRET_TEST)))

    fig = plt.figure(constrained_layout=True, figsize=(15, 12))
    sub_figs = fig.subfigures(3, 1, wspace=0.07)

    conf_plots(sub_figs, df, df.index)

    fig.suptitle('DIP Measures Variation: Random Fixed-Length Secret; Same Carrier', fontsize=18, fontweight='bold')

    if save_plot:
        out_dir = out_dir.strip('/')
        out_dir = f'/{out_dir}' if out_dir else ''
        plot_dir = f'../output/variations/{out_dir}'

        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)

        plot_path = f'{plot_dir}/dipm_ccv_vs_idx.png'
        plt.savefig(plot_path)

    plt.show()
    plt.close(fig)


if __name__ == '__main__':
    client = MongoClient()
    plot_const_carrier_dip_variation_idx(client, save_plot=True, out_dir='dip_ccv')
    exit()
