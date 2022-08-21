class LSBPlus:
    def __init__(self, degree=3):
        self._degree = degree
        self._mask_432_lob = 28
        self._mask_32_lob = 12
        self._mask_210_lob = 7
        self._mask_10_lob = 3
        self._mask_0_lob = 1
        self._mask_e_flag = 128

    def get_even_parity(self, x: int, mask: int = -1) -> int:
        if mask == -1:
            mask = (2 ** (2 ** 3)) - 1

        x = x & mask

        for i in reversed(range(self._degree)):
            v = 2 ** i
            x = (x & ((2 ** v) - 1)) ^ (x >> v)

        return x

    def embed(self, secret_bits: int, c_blocks: list[tuple[int, int]]) \
            -> tuple[list[int], int]:
        if secret_bits == 0:
            return [n[1] for n in c_blocks], secret_bits

        e_blocks = []

        for tpl in c_blocks:
            key = tpl[0]
            c_block = tpl[1] ^ key

            is_dyn_embeddable = (c_block & self._mask_e_flag) == 128 \
                or self.get_even_parity(c_block, mask=224) == 1

            if secret_bits > 0:
                # print(f'{"T" if (c_block & self._mask_e_flag) == 128 else "F"}{"T" if self.get_even_parity(c_block, mask=224) == 1 else "F"}->', end='')
                if is_dyn_embeddable:
                    c_432_lob = (c_block & self._mask_432_lob) >> 2
                    c_32_lob = (c_block & self._mask_32_lob) >> 2

                    s_210_lob = secret_bits & self._mask_210_lob
                    s_10_lob = secret_bits & self._mask_10_lob
                    s_0_lob = secret_bits & self._mask_0_lob

                    if c_432_lob == s_210_lob:
                        c_10_lob = 3
                        # e_bits = f'(03){c_432_lob:0b}'
                        secret_bits >>= 3
                    elif c_32_lob == s_10_lob:
                        c_10_lob = 2
                        # e_bits = f'(02){c_32_lob:0b}'
                        secret_bits >>= 2
                    elif s_0_lob == 1:
                        c_10_lob = 1
                        # e_bits = f'(01){s_0_lob:0b}'
                        secret_bits >>= 1
                    else:
                        c_10_lob = 0
                        # e_bits = f'(00){s_0_lob:0b}'
                        secret_bits >>= 1

                    c_block = c_block & 252 | c_10_lob
                    # print(f'{e_bits} = {(tpl[1] ^ key):08b} -> {c_block:08b}')
                else:
                    c_block = c_block & 254 | (secret_bits & 1)
                    # print(f'(--){(secret_bits & 1):0b} = {(tpl[1] ^ key):08b} -> {c_block:08b}')
                    secret_bits >>= 1

            e_blocks.append(c_block ^ key)

        return e_blocks, secret_bits

    def extract(self, c_blocks: list[tuple[int, int]]) -> int:
        secret_bits = 0
        emb_len = 0
        for tpl in c_blocks:
            key = tpl[0]
            c_block = tpl[1] ^ key

            is_dyn_embeddable = (c_block & self._mask_e_flag) == 128 \
                or self.get_even_parity(c_block, mask=224) == 1

            # print(f'{"T" if (c_block & self._mask_e_flag) == 128 else "F"}{"T" if self.get_even_parity(c_block, mask=224) == 1 else "F"}->', end='')
            if is_dyn_embeddable:
                flag = c_block & self._mask_10_lob
                if flag == 3:
                    # print(f'{((c_block & self._mask_432_lob) >> 2):0b}')
                    secret_bits = (((c_block & self._mask_432_lob) >> 2) << emb_len) | secret_bits
                    emb_len += 3
                elif flag == 2:
                    # print(f'{((c_block & self._mask_32_lob) >> 2):0b}')
                    secret_bits = (((c_block & self._mask_32_lob) >> 2) << emb_len) | secret_bits
                    emb_len += 2
                elif flag == 1:
                    # print(f'1')
                    secret_bits = (1 << emb_len) | secret_bits
                    emb_len += 1
                else:
                    # print(f'0')
                    emb_len += 1
            else:
                # print(f'{(c_block & 1)}')
                secret_bits = ((c_block & 1) << emb_len) | secret_bits
                emb_len += 1

        return secret_bits


if __name__ == '__main__':
    c_bytes = [
        35,
        160,
        252,
        157,
        225,
        207,
        199,
        192,
        211,
        164,
        217,
        182,
        221,
        202,
        214,
        194,
        123,
    ]

    s_bits = 3557

    lsb_plus = LSBPlus()
    print(f"{s_bits:0b}")
    e_bytes, r_s_bits = lsb_plus.embed(s_bits, [(244, b) for b in c_bytes])

    print(f'c_bytes  = {[f"{(n ^ 244):08b}" for n in c_bytes]}')
    print(f'e_bytes  = {[f"{(n ^ 244):08b}" for n in e_bytes]}')
    print(f'r_s_bits = {r_s_bits}')

    e_s_bits = lsb_plus.extract([(244, b) for b in e_bytes])
    print(f's_bits   = {format(s_bits, f"0{e_s_bits.bit_length()}b")}')
    print(f'e_s_bits = {e_s_bits:0b}')

    message = f'{s_bits:0b} == {e_s_bits:0b} ? {True if (s_bits & e_s_bits) == s_bits else False}'
    print(message)

    # exit()
