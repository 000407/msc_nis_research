import os

import matplotlib.pyplot as plt
import pandas as pd

from plotutils import conf_plots_dip_all
from db.mongo import MongoClient, CollectionName


def plot_inc_secret_len_dip_variation_idx(mongo_client: MongoClient, save_plot: bool = False, out_dir: str = ''):
    df = pd.DataFrame.from_records(list(mongo_client.find_all(CollectionName.DIP_SECRET_LENGTH_TEST)))

    for i in range(4):
        df_sub = df[500 * i: (500 * (i + 1))]
        fig = plt.figure(constrained_layout=True, figsize=(15, 12))
        sub_figs = fig.subfigures(3, 1, wspace=0.07)

        conf_plots_dip_all(sub_figs, df_sub, df_sub.loc[:, 'secretLength'])

        fig.suptitle(f'DIP Measures Variation: Increasing Length Secret (Samples {500 * i} - {(500 * (i + 1))}); Same Carrier', fontsize=18, fontweight='bold')

        if save_plot:
            out_dir = out_dir.strip('/')
            out_dir = f'/{out_dir}' if out_dir else ''
            plot_dir = f'../output/variations/{out_dir}'

            if not os.path.exists(plot_dir):
                os.makedirs(plot_dir)

            plot_path = f'{plot_dir}/dipm_isl_vs_len_{500 * i}_{(500 * (i + 1))}.png'
            plt.savefig(plot_path)

        plt.show()
        plt.close(fig)


if __name__ == '__main__':
    client = MongoClient()
    plot_inc_secret_len_dip_variation_idx(client, save_plot=True, out_dir='dip_islv')
    exit()
