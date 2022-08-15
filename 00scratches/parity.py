def even_8parity(x: int, mask: int = 255):
    x = x & mask

    x = (x & 15) ^ (x >> 4)
    x = (x & 3) ^ (x >> 2)
    x = (x & 1) ^ (x >> 1)

    return x


if __name__ == '__main__':
    print(even_8parity(119))
    print(even_8parity(118))
    print(even_8parity(211))
    print(even_8parity(222))
    print(even_8parity(193))
    exit()
