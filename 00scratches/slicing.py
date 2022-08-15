import numpy as np

if __name__ == '__main__':
    arr = np.array(
        [
            [
                [11, 12, 13],
                [14, 15, 16],
                [17, 18, 19]
            ],
            [
                [23, 22, 21],
                [26, 25, 24],
                [29, 28, 27]
            ],
            [
                [31, 34, 37],
                [32, 35, 38],
                [33, 36, 39]
            ]
        ]
    )

    # print([arr[:, :, k] for k in range(len(arr))])

