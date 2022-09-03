import os
import numpy as np

import matplotlib.pyplot as plt
import pandas as pd

from db.mongo import MongoClient, CollectionName
from plotutils import conf_plots_dip_vs


def make_plot_for_spec(spec: dict):
    fig = plt.figure(constrained_layout=True, figsize=(15, 12))
    sub_figs = fig.subfigures(len(spec['plots']), 1, wspace=0.07)

    for i in range(spec['plots'].shape[0]):
        ps = spec['plots'][i]
        kw_args = ps.get('kw_args', {})
        conf_plots_dip_vs(sub_figs, spec['df'], spec['x'], i, ps['column_name'], ps['title'], **kw_args)

    fig.suptitle(spec['suptitle'], fontsize=18, fontweight='bold')

    if spec['save_fig']:
        out_dir = spec['out_dir'].strip('/')
        out_dir = f'/{out_dir}' if out_dir else ''
        plot_dir = f'../output/variations/{out_dir}'

        out_fname = spec.get('out_fname', 'output.png')

        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)

        plot_path = f'{plot_dir}/{out_fname}'
        plt.savefig(plot_path)

    plt.show()
    plt.close(fig)


def plot_const_secret_dip_variation_idx(mongo_client: MongoClient, save_fig: bool = False, out_dir: str = ''):
    df = pd.DataFrame.from_records(list(mongo_client.find_all(CollectionName.DIP_RFLS_VS_WOW_TEST)))
    suptitle = 'DIP Measures Variation: Same Secret in Different Carriers - WOW vs. LSB+'
    kw_args = {
        'ticklabel_fmt_offset': False
    }

    sp = {
        'suptitle': suptitle,
        'df': df,
        'x': df.index,
        'save_fig': save_fig,
        'out_dir': out_dir,
        'out_fname': 'dip_rfls_wow_vs_psnr',
        'plots': np.array([
            {
                'title': 'PSNR (LSB+ Embedding)',
                'column_name': 'psnr_lsbp',
                'kw_args': kw_args
            },
            {
                'title': 'PSNR (WOW Embedding)',
                'column_name': 'psnr_wow',
                'kw_args': kw_args
            }
        ])
    }
    make_plot_for_spec(sp)

    sp['plots'] = np.array([
        {
            'title': 'MSE (LSB+ Embedding)',
            'column_name': 'mse_lsbp',
            'kw_args': kw_args
        },
        {
            'title': 'MSE (WOW Embedding)',
            'column_name': 'mse_wow',
            'kw_args': {
                'ticklabel_fmt_offset': False
            }
        }
    ])
    sp['out_fname'] = 'dip_rfls_wow_vs_mse'
    make_plot_for_spec(sp)

    sp['plots'] = np.array([
        {
            'title': 'SSIM (LSB+ Embedding)',
            'column_name': 'ssim_lsbp',
            'kw_args': kw_args
        },
        {
            'title': 'SSIM (WOW Embedding)',
            'column_name': 'ssim_wow',
            'kw_args': kw_args
        }
    ])
    sp['out_fname'] = 'dip_rfls_wow_vs_ssim'
    make_plot_for_spec(sp)


if __name__ == '__main__':
    client = MongoClient()
    plot_const_secret_dip_variation_idx(client, save_fig=True, out_dir='dip_rfls_wow_vs')
    exit()
