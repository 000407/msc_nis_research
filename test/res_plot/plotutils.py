def conf_plots_dip_all(sub_figs, df, x):
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


def conf_plots_dip_vs(sub_figs, df, x, i: int, y_name: str, y_title: str, **kwargs):
    ax = sub_figs[i].subplots(1, 1)
    sub_figs[i].suptitle(y_title, fontsize=15, fontweight='bold')
    ax.plot(x, df.loc[:, y_name])

    if 'ylim' in kwargs.keys() and kwargs['ylim'] is not None:
        ax.set(ylim=kwargs['ylim'])

    ax.set_ylabel(' ')
    if 'ylabel' in kwargs.keys() and kwargs['ylabel'] is not None:
        ax.set_ylabel(kwargs['ylabel'])

    if 'ticklabel_fmt_offset' in kwargs.keys():
        ax.ticklabel_format(useOffset=kwargs['ticklabel_fmt_offset'])
