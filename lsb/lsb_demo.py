import argparse

import numpy as np
from PIL import Image


def count_channels(img_mode: str):
    return 3 if img_mode == 'RGB' else 4


def to_bin(num: int, ln: int = 8):
    return [num >> i & 1 for i in range(ln - 1, -1, -1)]


def encode(src: str, message: str, dest: str):
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    ch_count = count_channels(img.mode)
    img_pixel_count = array.size // ch_count

    message = "$"
    b_message = []

    for c in message:
        b_message.extend(to_bin(ord(c)))

    msg_len = len(b_message)

    if msg_len > img_pixel_count:
        print("ERROR: Need larger file size")
    else:
        for i in range(msg_len):
            p = i // ch_count
            q = i % ch_count

            array[p][q] = array[p][q] & 254 | b_message[i]

        array = array.reshape([height, width, ch_count])
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully")


def decode(src):
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    channel_count = count_channels(img.mode)
    total_pixels = array.size // channel_count

    byte_buf = ""
    lsb_bytes = []

    for i in range(array.size):
        p = i // channel_count
        q = i % channel_count
        lsb = to_bin(array[p][q])[-1]
        print(array[p][q], lsb)
        byte_buf += str(lsb)

        if len(byte_buf) == 8:
            ord_v = int(''.join(str(i) for i in byte_buf), 2)
            if ord_v < 128:
                lsb_bytes.append(chr(ord_v))
                byte_buf = ""

    # hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]
    #
    message = ''.join(lsb_bytes)

    if "$" in message:
        print("Hidden Message:", message[:-5])
    else:
        print("No Hidden Message Found")


def compare(cover_path: str, stego_path: str):
    cover = np.array(list(Image.open(cover_path, 'r').getdata()))
    stego = np.array(list(Image.open(stego_path, 'r').getdata()))

    for i in range(len(cover)):
        print(cover[i], stego[i])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("op", nargs=1, help="Specifies the operation type", choices=['encode', 'decode', 'compare'])
    ap.add_argument("-c", "--cover", help="Path to the cover image")
    ap.add_argument("-s", "--stego", help="Path to stego object")
    ap.add_argument("-m", "--message", help="Message to be embedded")
    ap.add_argument("-o", "--output", help="Stego output path")
    ap.add_argument("-i", "--input", help="Stego object path")

    args = vars(ap.parse_args())

    op = args['op'][0]

    if op == 'encode':
        if args['cover'] is None or args['message'] is None or args['output'] is None:
            ap.error("encode requires --cover, --message and --output.")
        print('Embedding secret...')
        encode(args['cover'], args['message'], args['output'])
        print('...DONE!')

    elif op == 'decode':
        if args['input'] is None:
            ap.error("decode requires --input.")
        print('Retrieving secret...')
        decode(args['input'])
        print("...DONE!")

    elif op == 'compare':
        if args['cover'] is None or args['stego'] is None:
            ap.error("decode requires --cover and --stego.")
        print('Comparing stego and cover...')
        compare(args['cover'], args['stego'])
        print("...DONE!")

    exit()
