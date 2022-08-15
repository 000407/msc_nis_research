def even_8parity(x: int, mask: int = 255):
    x = x & mask

    x = (x & 15) ^ (x >> 4)
    x = (x & 3) ^ (x >> 2)
    x = (x & 1) ^ (x >> 1)

    return x


def embed(s_bits: int, c_blocks: list[tuple[int, int]]):
    e_blocks = []

    for tpl in c_blocks:
        key = tpl[0]
        c_block = tpl[1] ^ key

        mask_ef = 32
        mask_el = 24
        mask_b = 255
        max_embed_len = 3

        # 1. Derive embeddable length
        p_len = (c_block & mask_el) >> max_embed_len

        # 2.1. Derive the value for is_embeddable flag (3rd bit)
        is_embeddable = (c_block & mask_ef) == mask_ef

        # 2.2. Derive the value for is_embeddable flag (even parity)
        if not is_embeddable:
            is_embeddable = even_8parity(c_block, 224) == 1

        # 3. Derive effective block mask
        mask_fb = mask_b >> (8 - p_len)

        # 4. Extract embeddable secret bits
        s_bits_e = s_bits & mask_fb

        # 5. Extract embeddable carrier bits
        c_bits_e = c_block & mask_fb

        # 6. Dynamic LSB embedding
        if is_embeddable:
            if s_bits_e == c_bits_e and p_len > 0:
                print('Secret bits and carrier bits match!')
                s_bits >>= p_len
            elif p_len <= 1:
                print('LSB embedding len <= 1...')
                c_block = c_block & 254 | (s_bits & 1)
                s_bits >>= 1
            else:
                print(f'LSB embedding...')
                c_block = c_block & 254 | (s_bits & 1)
                s_bits >>= 1

        e_blocks.append(c_block ^ key)

        # 7. Exit from the loop
        # if all bits of the secret payload are embedded
        if s_bits == 0:
            break

    return e_blocks, s_bits


if __name__ == '__main__':
    c_bytes = [
        (244, 129),
        (244, 160),
        (244, 252),
        (244, 157),
        (244, 225),
        (244, 110),
        (244, 141),
        (244, 192),
        (244, 211),
        (244, 164),
        (244, 217),
        (244, 182)
    ]

    s_bits = 3557

    e_bytes, s_bits = embed(s_bits, c_bytes)

    print(f'c_bytes = {[x[1] for x in c_bytes]}')
    print(f'e_bytes = {e_bytes}')
    print(f's_bits = {s_bits}')

    exit()
