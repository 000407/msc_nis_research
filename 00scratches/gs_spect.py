import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


if __name__ == '__main__':
    fig, ax = plt.subplots()

    length = 1

    ax.plot()

    for x in range(16):
        for y in range(16):
            color = f'{x:x}{y:x}' * 3
            ax.add_patch(
                Rectangle((y + 1, x + 1), length, length, facecolor=f'#{color}', edgecolor='#000', linewidth=0.25))

    # plt.show()
    fig.savefig('gs_spect.png', format='png', dpi=1200)
