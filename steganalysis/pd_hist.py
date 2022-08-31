import os
import time
from enum import Enum

import numpy as np
import skimage.color
import skimage.io
import matplotlib.pyplot as plt
import argparse


class ColorChannel(Enum):
    RED = ('Red', 'red')
    GREEN = ('Green', 'green')
    BLUE = ('Blue', 'blue')


def conf_plot(ax, ch: ColorChannel, hist, bins, with_title=False):
    width = 1 * (bins[1] - bins[0])
    ax.bar(range(len(bins) - 1), hist, align='center', width=width, color=ch.value[1])
    if with_title:
        ax.set_title(ch.name.capitalize())


def hist_rgb(o_path, s_path, make_plot: bool = False, save_plot: bool = False, out_dir: str = None):
    bin_size = 256
    plot_path = None

    orig = skimage.io.imread(fname=os.path.abspath(o_path))
    steg = skimage.io.imread(fname=os.path.abspath(s_path))

    h1r, be1r = np.histogram(orig[:, :, 0], bins=bin_size)
    h1g, be1g = np.histogram(orig[:, :, 1], bins=bin_size)
    h1b, be1b = np.histogram(orig[:, :, 2], bins=bin_size)

    h2r, be2r = np.histogram(steg[:, :, 0], bins=bin_size)
    h2g, be2g = np.histogram(steg[:, :, 1], bins=bin_size)
    h2b, be2b = np.histogram(steg[:, :, 2], bins=bin_size)

    if make_plot:
        fig = plt.figure(constrained_layout=True, figsize=(15, 12))
        sub_figs = fig.subfigures(3, 1, wspace=0.07)

        axs_t = sub_figs[0].subplots(1, 3)
        sub_figs[0].suptitle('Original Image')

        conf_plot(axs_t[0], ColorChannel.RED, h1r, be1r, with_title=True)
        conf_plot(axs_t[1], ColorChannel.GREEN, h1g, be1g, with_title=True)
        conf_plot(axs_t[2], ColorChannel.BLUE, h1b, be1b, with_title=True)

        axs_m = sub_figs[1].subplots(1, 3)
        sub_figs[1].suptitle('Stego Object')

        conf_plot(axs_m[0], ColorChannel.RED, h2r, be2r)
        conf_plot(axs_m[1], ColorChannel.GREEN, h2g, be2g)
        conf_plot(axs_m[2], ColorChannel.BLUE, h2b, be2b)

        axs_b = sub_figs[2].subplots(1, 3)
        sub_figs[2].suptitle('Pixel Histogram Difference')

        conf_plot(axs_b[0], ColorChannel.RED, (h1r - h2r), be2r)
        conf_plot(axs_b[1], ColorChannel.GREEN, (h1g - h2g), be2g)
        conf_plot(axs_b[2], ColorChannel.BLUE, (h1b - h2b), be2b)

        axs_t[0].set_ylabel('Pixel Count')
        axs_m[0].set_ylabel('Pixel Count')
        axs_b[0].set_ylabel('Pixel Count')
        axs_m[1].set_xlabel('Colour Intensity')

        for ax in axs_b:
            ax.spines['bottom'].set_position('center')

        fig.suptitle('Pixel Histogram Difference of Each Channel')

        if save_plot:
            out_dir = out_dir.strip('/')
            out_dir = f'/{out_dir}' if out_dir else ''
            plot_path = f'./output{out_dir}/pd_hist_{time.time_ns()}.png'
            plt.savefig(plot_path)

        plt.close(fig)

    return {
        'original': {
            'path': o_path,
            'red': {
                'histogram': h1r.tolist(),
                'bin_edges': be1r.tolist()
            },
            'green': {
                'histogram': h1g.tolist(),
                'bin_edges': be1g.tolist()
            },
            'blue': {
                'histogram': h1b.tolist(),
                'bin_edges': be1b.tolist()
            }
        },
        'stego': {
            'path': s_path,
            'red': {
                'histogram': h2r.tolist(),
                'bin_edges': be2r.tolist()
            },
            'green': {
                'histogram': h2g.tolist(),
                'bin_edges': be2g.tolist()
            },
            'blue': {
                'histogram': h2b.tolist(),
                'bin_edges': be2b.tolist()
            }
        },
        'plot_path': plot_path
    }


def diff(c_o: list, c_s: list):
    return np.array(c_o) - np.array(c_s)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-o', '--original', required=True, help='Path of the carrier image file')
    ap.add_argument('-s', '--stego', required=True, help='Path of the stego object file')
    args = vars(ap.parse_args())

    res = hist_rgb(args['original'], args['stego'], make_plot=True)
    exit()
