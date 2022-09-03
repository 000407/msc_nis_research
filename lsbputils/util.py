import random


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


def get_random_secret(length: int):
    return random.randrange(
        2 ** (length - 1),
        2 ** length
    )
